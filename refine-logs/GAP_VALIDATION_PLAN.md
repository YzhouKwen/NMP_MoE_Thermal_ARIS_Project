# Gap Validation Plan — NMP/MoE Expert Placement Thermal Disadvantage and Thermal Risk

**Date**: 2026-06-24  
**Stage**: pre-method validation gate  
**Purpose**: verify the paper premise before committing to a TACE-first method paper  
**Execution mode**: ARIS-compatible `/run-experiment` plan  
**Relationship to current plan**: this plan runs **before** the current TACE-specific `EXPERIMENT_PLAN.md` becomes authoritative

## Why this plan exists

The current paper premise is not yet proven:

> Existing NMP-oriented MoE expert placements, although designed for access, communication, throughput, or load balance, may be thermally suboptimal on 3D-stacked NMP; in some regimes, that suboptimality may further escalate into thermally unsafe or performance-degrading behavior.

This premise must be tested directly before treating TACE as the primary contribution.

## Decision Policy

This plan is a **hypothesis gate**.

- If the thermal disadvantage is **clear and repeatable**, proceed to TACE method validation.
- If the thermal disadvantage is **weak, inconsistent, or negligible**, do **not** over-commit to a TACE-first paper. Reframe as characterization-first or stop the line.
- If the thermal disadvantage is clear but thermal risk is only conditional, the paper may still be viable, but more likely as characterization-first or conditional-method framing.

## Primary Hypothesis

**H1.** Current or nearby NMP-oriented expert placement strategies are **thermally disadvantaged** on 3D-stacked NMP relative to better thermal references.

Operational meaning:

- At least one realistic NMP-native placement heuristic shows repeatable thermal disadvantage:
  - higher peak temperature,
  - more concentrated hotspots,
  - longer time-above-threshold,
  - or worse bank-level thermal skew.

## Secondary Hypothesis

**H2.** That thermal disadvantage escalates into **thermal risk or operating degradation** in at least some realistic regimes.

Operational meaning:

- At least one realistic NMP-native placement heuristic causes threshold violations, prolonged dangerous-temperature residency, throttle pressure, or thermal-cap throughput degradation on some task families or operating points.

## Tertiary Hypothesis

**H3.** The observed thermal disadvantage / thermal risk is not explained away by token balance alone.

Operational meaning:

- Token-balanced routing can still yield skewed bank activity and elevated thermal stress.

## Non-Goals

- Do **not** optimize or defend TACE yet.
- Do **not** spend effort on large QAP solver engineering.
- Do **not** make TACG-port the paper centerpiece at this stage.
- Do **not** promise a new placement method unless H1 is supported.

## Placement Baselines to Test

These are the **primary** baselines for this gap study:

1. **Random**
   - Uniform random expert-to-site assignment
   - Purpose: lower-bound sanity baseline

2. **Even-odd / spread placement**
   - Proxy for A3D-MoE-style rule-based spreading
   - Purpose: access-aware simple static placement

3. **Access-likelihood tiering**
   - Proxy for Stratum-style access/use-rate-driven tier placement
   - Purpose: NMP-native performance-oriented placement

4. **Frequency-only placement**
   - High-rate experts placed on cooler/favored sites, no pairwise co-burst logic
   - Purpose: thermal-blind frequency-aware placement

Optional transferred control:

5. **TACG-port**
   - Only as a communication-centric opposite-sign control
   - Not the load-bearing baseline for this gap study

## Shared Evaluation Inputs

- **Trace source**: Patterns Behind Chaos public MoE traces
- **Task families**: chat / code / math / multilingual (subject to availability)
- **Substrate**: same 3D-NMP bank/tier model across all baselines
- **Power model**: same `q_e` derivation across all baselines
- **Thermal backbone**: CoMeT primary, Voxel optional cross-check

## Core Metrics

Mandatory:

- `peak_temperature`
- `top_k_hottest_banks`
- `bank_activity_gini`
- `time_above_threshold`
- `thermal_violation_count`

Strongly preferred:

- `throughput_under_Tcap`
- `throttle_event_count`
- `avg_tpot`

Auxiliary:

- `token_gini`
- `expert_activity_gini`
- hotspot location overlap across families

## Success Thresholds for H1

H1 is considered **supported** if at least one NMP-native placement heuristic shows, on **>= 3/4 task families**, at least one of:

- `>= 2.0°C` peak-temperature disadvantage relative to the coldest credible reference
- clearly elevated `time_above_threshold`
- clearly more concentrated hotspot pattern
- clearly worse bank-level thermal skew despite similar or better token balance

H1 is considered **strongly supported** if multiple NMP-native baselines show such disadvantage and the effect is repeatable across model/task families.

## Success Thresholds for H2

H2 is considered **supported** if at least one NMP-native placement heuristic shows, on **>= 2/4 task families** or under a realistic subset of operating points:

- `peak_temperature >= T_cap`
- non-trivial `thermal_violation_count`
- clearly elevated `time_above_threshold`
- clearly worse `throughput_under_Tcap`
- clearly more `throttle_event_count`

H2 is considered **strongly supported** if such unsafe or degraded behavior is repeatable across several families and not confined to a single outlier condition.

## Success Thresholds for H3

H3 is considered supported if, on **>= 3/4 task families**:

- token Gini is low or improved under balancing,
- yet bank-activity Gini remains high,
- and thermal disadvantage / risk metrics do not improve proportionally.

## Experiment Blocks

### G0 — Pre-flight inventory and simulator anchor
- **Purpose**: ensure the gap study is runnable
- **Checks**:
  - trace coverage matrix by `(model, task_family)`
  - CoMeT smoke-test on a simple power map
  - optional Voxel smoke-test
  - substrate/power-model plumbing complete enough to compare fixed placements
- **Outputs**:
  - coverage table
  - simulator anchor note
  - environment summary
- **Gate**:
  - if traces are too sparse or simulator path is broken, stop here and repair infrastructure first

### G1 — Static thermal-disadvantage comparison of NMP-native placements
- **Purpose**: test H1 directly
- **Method**:
  - for each task family, replay the same traces under the baseline placement set
  - compute `peak_temperature`, `top_k_hottest_banks`, `bank_activity_gini`, `time_above_threshold`, `thermal_violation_count`
- **Primary output**:
  - per-family thermal-disadvantage comparison table
  - ranking of placements by thermal quality
- **Gate**:
  - if no consistent thermal disadvantage appears, do not proceed to TACE-first framing

### G2 — Token-balance vs thermal-balance check
- **Purpose**: test H3
- **Method**:
  - compare vanilla, LPR-balanced, and aux-loss-free-balanced routing
  - under fixed reference placement(s), measure token Gini, bank-activity Gini, and thermal metrics
- **Primary output**:
  - one compact Section-4-style figure showing that routing balance does not imply thermal balance
- **Gate**:
  - if token balance already fixes thermal behavior, the motivation for a new placement is weaker

### G3 — Thermal-risk / thermal-cap serving sensitivity
- **Purpose**: test whether thermal disadvantage escalates into operational risk (H2)
- **Method**:
  - take the thermally best and worst NMP-native placements from G1
  - run a thermal-cap serving loop with fixed `T_cap`
  - compare throughput, throttle events, average TPOT
- **Primary output**:
  - whether thermal disadvantage translates into serving consequences
- **Gate**:
  - if thermal differences never affect serving behavior, the paper may still remain characterization-first rather than method-first

### G4 — Decision gate
- **Purpose**: convert evidence into paper direction
- **Possible outcomes**:
  1. **Proceed to TACE** — H1 clearly supported, and optionally strengthened by H2/H3
  2. **Characterization-first paper** — H1 supported, but H2 weak or incomplete
  3. **Stop / re-scope** — H1 not supported strongly enough

## Recommended Run Order

1. `G0`
2. `G1`
3. `G2`
4. `G3`
5. `G4`

## Mapping to ARIS `/run-experiment`

This plan is compatible with ARIS `/run-experiment` if Claude treats each `G*` item as an experiment block, exactly the same way the current TACE plan uses `B*` blocks.

Recommended execution pattern:

- `/run-experiment G0`
- `/run-experiment G1`
- `/run-experiment G2`
- `/run-experiment G3`

After each block:

- append results to `GAP_VALIDATION_RESULTS.md`
- update the verdict in `GAP_VALIDATION_SUMMARY.md`

## What this plan should decide

At the end of this plan, the project must answer only:

1. Do current NMP-oriented expert placements create a real thermal disadvantage?
2. Which placement heuristic is thermally worst, and why?
3. Does that disadvantage escalate into thermal risk or thermal-cap degradation?
4. Is the evidence strong enough to justify a new thermal-aware placement paper?
5. Should TACE remain the next step, or should the paper be reframed?
