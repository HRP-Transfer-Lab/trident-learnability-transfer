"""Adapter for gameplay-level Lumosity learning data.

The open Steyvers-Schafer release has been distributed in multiple processed/raw forms.
Rather than hard-code column names before the downloaded files are inspected, this
adapter accepts an explicit mapping and converts each gameplay into the common schema.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ..schema import validate_longitudinal_frame


@dataclass(frozen=True)
class LumosityColumns:
    participant: str
    game: str
    gameplay_index: str
    score: str
    construct: str | None = None
    timestamp: str | None = None


def adapt_lumosity_gameplays(
    frame: pd.DataFrame,
    columns: LumosityColumns,
    *,
    game_to_construct: dict[str, str] | None = None,
    score_is_higher_better: bool = True,
) -> pd.DataFrame:
    """Convert gameplay-level Lumosity rows to canonical longitudinal format.

    Parameters
    ----------
    frame:
        Raw or preprocessed gameplay table.
    columns:
        Explicit source-column mapping.
    game_to_construct:
        Optional mapping used when a construct/domain column is not present.
    score_is_higher_better:
        If False, the source score is multiplied by -1 so canonical `performance`
        always follows the higher-is-better convention.
    """

    required_source = [columns.participant, columns.game, columns.gameplay_index, columns.score]
    missing = [name for name in required_source if name not in frame.columns]
    if missing:
        raise ValueError(f"Lumosity source table missing columns: {missing}")

    out = pd.DataFrame(
        {
            "participant_id": frame[columns.participant].astype(str),
            "task_id": frame[columns.game].astype(str),
            "session": pd.to_numeric(frame[columns.gameplay_index], errors="coerce"),
            "performance": pd.to_numeric(frame[columns.score], errors="coerce"),
        }
    )

    if not score_is_higher_better:
        out["performance"] = -out["performance"]

    if columns.construct is not None:
        if columns.construct not in frame.columns:
            raise ValueError(f"Construct column not found: {columns.construct}")
        out["construct"] = frame[columns.construct].astype(str)
    elif game_to_construct is not None:
        out["construct"] = out["task_id"].map(game_to_construct)
    else:
        out["construct"] = "unknown"

    if columns.timestamp is not None:
        if columns.timestamp not in frame.columns:
            raise ValueError(f"Timestamp column not found: {columns.timestamp}")
        out["timestamp"] = pd.to_datetime(frame[columns.timestamp], errors="coerce", utc=True)

    out = out.dropna(subset=["session", "performance"])
    return validate_longitudinal_frame(out)
