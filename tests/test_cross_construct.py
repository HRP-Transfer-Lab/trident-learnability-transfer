import numpy as np

from trident_transfer.cross_construct import make_directional_panel, windowed_construct_velocity
from trident_transfer.synthetic import SyntheticConfig, simulate_longitudinal_data


def test_directional_panel_has_lagged_target_velocity():
    observations = simulate_longitudinal_data(
        SyntheticConfig(n_participants=12, n_sessions=20, tasks_per_construct=2, seed=31)
    )
    velocities = windowed_construct_velocity(observations, window_size=5)
    panel = make_directional_panel(velocities, "perceptual_speed", "working_memory")

    assert not panel.empty
    assert {
        "source_velocity_t",
        "target_velocity_t",
        "target_velocity_t1",
        "source_performance_t",
        "target_performance_t",
    }.issubset(panel.columns)

    # Last window for each participant has no t+1 target by construction.
    last_rows = panel.groupby("participant_id", observed=True).tail(1)
    assert last_rows["target_velocity_t1"].isna().all()
    assert np.isfinite(panel["source_velocity_t"].dropna()).all()
