"""Canonical long-format schema for longitudinal cognitive-task data.

The project intentionally separates source-specific ingestion from downstream analysis.
Every dataset adapter should return one row per observation (trial, block, or gameplay)
with the common identifiers defined here. `performance` must be coded so that larger
values mean better performance; source-specific raw measures should be retained in
additional columns where possible.
"""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


CANONICAL_COLUMNS = (
    "participant_id",
    "task_id",
    "construct",
    "session",
    "performance",
)

OPTIONAL_COLUMNS = (
    "block",
    "trial",
    "accuracy",
    "rt_ms",
    "condition",
    "wrapper",
    "timestamp",
    "difficulty",
)


def validate_longitudinal_frame(
    frame: pd.DataFrame,
    *,
    required: Iterable[str] = CANONICAL_COLUMNS,
    require_multiple_sessions: bool = True,
) -> pd.DataFrame:
    """Validate and return a sorted copy of a canonical longitudinal dataframe.

    Parameters
    ----------
    frame:
        Input observations.
    required:
        Columns required for a particular analysis.
    require_multiple_sessions:
        If True, every participant/task series must contain at least two distinct
        sessions. This can be disabled for ingestion diagnostics.

    Raises
    ------
    ValueError
        If required columns are absent, identifiers are missing, sessions cannot be
        interpreted numerically, performance is non-numeric, or repeated-session
        structure is absent where required.
    """

    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    out = frame.copy()

    id_columns = [column for column in ("participant_id", "task_id") if column in out]
    if id_columns and out[id_columns].isna().any().any():
        raise ValueError("participant_id and task_id must not contain missing values")

    if "session" in out:
        out["session"] = pd.to_numeric(out["session"], errors="coerce")
        if out["session"].isna().any():
            raise ValueError("session must be numeric or coercible to numeric")

    if "performance" in out:
        out["performance"] = pd.to_numeric(out["performance"], errors="coerce")
        if out["performance"].isna().all():
            raise ValueError("performance contains no usable numeric observations")

    if require_multiple_sessions and {"participant_id", "task_id", "session"}.issubset(out.columns):
        counts = out.groupby(["participant_id", "task_id"], observed=True)["session"].nunique()
        bad = counts[counts < 2]
        if not bad.empty:
            examples = list(bad.index[:5])
            raise ValueError(
                "Longitudinal analysis requires at least two sessions per participant/task; "
                f"examples with insufficient data: {examples}"
            )

    sort_columns = [
        column
        for column in ("participant_id", "task_id", "session", "block", "trial")
        if column in out.columns
    ]
    if sort_columns:
        out = out.sort_values(sort_columns, kind="stable").reset_index(drop=True)

    return out
