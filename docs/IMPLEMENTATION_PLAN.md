# Implementation Plan

## Phase 0 — project contract

- Freeze the prospective claims and competing retrospective mechanism models.
- Record dataset provenance and access conditions.
- Define a common long-format schema for participant, task, construct, session, block, trial, response, accuracy and RT.
- Predefine a model-comparison contract emphasising participant-isolated held-out prediction where practical.

The model tournament is specified in `docs/TRANSFER_MODEL_TOURNAMENT.md`.

## Phase 1 — canonical learning curves

For each task, fit simple and nonlinear mixed-effects learning curves. Extract person-level estimates of:

- early learning velocity;
- late learning velocity;
- curve shape;
- flattening point;
- asymptote;
- residual variability;
- candidate change-points;
- post-change recovery or renewed learning.

Compare alternative window sizes and require reasonable parameter stability before using derived measures downstream.

These features provide the basis for M0–M4 and later state models.

## Phase 2 — within-operation construct portability tournament

For trained/untrained same-operation task pairs, compare:

- **M0 task-specific fluency** — baseline plus final trained-task performance;
- **M1 surface-invariant operation** — source-task learning predicts changed-surface transfer;
- **M3 learning-dynamics transfer** — trajectory features add predictive value;
- **M4 plateau/reorganisation** — plateau and renewed-learning features add predictive value.

Primary question: do trajectory features explain held-out transfer beyond baseline score, total gain and endpoint performance?

For COGITO, priority pairs are spatial 3-back to numerical 3-back, numerical updating to spatial updating, and alpha span to animal span.

## Phase 3 — breadth and latent construct strengthening

Compare:

- **M2 construct strengthening** — coordinated change across several tasks predicts a latent construct outcome;
- **M5 breadth/variation** — balanced improvement across task forms predicts transfer better than narrow specialisation.

Construct task-breadth indices and latent construct scores without allowing the transfer outcome itself to leak into predictors.

## Phase 4 — common learnability

Estimate whether learning parameters share a reliable common component across tasks and constructs.

Compare models containing construct-specific learning parameters with **M6 general learnability**.

Candidate construct families include working memory, perceptual speed/evidence processing and episodic memory.

The common factor is a competing explanation, not automatically evidence for causal cross-construct transfer.

## Phase 5 — cross-construct temporal tournament

Aggregate sessions into prespecified windows and estimate local learning velocity for each construct.

Base prospective model:

`delta_B(t+1) ~ delta_B(t) + delta_A(t) + time + person effects`

Compare:

- **M7 directed facilitation** — A predicts later acceleration in B;
- **M8 reciprocal mutualism** — A predicts B and B predicts A;
- **M9 bottleneck release** — B accelerates after A crosses a threshold/change-point;
- **M10 competition/interference** — rapid A learning predicts slower subsequent B learning.

All models should be rerun with general learnability covariates or latent factors where feasible.

The reverse temporal direction is compulsory whenever directional claims are made.

## Phase 6 — plateau and breakthrough analogues

Search for naturally occurring trajectories of the form:

`improvement → flattening → renewed improvement`

For task A, test whether renewed learning after a plateau is preceded by:

- improvement in another task representing the same construct;
- broader improvement across different task forms;
- improvement in another construct;
- no systematic change elsewhere.

This is an observational analogue of the prospective Anchor–Perturb–Return breakthrough hypothesis, not a causal test of wrapper perturbation.

## Phase 7 — latent learning states

Only after the simpler models are stable, compare rule-based states with HMM, hidden semi-Markov or switching state-space models.

Candidate behavioural states are:

`SEARCH → TUNE → SATURATED → REORGANISE → RECOVER → STABLE`

Evaluate **M11 state-gated transfer** by asking whether state identity or state transitions improve prediction of later portability or cross-construct acceleration beyond continuous learning-curve features.

## Phase 8 — model tournament scoring

For each stage, compare models using participant-isolated held-out prediction where practical.

Report:

- predictive error or held-out likelihood appropriate to the model;
- calibration where probabilistic state outputs are used;
- bootstrap or resampling stability;
- parameter uncertainty;
- transport across task pairs and, where available, age groups;
- incremental predictive value over simpler baselines.

Do not select a transfer mechanism solely from the smallest p-value.

## Phase 9 — prospective Synergy IQ construct-transfer study

Use the retrospective tournament to choose the most defensible causal training comparison.

Core experimental contrast:

`backbone-only continued practice`

versus

`plateau-triggered Anchor–Perturb–Return`

Match training exposure as closely as possible.

Primary post-return outcomes should reflect the multidimensional Synergy IQ performance concept rather than accuracy alone, including where available:

- capacity/frontier level;
- accuracy at matched demand;
- interference or lure robustness;
- response efficiency;
- performance stability;
- perturbation cost;
- return-to-frontier recovery;
- frontier extension;
- held-out wrapper transfer;
- delayed re-entry.

## Phase 10 — prospective cross-construct learnability study

If the construct-transfer regime succeeds, test whether it changes subsequent learning of a second construct.

The key outcome is the learning trajectory of construct B, not merely its post-test score.

Compare early learning velocity, time to plateau, probability/timing of state transitions and final frontier between participants receiving successful construct-A transfer training and an appropriate control regime.

This phase is the causal test of the stronger proposal:

`successful construct learning in A → increased learnability of B`.
