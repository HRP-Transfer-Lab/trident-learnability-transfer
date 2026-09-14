"""Interpretable learning-curve features for transfer-model comparisons."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from .schema import validate_longitudinal_frame


def _linear_slope(x: np.ndarray, y: np.ndarray) -> float:
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]
    if len(x) < 2 or np.allclose(x, x[0]):
        return float("nan")
    return float(np.polyfit(x, y, 1)[0])


def _plateau_session(
    sessions: np.ndarray,
    performance: np.ndarray,
    *,
    window: int,
    slope_tolerance: float,
    minimum_fraction: float,
) -> float:
    """Return the first session with a persistently small local slope.

    This is deliberately a conservative descriptive heuristic, not a claim that a
    cognitive state transition has occurred. Real analyses should compare this with
    nonlinear and change-point alternatives.
    """

    n = len(sessions)
    if n < max(window + 1, 6):
        return float("nan")

    start = max(window, int(math.ceil(n * minimum_fraction)))
    for end in range(start, n + 1):
        local_x = sessions[end - window : end]
        local_y = performance[end - window : end]
        slope = _linear_slope(local_x, local_y)
        if np.isfinite(slope) and abs(slope) <= slope_tolerance:
            return float(local_x[-1])
    return float("nan")


def extract_learning_features(
    frame: pd.DataFrame,
    *,
    early_fraction: float = 0.25,
    late_fraction: float = 0.25,
    plateau_window: int = 5,
    plateau_slope_tolerance: float = 0.002,
    plateau_minimum_fraction: float = 0.30,
) -> pd.DataFrame:
    """Summarise participant-by-task learning trajectories.

    The input may contain trial-, block-, or gameplay-level rows. Performance is first
    averaged within session so that tasks with different trial counts do not dominate.

    Returned features are intentionally simple and interpretable. They form the first
    layer of the M0-M5 tournament and should later be compared with nonlinear learning
    curves and formal change-point models.
    """

    data = validate_longitudinal_frame(frame)
    session_level = (
        data.groupby(["participant_id", "task_id", "construct", "session"], observed=True)
        .agg(performance=("performance", "mean"))
        .reset_index()
    )

    rows: list[dict[str, float | str]] = []
    for (participant_id, task_id, construct), group in session_level.groupby(
        ["participant_id", "task_id", "construct"], observed=True, sort=False
    ):
        group = group.sort_values("session")
        sessions = group["session"].to_numpy(dtype=float)
        perf = group["performance"].to_numpy(dtype=float)
        mask = np.isfinite(sessions) & np.isfinite(perf)
        sessions = sessions[mask]
        perf = perf[mask]
        n = len(perf)
        if n < 2:
            continue

        n_early = max(2, int(math.ceil(n * early_fraction)))
        n_late = max(2, int(math.ceil(n * late_fraction)))
        plateau = _plateau_session(
            sessions,
            perf,
            window=plateau_window,
            slope_tolerance=plateau_slope_tolerance,
            minimum_fraction=plateau_minimum_fraction,
        )

        overall_slope = _linear_slope(sessions, perf)
        fitted = np.polyval(np.polyfit(sessions, perf, 1), sessions)
        residual_sd = float(np.std(perf - fitted, ddof=1)) if n > 2 else float("nan")

        post_plateau_slope = float("nan")
        post_plateau_gain = float("nan")
        if np.isfinite(plateau):
            post_mask = sessions >= plateau
            if int(post_mask.sum()) >= 2:
                post_plateau_slope = _linear_slope(sessions[post_mask], perf[post_mask])
                post_plateau_gain = float(perf[post_mask][-1] - perf[post_mask][0])

        rows.append(
            {
                "participant_id": participant_id,
                "task_id": task_id,
                "construct": construct,
                "n_sessions": n,
                "baseline_score": float(perf[0]),
                "endpoint_score": float(perf[-1]),
                "gain": float(perf[-1] - perf[0]),
                "overall_slope": overall_slope,
                "early_slope": _linear_slope(sessions[:n_early], perf[:n_early]),
                "late_slope": _linear_slope(sessions[-n_late:], perf[-n_late:]),
                "asymptote_proxy": float(np.mean(perf[-n_late:])),
                "residual_sd": residual_sd,
                "plateau_session": plateau,
                "post_plateau_slope": post_plateau_slope,
                "post_plateau_gain": post_plateau_gain,
            }
        )

    return pd.DataFrame(rows)


def add_construct_context(features: pd.DataFrame) -> pd.DataFrame:
    """Add participant-level construct breadth features used by M2 and M5.

    For each task row, construct means are computed from the *other* tasks in the same
    construct where possible. This leave-one-task-out construction reduces circularity
    when a source task is itself being used to predict its transfer outcome.
    """

    required = {"participant_id", "task_id", "construct", "gain", "early_slope"}
    missing = required.difference(features.columns)
    if missing:
        raise ValueError(f"Missing columns for construct context: {sorted(missing)}")

    out = features.copy()
    out["construct_other_gain"] = np.nan
    out["construct_other_early_slope"] = np.nan
    out["construct_breadth_sd"] = np.nan

    for (_, construct), idx in out.groupby(["participant_id", "construct"], observed=True).groups.items():
        group = out.loc[idx]
        for row_idx in idx:
            others = group[group.index != row_idx]
            if others.empty:
                continue
            out.loc[row_idx, "construct_other_gain"] = others["gain"].mean()
            out.loc[row_idx, "construct_other_early_slope"] = others["early_slope"].mean()
            out.loc[row_idx, "construct_breadth_sd"] = others["gain"].std(ddof=0)

    return out
