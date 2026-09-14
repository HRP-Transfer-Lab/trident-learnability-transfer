import numpy as np

from trident_transfer.features import add_construct_context, extract_learning_features
from trident_transfer.schema import validate_longitudinal_frame
from trident_transfer.synthetic import SyntheticConfig, simulate_longitudinal_data, simulate_transfer_outcomes
from trident_transfer.tournament import evaluate_construct_tournament


def test_canonical_synthetic_pipeline_runs():
    observations = simulate_longitudinal_data(
        SyntheticConfig(n_participants=24, n_sessions=16, observations_per_session=2, seed=7)
    )
    validated = validate_longitudinal_frame(observations)
    assert not validated.empty
    assert validated["participant_id"].nunique() == 24

    features = add_construct_context(
        extract_learning_features(
            validated,
            plateau_window=4,
            plateau_slope_tolerance=0.01,
        )
    )
    assert {"early_slope", "plateau_session", "construct_other_gain"}.issubset(features.columns)

    outcomes = simulate_transfer_outcomes(features, mechanism="M3", seed=11)
    results = evaluate_construct_tournament(features, outcomes)

    ok = results[results["status"] == "ok"]
    assert len(ok) == 6
    assert np.isfinite(ok["rmse"]).all()
    assert np.isfinite(ok["mae"]).all()


def test_null_and_dynamic_transfer_generators_differ():
    observations = simulate_longitudinal_data(
        SyntheticConfig(n_participants=20, n_sessions=15, seed=21)
    )
    features = add_construct_context(
        extract_learning_features(observations, plateau_window=4, plateau_slope_tolerance=0.01)
    )
    m0 = simulate_transfer_outcomes(features, mechanism="M0", noise_sd=0.0, seed=1)
    m3 = simulate_transfer_outcomes(features, mechanism="M3", noise_sd=0.0, seed=1)
    assert not np.allclose(m0["transfer_gain"], m3["transfer_gain"])
