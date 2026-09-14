# Study 01 — Construct Transfer

## Question

Do learning dynamics on a trained task predict improvement on an untrained task that preserves the central operation while changing the surface/material?

## Candidate COGITO pairs

- spatial 3-back → numerical 3-back;
- numerical memory updating → spatial memory updating;
- alpha span → animal span.

## Primary predictors

For each trained task estimate early learning slope, nonlinear rate, flattening point, asymptotic performance and residual variability.

## Primary outcome

Pre-to-post change on the untrained counterpart, standardised within task.

## Core model

`transfer_gain ~ baseline_transfer + final_trained_score + learning_dynamics + covariates`

The key test is whether learning-dynamic parameters improve prediction beyond baseline and final trained performance.

## Robustness

- compare younger and older samples where available;
- bootstrap person-level estimates;
- test reasonable alternative learning-curve forms;
- repeat analyses across all three task pairs;
- report null and inconsistent results explicitly.

## Interpretation

A positive result supports construct portability associated with how learning unfolds. It is not a full test of the prospective Anchor–Perturb–Return intervention because perturbation and return were not experimentally scheduled in COGITO.
