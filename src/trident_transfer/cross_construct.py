"""Utilities for analysing cross-construct learning velocities (M6-M11)."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .schema import validate_longitudinal_frame


def _slope(x: np.ndarray, y: np.ndarray) -> float:
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]
    if len(x) < 2 or np.allclose(x, x[0]):
        return float("nan")
    return float(np.polyfit(x, y, 1)[0])


def windowed_construct_velocity(
    frame: pd.DataFrame,
    *,
    window_size: int = 5,
    step: int | None = None,
) -> pd.DataFrame:
    """Estimate local construct-level learning velocity in session windows.

    Task observations are first averaged within participant/task/session and then
    averaged across tasks within construct/session. Windows are defined within each
    participant/construct trajectory, which permits datasets with missing sessions.
    """

    if window_size < 2:
        raise ValueError("window_size must be at least 2")
    if step is None:
        step = window_size
    if step < 1:
        raise ValueError("step must be at least 1")

    data = validate_longitudinal_frame(frame)
    task_session = (
        data.groupby(["participant_id", "construct", "task_id", "session"], observed=True)
        .agg(performance=("performance", "mean"))
        .reset_index()
    )
    construct_session = (
        task_session.groupby(["participant_id", "construct", "session"], observed=True)
        .agg(performance=("performance", "mean"), n_tasks=("task_id", "nunique"))
        .reset_index()
    )

    rows: list[dict[str, float | int | str]] = []
    for (participant_id, construct), group in construct_session.groupby(
        ["participant_id", "construct"], observed=True, sort=False
    ):
        group = group.sort_values("session").reset_index(drop=True)
        if len(group) < window_size:
            continue
        window_index = 0
        for start in range(0, len(group) - window_size + 1, step):
            chunk = group.iloc[start : start + window_size]
            x = chunk["session"].to_numpy(dtype=float)
            y = chunk["performance"].to_numpy(dtype=float)
            rows.append(
                {
                    "participant_id": participant_id,
                    "construct": construct,
                    "window_index": window_index,
                    "session_start": float(x[0]),
                    "session_end": float(x[-1]),
                    "mean_performance": float(np.mean(y)),
                    "learning_velocity": _slope(x, y),
                    "performance_change": float(y[-1] - y[0]),
                    "mean_n_tasks": float(chunk["n_tasks"].mean()),
                }
            )
            window_index += 1

    return pd.DataFrame(rows)


def make_directional_panel(
    velocities: pd.DataFrame,
    source_construct: str,
    target_construct: str,
) -> pd.DataFrame:
    """Create a lagged panel for directed facilitation tests.

    Output rows contain source learning velocity in window t, target velocity in the
    same window, and target velocity in window t+1. This supports the canonical model:

        target_velocity_t+1 ~ target_velocity_t + source_velocity_t + time + person

    The reverse direction should always be fitted as a compulsory comparison.
    """

    needed = {"participant_id", "construct", "window_index", "learning_velocity", "mean_performance"}
    missing = needed.difference(velocities.columns)
    if missing:
        raise ValueError(f"Missing velocity columns: {sorted(missing)}")

    subset = velocities[velocities["construct"].isin([source_construct, target_construct])].copy()
    wide_v = subset.pivot_table(
        index=["participant_id", "window_index"],
        columns="construct",
        values="learning_velocity",
        aggfunc="mean",
    )
    wide_p = subset.pivot_table(
        index=["participant_id", "window_index"],
        columns="construct",
        values="mean_performance",
        aggfunc="mean",
    )

    if source_construct not in wide_v.columns or target_construct not in wide_v.columns:
        return pd.DataFrame()

    panel = pd.DataFrame(index=wide_v.index).reset_index()
    panel["source_velocity_t"] = wide_v[source_construct].to_numpy()
    panel["target_velocity_t"] = wide_v[target_construct].to_numpy()
    panel["source_performance_t"] = wide_p[source_construct].to_numpy()
    panel["target_performance_t"] = wide_p[target_construct].to_numpy()
    panel = panel.sort_values(["participant_id", "window_index"])
    panel["target_velocity_t1"] = panel.groupby("participant_id", observed=True)["target_velocity_t"].shift(-1)
    panel["target_performance_t1"] = panel.groupby("participant_id", observed=True)["target_performance_t"].shift(-1)
    panel["source_construct"] = source_construct
    panel["target_construct"] = target_construct
    return panel.reset_index(drop=True)
