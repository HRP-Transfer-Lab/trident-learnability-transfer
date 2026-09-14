# Hypotheses

This project separates the **prospective Trident training hypotheses** from the **retrospective mechanism models** that can be compared using existing longitudinal datasets.

## P1 — Plateau-triggered construct breakthrough

Training a construct on a stable backbone until genuine flattening, followed by a bounded wrapper perturbation and return to the backbone, may produce renewed improvement or a breakthrough in the original performance frontier.

The post-return effect may be expressed through capacity, accuracy, robustness to interference/lures, response efficiency, reduced variability, or a composite performance measure rather than accuracy alone.

Canonical sequence:

`BUILD → FLATTEN → PERTURB → ADAPT → RETURN → RECOVER → BREAKTHROUGH? → RESTABILISE`

## P2 — Cross-construct learnability transfer

Successful learning of construct A may increase the subsequent learning rate or alter the state-transition dynamics of construct B when A provides an enabling or rate-limiting constraint.

The key temporal claim is:

`earlier change(A) predicts later learning velocity or transition dynamics in B`

rather than merely:

`change(A) correlates with change(B)`

Reverse-direction models must always be fitted.

## Retrospective mechanism hypotheses

The existing-data programme compares a model tournament rather than assuming P1 or P2 are already correct.

- **M0 Task-specific fluency:** practice effects remain largely task-bound.
- **M1 Surface-invariant operation:** improvement transfers across changed task material while preserving the operation.
- **M2 Construct strengthening:** coordinated improvement reflects a broader latent construct.
- **M3 Learning-dynamics transfer:** trajectory properties predict transfer above endpoint performance.
- **M4 Plateau/reorganisation:** plateaus, change-points or renewed learning predict portability.
- **M5 Breadth/variation:** distributed improvement across task forms predicts transfer better than narrow specialisation.
- **M6 General learnability:** a common person-level learning component explains covariance across constructs.
- **M7 Directed facilitation:** earlier improvement in A predicts later learning acceleration in B.
- **M8 Reciprocal mutualism:** A and B prospectively facilitate one another beyond common learnability.
- **M9 Bottleneck release:** B accelerates after A crosses a threshold or undergoes a meaningful transition.
- **M10 Competition/interference:** rapid learning in A temporarily or systematically slows B.
- **M11 State-gated transfer:** transfer depends on latent learning state or state transitions, not score alone.

Full definitions, predictions and model comparisons are in `docs/TRANSFER_MODEL_TOURNAMENT.md`.

## Core empirical tests

### H1 — Construct portability

Learning-curve parameters from a trained task predict improvement on an untrained task that preserves the central cognitive operation while changing the surface or material.

Primary test: do learning dynamics explain transfer beyond baseline score, total gain and final trained-task performance?

### H2 — Common versus construct-specific learnability

Person-level learning parameters may covary across tasks and constructs, supporting a common learnability component in addition to construct-specific effects.

Candidate parameters include early slope, nonlinear rate, flattening point, asymptote, residual variability and change-point/recovery features.

### H3 — Cross-construct facilitation

Earlier improvement in construct A predicts greater subsequent learning velocity in construct B after controlling prior B trajectory, session/time and person-level differences.

Directed, reciprocal, threshold and interference alternatives must be compared.

### H4 — State-sensitive transfer

When sufficient longitudinal resolution exists, transfer should be better predicted by where a learner is in the acquisition trajectory than by current score alone.

## Falsification checks

The stronger Trident claims are weakened if:

- transfer is predicted no better by learning dynamics than by endpoint performance;
- apparent cross-construct effects disappear after modelling general learnability;
- only concurrent correlations appear with no prospective effects;
- reverse-direction models fit equally well when directional claims are made;
- effects depend on one task only and fail to replicate across related tasks or samples;
- plateau/change-point models add no predictive value over smooth learning curves;
- interference or task-specific fluency models outperform facilitation models.
