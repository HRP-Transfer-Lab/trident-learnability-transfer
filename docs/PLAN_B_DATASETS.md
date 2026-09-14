# Plan B and Parallel Datasets

The primary target remains COGITO because it combines intensive repeated practice, multiple cognitive constructs, pre/post transfer measures, passive controls, and follow-up. However, the research programme must not depend on one restricted dataset.

## Priority 1 — Open Lumosity learning trajectories (Steyvers & Schafer)

**Status:** fully open research data and code via OSF (project linked from the published paper).

**Scale:** 36,297 users learning 51 cognitive-training tasks.

**Resolution:** gameplay-level performance scores across repeated plays. The raw data do not contain the individual decisions made within each gameplay.

**Why it is highly relevant:**

- directly supports estimation of individual learning curves across many tasks;
- permits tests of a domain-general learnability factor versus task/domain-specific factors;
- permits prediction of an unobserved task-learning trajectory from trajectories on other tasks;
- is well suited to M0–M3, M5–M9 and parts of M11;
- allows a large-sample test of whether earlier improvement in one task/domain predicts later acceleration on another;
- can be used immediately while COGITO access is pending.

**Key limitation:** this is naturalistic training rather than an experimentally controlled wrapper-transfer protocol. Game scheduling is self-selected/algorithmic, and gameplay-level scores do not provide trial-level error topologies such as lure false alarms.

**Primary role in this project:** open-data development dataset and large-scale test of general versus cross-task learnability.

## Priority 2 — Naefgen et al. 2023 single/dual-task longitudinal dataset (OpenCogData)

**Status:** public trial-level dataset indexed by OpenCogData.

**Scale:** 58 participants across 20 sessions.

**Structure:** two simple component tasks performed in single-task and dual-task conditions.

**Why useful:**

- genuine repeated within-person performance;
- useful for testing the canonical schema, local learning velocities, session-to-session coupling and state-change detection;
- single-to-dual task relations provide a constrained test of shared-capacity and coupling models;
- sufficiently small to use as a rapid pipeline-development and unit-test dataset.

**Limitation:** narrow cognitive scope; not a strong dataset for broad cross-construct transfer.

## Priority 3 — COG-BCI

**Status:** open on Zenodo.

**Scale:** 29 participants, three sessions, four cognitive tasks plus resting-state recordings; over 100 hours of EEG.

**Tasks:** N-back, Flanker, psychomotor vigilance task (PVT), and MATB-II multitasking.

**Why useful:**

- behavioural plus EEG data;
- can test whether behavioural states attributed to learning are separable from workload, vigilance, conflict and fatigue;
- useful for developing nuisance-state classifiers and later EEG validation.

**Limitation:** only three sessions, so it is not a primary dataset for long-run learning curves or transfer.

## Priority 4 — OpenNeuro visuomotor-rotation datasets

Use a well-documented rotation/adaptation dataset as a **ground-truth transition benchmark**. The model should be able to recover known baseline → perturbation → adaptation → washout transitions before subtle learning-state claims are trusted.

This is not a cognitive-construct transfer dataset. Its role is validation of change-point/state-detection methods.

## Priority 5 — Dallas Lifespan Brain Study (OpenNeuro ds004856)

This dataset includes repeated waves with broad batteries covering processing speed, working memory, episodic memory, reasoning, vocabulary and verbal fluency.

**Role:** replication of broad construct covariance and longitudinal change models.

**Limitation:** waves are separated by long intervals rather than intensive skill-learning sessions, so it cannot replace COGITO for learning-state analyses.

## Dataset hierarchy

The programme should use datasets for what they are structurally able to test rather than treating all repeated measures as equivalent:

1. **COGITO:** intensive construct transfer + within-person learning dynamics + pre/post transfer.
2. **Lumosity 51-task dataset:** large-scale general/cross-task learnability and learning-trajectory prediction.
3. **Naefgen 20-session dataset:** rapid open pipeline development and within-person coupling.
4. **COG-BCI:** nuisance-state and EEG validation.
5. **Visuomotor rotation:** ground-truth state-transition validation.
6. **Dallas Lifespan:** broad longitudinal construct replication.

## Decision rule if COGITO access is not granted

The main paper can still proceed as a two-dataset project:

- **Study 1:** Lumosity — M0–M9 tournament on 36k+ users and 51 tasks, with participant-isolated held-out prediction.
- **Study 2:** Naefgen — intensive 20-session replication of within-person coupling and state-sensitive models.

The prospective Synergy IQ experiment would then provide the first causal test of plateau-triggered Anchor–Perturb–Return construct transfer.
