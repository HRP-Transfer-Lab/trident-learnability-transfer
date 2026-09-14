"""Run the M0-M5 construct-transfer pipeline on synthetic data.

Usage from repository root:
    python scripts/demo_synthetic_pipeline.py
"""

from trident_transfer.features import add_construct_context, extract_learning_features
from trident_transfer.synthetic import SyntheticConfig, simulate_longitudinal_data, simulate_transfer_outcomes
from trident_transfer.tournament import TournamentConfig, evaluate_construct_tournament


def main() -> None:
    observations = simulate_longitudinal_data(
        SyntheticConfig(n_participants=120, n_sessions=40, seed=42)
    )
    features = add_construct_context(extract_learning_features(observations))

    # Generate a known learning-dynamics transfer mechanism. The tournament should
    # generally favour models containing dynamic features, subject to finite-sample noise.
    outcomes = simulate_transfer_outcomes(features, mechanism="M3", seed=123)
    results = evaluate_construct_tournament(
        features,
        outcomes,
        config=TournamentConfig(n_splits=5),
    )

    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
