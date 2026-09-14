# Trident Learnability Transfer

Research programme for testing whether cognitive training transfers not only as **performance gain**, but also as **learnability**: the rate and dynamics of acquiring, reorganising, recovering and generalising a cognitive operation.

## Two core prospective proposals

1. **Plateau-triggered construct breakthrough:** train a cognitive construct on a stable backbone until genuine flattening, introduce a bounded wrapper perturbation, then return to the backbone and test whether the original performance frontier recovers and extends.
2. **Cross-construct learnability transfer:** successful learning of construct A may increase the subsequent learning rate or alter the state-transition dynamics of construct B when A provides an enabling or rate-limiting constraint.

The prospective Trident horizontal cycle is:

```text
BUILD → FLATTEN → PERTURB → ADAPT → RETURN → RECOVER → BREAKTHROUGH? → RESTABILISE
```

Post-return performance is treated multidimensionally rather than as accuracy alone. Candidate outcomes include capacity/frontier level, accuracy at matched demand, interference robustness, response efficiency, stability, perturbation cost, return recovery, frontier extension, held-out wrapper transfer and delayed re-entry.

## Transfer mechanism tournament

The existing-data phase does not assume the prospective hypotheses are correct. Instead it compares competing mechanisms M0–M11:

- M0 task-specific fluency
- M1 surface-invariant operation
- M2 construct strengthening
- M3 learning-dynamics transfer
- M4 plateau/reorganisation
- M5 breadth/variation
- M6 general learnability
- M7 directed facilitation
- M8 reciprocal mutualism
- M9 bottleneck release
- M10 competition/interference
- M11 state-gated transfer

The aim is to discover which longitudinal signatures best predict within-construct portability and later learning in other constructs, then use those results to choose the most defensible prospective Synergy IQ training regime.

## Dataset strategy

**COGITO** remains the preferred controlled longitudinal dataset. The programme does not depend on COGITO access, however. The strongest open backup is the Steyvers–Schafer Lumosity dataset: 36,297 users learning 51 cognitive-training tasks with gameplay-level performance trajectories. A smaller 20-session single/dual-task dataset indexed by OpenCogData is the rapid pipeline-development dataset. COG-BCI and visuomotor-rotation datasets are reserved for nuisance-state/EEG and state-transition validation respectively.

See `docs/PLAN_B_DATASETS.md` and `configs/datasets.yaml`.

## Code status

The first analysis layer is now implemented in `src/trident_transfer/`:

- `schema.py` — canonical long-format data contract;
- `features.py` — interpretable task learning features, including early/late slopes, asymptote proxy, variability, plateau timing and post-plateau change;
- `synthetic.py` — known-mechanism synthetic data for pipeline checks;
- `tournament.py` — participant-isolated M0–M5 predictive tournament;
- `cross_construct.py` — windowed learning velocities and directional A→B / B→A panels for later M6–M11 analyses.

A synthetic end-to-end demonstration is in `scripts/demo_synthetic_pipeline.py`; initial checks are in `tests/test_pipeline.py`.

To install locally:

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -e ".[dev]"
pytest -q
python scripts/demo_synthetic_pipeline.py
```

## Project documents

- `docs/THEORETICAL_PROPOSAL.md`
- `docs/HYPOTHESES.md`
- `docs/TRANSFER_MODEL_TOURNAMENT.md`
- `docs/DATASET_STRATEGY.md`
- `docs/PLAN_B_DATASETS.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `studies/01_construct_transfer/protocol.md`
- `studies/02_cross_construct_learnability/protocol.md`
- `studies/03_learning_state_detection/protocol.md`

## Current status

Phase 0 theory/model contract is established and the initial Phase 1 code scaffold is in place. Immediate next step: ingest the open Lumosity or Naefgen longitudinal dataset into the canonical schema and run the first real-data learning-curve diagnostics while the COGITO request proceeds.
