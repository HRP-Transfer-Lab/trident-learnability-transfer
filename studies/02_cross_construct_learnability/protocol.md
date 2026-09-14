# Study 02 — Cross-Construct Learnability

## Question

Does earlier improvement in one construct predict faster subsequent learning in another construct?

## Initial target

Start with perceptual/evidence-processing learning and working-memory learning in the same participants. Use episodic-memory learning as a specificity comparator.

## Windowed representation

Aggregate repeated sessions into prespecified windows, initially 5-session and 10-session windows. For each construct derive a latent or composite performance estimate and local learning velocity.

## Primary prospective model

`delta_WM(t+1) ~ delta_WM(t) + delta_PS(t) + time + person effects`

Fit the reverse direction:

`delta_PS(t+1) ~ delta_PS(t) + delta_WM(t) + time + person effects`

## Interpretation logic

- both directions positive: possible common learning process or reciprocal coupling;
- PS → WM stronger: candidate directional facilitation;
- contemporaneous association only: shared plasticity or common-cause explanation remains more plausible;
- no reliable coupling: reject the strong transfer-of-learnability claim for this pair.

## Robustness

Compare window sizes, standardisation schemes and task-composite definitions. Use person-level resampling and report the sensitivity of directional estimates to modelling choices.
