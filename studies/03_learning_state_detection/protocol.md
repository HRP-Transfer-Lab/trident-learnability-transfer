# Study 03 — Learning-State Modelling

## Aim

Explore whether longitudinal task-performance features can identify recurring phases of skill acquisition.

## Candidate phases

```text
SEARCH
TUNE
SATURATED
REORGANISE
RECOVER
STABLE
```

These are descriptive behavioural labels rather than direct neural measurements.

## Candidate features

Use accuracy or d-prime, median reaction time, robust RT variability, omission and false-alarm rates, recent learning slope, error clustering and post-error adjustment where available.

## Modelling order

1. simple rule-based segmentation;
2. probabilistic phase scores;
3. hidden Markov or hidden semi-Markov models;
4. switching state-space models only if justified by predictive performance.

## Validation

Compare out-of-sample prediction of later performance, transfer and recovery against simpler models using current score and session number alone.

## Later prospective use

Results can inform future adaptive training experiments in which task difficulty and wrapper changes are selected from recent performance dynamics rather than from a single score threshold.
