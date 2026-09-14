# Implementation Plan

## Phase 0 — project contract

- Freeze the theoretical claims and primary hypotheses.
- Record dataset provenance and access conditions.
- Define a common long-format schema for participant, task, session, block, trial, response, accuracy and RT.

## Phase 1 — learning curves

For each task, fit simple and nonlinear mixed-effects learning curves. Extract person-level estimates of early learning velocity, curve shape, flattening point, asymptote and residual variability.

Compare alternative window sizes and require reasonable parameter stability before using derived measures downstream.

## Phase 2 — construct portability

For trained/untrained same-operation task pairs, predict transfer gain from learning-dynamic features while controlling baseline and trained-task endpoint performance.

Primary question: do trajectory features add explanatory value beyond final score?

## Phase 3 — cross-construct learnability

Aggregate sessions into prespecified windows. Estimate local learning velocity for each construct and fit prospective models of the form:

`delta_B(t+1) ~ delta_B(t) + delta_A(t) + time + person effects`

Fit the reverse direction as a compulsory comparison.

## Phase 4 — common learnability

Estimate whether learning parameters share a reliable common component across tasks/constructs, while retaining construct-specific variance.

## Phase 5 — latent states

Only after the simpler models are stable, compare rule-based states with HMM, hidden semi-Markov or switching state-space models. Candidate behavioural states are SEARCH, TUNE, SATURATED, REORGANISE, RECOVER and STABLE.

## Phase 6 — prospective app study

Use the retrospective results to design a controlled Anchor–Perturb–Return experiment in a training app. The controller should select difficulty or wrapper changes from performance evidence rather than from score thresholds alone.
