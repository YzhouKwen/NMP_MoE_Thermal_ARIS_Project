# Pipeline Summary

**Problem**: Irregular MoE routing on 3D-stacked NMP creates joint spatial-temporal alignment of co-bursting expert pairs with the substrate's anisotropic thermal kernel, producing a localized hotspot that token-level balancing cannot see and that costs throughput under thermal cap.

**Final Method Thesis**: Anti-cluster high-power, high-correlation experts under the anisotropic 3D thermal kernel by solving a QAP whose objective is a direct `max_t T(t)` surrogate, not an eigenvalue proxy.

**Final Verdict**: READY

**Date**: 2026-06-24

## Final Deliverables

- Proposal: `refine-logs/FINAL_PROPOSAL.md`
- Review summary: `refine-logs/REVIEW_SUMMARY.md`
- Refinement report: `refine-logs/REFINEMENT_REPORT.md`
- Experiment plan: `refine-logs/EXPERIMENT_PLAN.md`
- Experiment tracker: `refine-logs/EXPERIMENT_TRACKER.md`

## Contribution Snapshot

- **Dominant contribution**: QAP-formulated anti-clustering of MoE experts on 3D-NMP, with a direct `max_t T(t)` surrogate (Form A) inside the solver and CoMeT-based verification (Form B) at acceptance, shown to close the thermal gap left by current NMP-native MoE placements.
- **Optional supporting contribution**: Section 4 characterization showing token-balance ≠ thermal-balance under LPR-balanced routing (empirical justification for the three QAP objective terms).
- **Explicitly rejected complexity**: online remapping (FDR/I5 → v2), headroom-credit scheduling (HC-MoE/I4 → separate submission), cool-tier shadow experts (I7 → killed), eigenvalue surrogate, standalone Atlas paper, per-step solve, custom thermal solver.

## Must-Prove Claims

- **C1** Token-balance ≠ thermal-balance: under LPR-balanced routing, token Gini ≤ 0.05 with bank-activity Gini ≥ 0.30 and ΔT_peak < 1 °C on ≥ 3/4 task families.
- **C2** TACE reduces peak T against NMP-native baselines: 4–7 °C vs random/even-odd, 2–4 °C vs NeuroTAP, 1–3 °C vs Stratum (paired bootstrap, p < 0.05 with Bonferroni, on held-out family). TACG-port is retained as a transferred opposite-sign control.
- **C3** Thermal wins translate to E2E serving: 1.3–1.8× throughput at fixed T_cap, 30–60% fewer throttle events, ≤ 1 °C-worth (≈ ≤ 5%) avg TPOT increase.

## First Runs to Launch

1. **B0** — pre-flight inventory: trace coverage matrix + CoMeT/Voxel smoke-test against a published 3D thermal anchor + solver wall-clock at 16×4
2. **B1** — surrogate calibration: Pearson/Spearman correlation between Form A and Form B; ridge-refit fallback if < 0.85
3. **B2** — Section 4 hook (C1): LPR / aux-loss-free / vanilla routing × 4 task families × CoMeT replay

These three runs unlock the rest of the plan (M0–M2 gates).

## Main Risks

- **Some transferred controls or communication-centric placements close the gap at low anisotropy** — Mitigation: anisotropy sweep in B8 reports the delta as a function of R_v/R_l; the load-bearing finding is the thermal gap of NMP-native baselines.
- **Anti-clustering costs TPOT > 1 °C-worth** — Mitigation: B5 measures it; if it does, reframe C3 as joint Pareto improvement and surface as finding.
- **Form A poorly correlates with Form B peak T** — Mitigation: B1 ridge-refit fallback; if still < 0.85, switch to per-family-trained weights.
- **Voxel disagrees with CoMeT on hotspot location** — Mitigation: predeclared agreement criterion in B7 (Jaccard ≥ 0.67 on top-3 banks); report as limitation, not retraction.

## Locked Phase 4.5 Inputs

- Q5 = predicted `max_t T(t)` as thermal surrogate
- Q6 = ILP cap at 16 experts × 4 banks (Voxel cross-check at 32×8)
- Q7 = train-on-3 / test-on-1, 4-fold domain shift

## Pre-Submission Change Coverage

All 12 mandatory pre-submission changes from Phase 4 review are addressed by the proposal + plan; none deferred. Coverage table appears in both `FINAL_PROPOSAL.md` §12 and `EXPERIMENT_PLAN.md` final section.

## Next Action

- Proceed to `/run-experiment` starting at B0.
