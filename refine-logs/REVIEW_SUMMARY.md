# Review Summary — TACE

**Date**: 2026-06-24
**Source**: GPT-5.4 critical review (Phase 4, 2026-06-23), trace at `.aris/traces/idea-creator/2026-06-23_run01/review.md`
**Verdict carried forward**: GO-WITH-CHANGES — bundled paper survives if and only if the 12 mandatory pre-submission changes are addressed.

## Reviewer's Core Concerns (paraphrased)

1. **Eigenvalue surrogate is wrong physics.** `min Σ_t λ_max(P(t))` is not peak T. Replace with a direct prediction (`max_t T(t)` or thresholded equivalent) computed from the same RC/Green's-function model the rest of the paper relies on.
2. **The paper must distinguish NMP-native baselines from transferred controls.** TACG is useful because it uses the same co-activation signal in the opposite direction, but it is not a published 3D-NMP MoE placement baseline. The paper should first prove a thermal gap in current NMP-oriented placements, then use TACG-port as a same-substrate transferred control.
3. **Atlas as a standalone paper is weak.** Public trace + open simulator = "profiling + replay." Inside a bundled paper, it becomes the empirical justification for TACE's term structure — that is its proper home.
4. **Static placement attracts a drift attack.** A reviewer will ask "what happens when the workload distribution shifts?" Pre-empt with explicit train-on-X / test-on-Y folds.
5. **Thermal-only wins are insufficient.** Peak T reduction without TPOT, throughput, and throttle-event evidence is reviewer-bait. The paper must operate the system under a thermal cap and report end-to-end serving deltas.
6. **HC-MoE is a different paper.** Different lever (scheduling), different inference-semantics risk surface, different stability proof obligation. Bundling would compress both contributions below the venue bar.
7. **I7 (Cool-Tier Shadow Experts) is overbuilt.** Hardware answer to a software-solvable problem; overlaps CRAFT + Tasa; kill.

## Each Concern → TACE's Response

| Reviewer concern | TACE's response (where in FINAL_PROPOSAL.md) |
|------------------|-----------------------------------------------|
| 1. Eigenvalue surrogate | §5.3 Form A (direct surrogate inside QAP) + Form B (CoMeT verification at acceptance). §10 A5 ablates direct-T vs λ_max so the choice is empirically defended. |
| 2. NMP-native baselines first, TACG-port second | §6 reframes baseline strategy: A3D/Stratum/NeuroTAP-style baselines are the primary thermal-gap targets; TACG-port is retained as a faithful transferred control, not the sole headline baseline. |
| 3. Atlas as Section 4 | §2/§3/§9 C1 — Atlas is not branded as a separate contribution; its job is to derive the term structure that §5 uses. |
| 4. Drift attack | Q7 train-on-3/test-on-1 4-fold protocol. §11 reviewer-attack row pre-declares the attack and its mitigation. |
| 5. E2E serving metrics | §9 C3 — TPOT, throughput, throttle events under thermal cap. Promoted to the third (not optional) claim. |
| 6. HC-MoE bundling | Demoted to separate submission. §4 rejected complexity list. Will be picked up only after TACE results unlock the substrate. |
| 7. I7 kill | Already executed in Phase 4; §4 rejected complexity list confirms it stays dead. |

## Concerns Not Yet Addressed by Method Alone (handed to experiment plan)

| Concern | Where in EXPERIMENT_PLAN.md |
|---------|------------------------------|
| Cross-simulator credibility | B7 — CoMeT primary, Voxel cross-check on 32×8 subset, predeclared agreement criterion |
| Parameter sweep coverage | B8 — anisotropy ratio, ambient T, stack height, burstiness, threshold; ≥ 3 points per axis |
| Trace-data inventory risk | B0 pre-flight before any expensive run |
| Form A ↔ Form B fidelity | B1 calibrates correlation, falls back to ridge fit if < 0.85 |
| TPOT cost of anti-clustering | B5 measures it; if > 1 °C avg, C3 reframes as Pareto |

## What Was Not Changed in Refinement

- The single-paper packaging (Atlas as §4 + TACE as §5–7) — already locked by Phase 4.
- The choice of 3D-NMP / HBM-PIM substrate — already locked by RESEARCH_BRIEF and Phase 4.
- The CoMeT-primary / Voxel-cross-check decision — already locked.
- The kill of I7 and demotion of HC-MoE — already locked.

## Remaining Reviewer-Exposed Weaknesses (acknowledged in §11)

- **Transferred controls such as TACG-port may compress the win** if substrate anisotropy is small. Mitigated by reporting the win as a function of anisotropy rather than a single number; this does not overturn a thermal gap against NMP-native baselines.
- **TPOT cost may exceed 1 °C** on the most clustered task family. Mitigated by reframing C3 as Pareto if needed and surfacing this as a finding rather than hiding it.
- **Voxel may disagree with CoMeT.** Mitigated by predeclaring the agreement criterion before the cross-check runs.

These are honest limitations, not blockers.
