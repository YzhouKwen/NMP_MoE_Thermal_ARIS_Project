# Idea Candidates — Compact

**Direction**: thermal-aware MoE execution in 3D-stacked NMP architectures
**Date**: 2026-06-23
**Stage**: Phase 4 complete (Phase 4.5 pending user inputs Q5–Q7)
**Mode**: AUTO_PROCEED=false, COMPACT=true
**Reviewer verdict**: GO-WITH-CHANGES on bundled paper.

## Final Status Table

| # | Idea | Lever | Phase-4 Score | Status |
|---|------|-------|---------------|--------|
| 1 | **TACE** — Thermal Anti-Clustering of Experts (recast from CATEP) | placement | **7/10** | **HEADLINE** |
| 2 | Section 4 — Routing-to-Temperature Characterization (formerly Atlas) | measurement | 5/10 as section | bundled |
| 3 | HC-MoE — Headroom-Credit Scheduler | scheduling | 4/10 | separate submission |
| 4 | I7 — Cool-Tier Shadow Experts | arch-codesign | 2/10 | **KILLED** |

## Active Idea: TACE

- **Thesis**: Anti-cluster high-power high-correlation experts under anisotropic 3D thermal kernel; minimize a *direct* temperature surrogate (predicted max_t T(t)), not an eigenvalue proxy.
- **Mechanism**: QAP on expert→(bank,tier). Three terms — long-run rate, anti-clustering on co-activation graph weighted by 3D thermal kernel, lateral/vertical coupling penalty. Optional firebreak ring. SA + spectral warm-start; ILP exact on small instances for gap bound.
- **Key wins claimed**:
  - 4–7 °C peak-T ↓ vs random/even-odd
  - 2–4 °C ↓ vs NeuroTAP
  - 2–5 °C ↓ vs **TACG-ported** (centerpiece baseline)
  - 1.3–1.8× throughput under thermal cap; 30–60% fewer throttle events; ≤ 1 °C TPOT change
- **Substrate**: 3D-NMP (HBM-PIM bank/tier model), CoMeT primary, Voxel cross-check
- **Traces**: Patterns Behind Chaos public set (2510.05497) — 24k requests × 4 large MoE models

## Closest Prior Art (must beat or differentiate)

- **TACG (2606.01007)** — co-activation grouping on GPU, communication objective. Centerpiece baseline.
- **Stratum (2510.05245)** — Mono3D-DRAM access-likelihood tiering, no thermal.
- **NeuroTAP (TACO 2024)** — DNN-generic frequency placement.
- **Tasa (2508.07252)** — op-type partitioning for dense LLM, not expert.
- **Gimbal (2606.15177)** — coordinated GPU MoE serving (HC-MoE territory).

## Mandatory Pre-Submission Changes (12 items)

Single paper · anti-clustering recast · direct T-surrogate · TACG-port baseline · Stratum/NeuroTAP/random/even-odd baselines · per-term ablations · thermal-cap E2E metrics (TPOT, throughput, throttle events) · domain-shift folds · ILP optimality gap · CoMeT+Voxel cross-check · 3D thermal trend reproduction · token-balance≠thermal-balance proof in Section 4.

## Pending User Inputs (Phase 4.5)

- Q5: T-surrogate choice (default: predicted max_t T(t))
- Q6: ILP cap (default: 16 experts × 4 banks; Voxel cross-check at 32×8)
- Q7: Domain-shift protocol (default: train-on-3 / test-on-1, 4-fold)

## Next Step

`/research-refine-pipeline` on TACE — locks Problem Anchor, reformulates QAP with direct T-surrogate, defines TACG-port algorithm, produces `refine-logs/FINAL_PROPOSAL.md` and `refine-logs/EXPERIMENT_PLAN.md` covering the 12 mandatory changes.
