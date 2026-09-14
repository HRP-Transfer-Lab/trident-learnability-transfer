"""Participant-isolated predictive comparison for construct-transfer mechanisms M0-M5."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import TransformedTargetRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


MODEL_FEATURES: dict[str, tuple[str, ...]] = {
    # Task-specific fluency / endpoint null.
    "M0_task_specific": (
        "baseline_score",
        "endpoint_score",
    ),
    # Same-operation portability: source-task improvement matters.
    "M1_surface_invariant": (
        "baseline_score",
        "endpoint_score",
        "gain",
    ),
    # Construct strengthening: other tasks in the construct contribute.
    "M2_construct_strengthening": (
        "baseline_score",
        "gain",
        "construct_other_gain",
        "construct_other_early_slope",
    ),
    # Learning dynamics: trajectory shape matters beyond endpoints.
    "M3_learning_dynamics": (
        "baseline_score",
        "endpoint_score",
        "gain",
        "early_slope",
        "late_slope",
        "overall_slope",
        "residual_sd",
    ),
    # Plateau/reorganisation: flattening and renewed improvement matter.
    "M4_plateau_reorganisation": (
        "baseline_score",
        "gain",
        "early_slope",
        "late_slope",
        "plateau_session",
        "post_plateau_slope",
        "post_plateau_gain",
        "residual_sd",
    ),
    # Breadth/variation: distributed learning across related tasks matters.
    "M5_breadth_variation": (
        "baseline_score",
        "gain",
        "early_slope",
        "construct_other_gain",
        "construct_other_early_slope",
        "construct_breadth_sd",
        "residual_sd",
    ),
}


@dataclass(frozen=True)
class TournamentConfig:
    target: str = "transfer_gain"
    n_splits: int = 5
    ridge_alpha: float = 1.0


def _estimator(alpha: float) -> TransformedTargetRegressor:
    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median", add_indicator=True)),
            ("scaler", StandardScaler()),
            ("ridge", Ridge(alpha=alpha)),
        ]
    )
    return TransformedTargetRegressor(regressor=model, transformer=StandardScaler())


def evaluate_construct_tournament(
    features: pd.DataFrame,
    outcomes: pd.DataFrame,
    *,
    config: TournamentConfig = TournamentConfig(),
) -> pd.DataFrame:
    """Evaluate M0-M5 with participant-isolated held-out prediction.

    Parameters
    ----------
    features:
        Participant-by-task learning features.
    outcomes:
        Table containing participant_id, task_id and the transfer outcome.

    Notes
    -----
    The initial implementation intentionally uses the same regularised linear learner
    for every mechanism. The contest is therefore primarily about *which information*
    improves out-of-sample prediction, not which model gets the most flexible learner.
    More complex nonlinear models can be added after the baseline contract is stable.
    """

    keys = ["participant_id", "task_id"]
    missing_outcome = [column for column in [*keys, config.target] if column not in outcomes.columns]
    if missing_outcome:
        raise ValueError(f"Outcomes missing required columns: {missing_outcome}")

    data = features.merge(outcomes[keys + [config.target]], on=keys, how="inner", validate="one_to_one")
    data = data.dropna(subset=[config.target, "participant_id"])
    if data.empty:
        raise ValueError("No matched feature/outcome rows available")

    n_groups = data["participant_id"].nunique()
    if n_groups < 2:
        raise ValueError("At least two participants are required for held-out evaluation")
    n_splits = min(config.n_splits, n_groups)
    if n_splits < 2:
        raise ValueError("n_splits must permit at least two participant-isolated folds")

    cv = GroupKFold(n_splits=n_splits)
    groups = data["participant_id"].to_numpy()
    y = data[config.target].to_numpy(dtype=float)

    results: list[dict[str, float | int | str]] = []
    for model_name, feature_names in MODEL_FEATURES.items():
        missing = [column for column in feature_names if column not in data.columns]
        if missing:
            results.append(
                {
                    "model": model_name,
                    "status": "skipped_missing_features",
                    "missing_features": ",".join(missing),
                    "n": len(data),
                    "rmse": np.nan,
                    "mae": np.nan,
                    "r2": np.nan,
                }
            )
            continue

        X = data.loc[:, feature_names]
        predictions = np.full(len(data), np.nan, dtype=float)

        for train_idx, test_idx in cv.split(X, y, groups=groups):
            model = _estimator(config.ridge_alpha)
            model.fit(X.iloc[train_idx], y[train_idx])
            predictions[test_idx] = model.predict(X.iloc[test_idx])

        valid = np.isfinite(predictions) & np.isfinite(y)
        results.append(
            {
                "model": model_name,
                "status": "ok",
                "missing_features": "",
                "n": int(valid.sum()),
                "rmse": float(np.sqrt(mean_squared_error(y[valid], predictions[valid]))),
                "mae": float(mean_absolute_error(y[valid], predictions[valid])),
                "r2": float(r2_score(y[valid], predictions[valid])),
            }
        )

    table = pd.DataFrame(results)
    ok = table["status"] == "ok"
    table.loc[ok, "rank_rmse"] = table.loc[ok, "rmse"].rank(method="min", ascending=True)
    return table.sort_values(["status", "rmse"], na_position="last").reset_index(drop=True)
