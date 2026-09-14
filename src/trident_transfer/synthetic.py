"""Synthetic longitudinal datasets for pipeline development and falsification tests.

The simulator is not intended as a substantive model of human learning. It creates
known data-generating mechanisms so that analysis code can be checked before restricted
or external datasets are introduced.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SyntheticConfig:
    n_participants: int = 120
    n_sessions: int = 40
    tasks_per_construct: int = 3
    constructs: tuple[str, ...] = ("working_memory", "perceptual_speed", "episodic_memory")
    observations_per_session: int = 2
    noise_sd: float = 0.035
    general_learnability_sd: float = 0.18
    task_rate_sd: float = 0.10
    cross_construct_facilitation: float = 0.0
    seed: int = 42


def simulate_longitudinal_data(config: SyntheticConfig = SyntheticConfig()) -> pd.DataFrame:
    """Generate multi-task repeated performance with optional cross-construct coupling.

    `cross_construct_facilitation` controls a deliberately simple mechanism: progress in
    the preceding construct modestly increases the effective learning rate of the next
    construct. A value of zero is therefore a useful null simulation.
    """

    rng = np.random.default_rng(config.seed)
    rows: list[dict[str, float | int | str]] = []

    task_defs: list[tuple[str, str, float]] = []
    for c_idx, construct in enumerate(config.constructs):
        for task_idx in range(config.tasks_per_construct):
            task_id = f"{construct}_task_{task_idx + 1}"
            base_rate = 0.055 + 0.006 * task_idx + 0.003 * c_idx
            task_defs.append((construct, task_id, base_rate))

    for participant in range(config.n_participants):
        pid = f"P{participant + 1:04d}"
        general = rng.normal(0.0, config.general_learnability_sd)
        participant_start = rng.normal(0.0, 0.035)
        prior_construct_progress = 0.0

        for c_idx, construct in enumerate(config.constructs):
            construct_shift = rng.normal(0.0, 0.05)
            construct_tasks = [task for task in task_defs if task[0] == construct]
            construct_endpoints: list[float] = []

            for _, task_id, base_rate in construct_tasks:
                rate_multiplier = np.exp(general + rng.normal(0.0, config.task_rate_sd))
                facilitation = 1.0 + config.cross_construct_facilitation * prior_construct_progress
                rate = max(0.004, base_rate * rate_multiplier * facilitation)

                start = np.clip(0.42 + participant_start + construct_shift + rng.normal(0, 0.025), 0.20, 0.70)
                asymptote = np.clip(0.86 + 0.035 * general + rng.normal(0, 0.025), 0.68, 0.97)

                for session in range(1, config.n_sessions + 1):
                    expected = asymptote - (asymptote - start) * np.exp(-rate * (session - 1))
                    for block in range(1, config.observations_per_session + 1):
                        score = float(np.clip(expected + rng.normal(0, config.noise_sd), 0.0, 1.0))
                        rows.append(
                            {
                                "participant_id": pid,
                                "task_id": task_id,
                                "construct": construct,
                                "session": session,
                                "block": block,
                                "performance": score,
                            }
                        )
                construct_endpoints.append(asymptote - start)

            prior_construct_progress = float(np.mean(construct_endpoints)) if construct_endpoints else 0.0

    return pd.DataFrame(rows)


def simulate_transfer_outcomes(
    features: pd.DataFrame,
    *,
    mechanism: str = "M3",
    noise_sd: float = 0.05,
    seed: int = 123,
) -> pd.DataFrame:
    """Create synthetic untrained-task transfer outcomes from known mechanisms.

    This allows the model tournament to be tested for recovery of M0-M5 under controlled
    conditions. The target is `transfer_gain`; higher values indicate better transfer.
    """

    rng = np.random.default_rng(seed)
    data = features.copy()
    if data.empty:
        raise ValueError("features must contain at least one participant/task row")

    signal = np.zeros(len(data), dtype=float)
    baseline = data.get("baseline_score", pd.Series(0.0, index=data.index)).fillna(0).to_numpy()
    endpoint = data.get("endpoint_score", pd.Series(0.0, index=data.index)).fillna(0).to_numpy()
    gain = data.get("gain", pd.Series(0.0, index=data.index)).fillna(0).to_numpy()
    early = data.get("early_slope", pd.Series(0.0, index=data.index)).fillna(0).to_numpy()
    plateau = data.get("plateau_session", pd.Series(0.0, index=data.index)).fillna(0).to_numpy()
    post = data.get("post_plateau_gain", pd.Series(0.0, index=data.index)).fillna(0).to_numpy()
    other_gain = data.get("construct_other_gain", pd.Series(0.0, index=data.index)).fillna(0).to_numpy()
    breadth = data.get("construct_breadth_sd", pd.Series(0.0, index=data.index)).fillna(0).to_numpy()

    if mechanism == "M0":
        signal = 0.15 * baseline + 0.25 * endpoint
    elif mechanism == "M1":
        signal = 0.15 * baseline + 0.35 * gain
    elif mechanism == "M2":
        signal = 0.15 * gain + 0.35 * other_gain
    elif mechanism == "M3":
        signal = 0.10 * gain + 3.0 * early + 0.25 * post
    elif mechanism == "M4":
        scaled_plateau = np.where(plateau > 0, 1.0 / (1.0 + plateau), 0.0)
        signal = 0.10 * gain + 0.35 * post + 1.5 * scaled_plateau
    elif mechanism == "M5":
        signal = 0.10 * gain + 0.30 * other_gain - 0.25 * breadth
    else:
        raise ValueError(f"Unknown synthetic mechanism: {mechanism}")

    out = data[["participant_id", "task_id", "construct"]].copy()
    out["transfer_gain"] = signal + rng.normal(0.0, noise_sd, len(signal))
    return out
