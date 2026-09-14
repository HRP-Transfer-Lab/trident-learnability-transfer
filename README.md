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

## Initial empirical programme

The first phase uses existing intensive longitudinal datasets. **COGITO** is the primary target; open repeated-session datasets will be used to develop the pipeline while access is arranged.

Start here:

- `docs/THEORETICAL_PROPOSAL.md`
- `docs/HYPOTHESES.md`
- `docs/TRANSFER_MODEL_TOURNAMENT.md`
- `docs/DATASET_STRATEGY.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `studies/01_construct_transfer/protocol.md`
- `studies/02_cross_construct_learnability/protocol.md`
- `studies/03_learning_state_detection/protocol.md`

## Current status

Phase 0: theory, competing mechanisms, dataset strategy and analysis contract established. Next step: implement the canonical learning-curve pipeline and begin the M0–M5 within-construct model tournament on an accessible longitudinal development dataset while COGITO access is arranged.
