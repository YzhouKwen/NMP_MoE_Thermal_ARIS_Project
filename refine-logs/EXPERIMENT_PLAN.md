# Experiment Plan — TACE

**Date**: 2026-06-24
**Stage**: Workflow 1.5, experiment-plan output (replaces generic placeholder)
**Method source**: `refine-logs/FINAL_PROPOSAL.md` (TACE, v1)
**Claims source**: `FINAL_PROPOSAL.md` §9

## Problem and Method Thesis (one paragraph each)

**Problem.** Irregular MoE routing on 3D-stacked NMP creates joint spatial-temporal alignment of co-bursting expert pairs with the substrate's anisotropic thermal kernel. Token-level balancing cannot see this alignment. The result is a localized hotspot that costs throughput under thermal cap.

**Method thesis.** Anti-cluster high-power high-correlation experts under the anisotropic 3D thermal kernel by solving a QAP whose objective is a direct `max_t T(t)` surrogate, not an eigenvalue proxy.

## Claim Map

| Claim | Importance | Minimum convincing evidence | Experiment blocks |
|-------|-----------|------------------------------|--------------------|
| **C1** Token-balance ≠ thermal-balance | Section 4 hook — without it the paper has no motivation | Token Gini ≤ 0.05 + bank-activity Gini ≥ 0.30 + ΔT_peak vs vanilla < 1 °C on ≥ 3/4 task families | B2 |
| **C2** TACE reduces peak T vs every baseline including TACG-port | Headline result — the contribution | Paired bootstrap (B=1000, p<0.05) deltas: 4–7 °C vs random/even-odd · 2–4 °C vs NeuroTAP · 1–3 °C vs Stratum · **2–5 °C vs TACG-port**, on held-out family | B3, B4 |
| **C3** Thermal wins translate to E2E serving wins | Publishability — peak T alone is reviewer-bait | 1.3–1.8× throughput at fixed T_cap, 30–60% fewer throttle events, ≤ 1 °C avg TPOT increase | B5 |

## Experiment Blocks

### B0 — Pre-flight inventory and infrastructure check
- **Validates**: feasibility (no claim directly)
- **Inputs**: Patterns Behind Chaos trace dataset (arXiv 2510.05497); CoMeT and Voxel installs; QAP solver toolchain (NumPy/SciPy + Gurobi or CBC)
- **Outputs**: trace coverage matrix (model × task-family × request count); CoMeT/Voxel smoke-test peak T on a hand-crafted uniform power map (must converge and reproduce CoMeT's published 3D thermal trend within ±5%); solver wall-clock on a 16×4 toy instance
- **Success**: ≥ 3 of 4 task families have ≥ 500 requests per model · simulators reproduce a published 3D thermal anchor · solver closes at 16×4
- **Priority**: must run first
- **Budget**: 0.5–1 day

### B1 — Surrogate calibration (Form A ↔ Form B)
- **Validates**: solver fidelity (precondition for C2)
- **Method**: on a held-out calibration trace fold (10% of B0's surviving requests), evaluate 200 random assignments + 50 SA solutions; compute Form A (closed-form surrogate) and Form B (CoMeT replay peak T) for each; report Pearson and Spearman correlation
- **Acceptance**: correlation ≥ 0.85 on both metrics. If lower, refit (α, β, γ, δ) via ridge regression with cross-validated λ; rerun until threshold met or document residual
- **Outputs**: scatter plot, correlation values, final weight tuple, residual analysis
- **Priority**: must run before B3 onward
- **Budget**: 1 day

### B2 — Section 4 hook: token-balance ≠ thermal-balance (C1)
- **Validates**: C1
- **Method**: replay each task family's trace under (i) vanilla expert routing, (ii) LPR-balanced routing (2506.21328), (iii) aux-loss-free balanced routing (2408.15664); for each, compute token Gini, expert-activity Gini, bank-activity Gini under a fixed reference placement, and CoMeT peak T
- **Success criterion (predeclared)**: on ≥ 3/4 task families, LPR yields token Gini ≤ 0.05 *and* bank-activity Gini ≥ 0.30 *and* peak T delta vs vanilla < 1 °C
- **Outputs**: 4×3 table (family × routing scheme) of (token Gini, bank Gini, ΔT) · Section 4 headline figure
- **Priority**: must run
- **Budget**: 1–2 days

### B3 — Main 6-arm thermal comparison (C2 core)
- **Validates**: C2 — the headline result
- **Method**: for each of the 4 task families and each baseline in `FINAL_PROPOSAL.md` §8 (random, even-odd, NeuroTAP-style, Stratum-style, TACG-port, TACE), produce an assignment using that baseline's algorithm, replay the family's full trace, evaluate Form B (CoMeT peak T over trace). 10 seeds for random. 4-fold Q7 domain shift: train on 3 families, test on 1.
- **Outputs**: 4 (held-out family) × 6 (baselines) × n_seeds peak T matrix; paired bootstrap test (B=1000) for each baseline-vs-TACE delta on the held-out family; headline TACG-port vs TACE scatter (peak T vs communication cost)
- **Success criterion (predeclared)**: paired deltas in §9 C2 hold with p < 0.05 after Bonferroni correction over 5 pairwise comparisons; **TACG-port loses by ≥ 2 °C on ≥ 3/4 held-out families**
- **Priority**: must run
- **Budget**: 3–5 days

### B4 — Per-term ablations (C2 mechanism)
- **Validates**: C2 — establishes the contribution is the term structure, not a generic optimizer
- **Method**: run TACE with each ablation in `FINAL_PROPOSAL.md` §10 (A1–A7); same 4 task families; report peak T vs full TACE
- **Success criterion (predeclared)**: removing each of the three load-bearing terms (long-run rate, pair co-activation, anisotropic kernel) costs ≥ 1 °C peak T on average; A5 (λ_max surrogate) loses to direct-T on ≥ 3/4 families
- **Outputs**: ablation table (7 rows × 4 families × peak T), Figure: bar chart of ablation deltas
- **Priority**: must run
- **Budget**: 2–3 days

### B5 — Thermal-cap E2E serving (C3)
- **Validates**: C3 — the publishability claim
- **Method**: pick the best 3 placements from B3 (TACG-port, NeuroTAP-style, TACE); run a closed-loop serving simulator (CoMeT transient + simple throttle controller; throttle triggers when CoMeT-predicted T ≥ T_cap; throughput = served tokens / wall-clock) on each task family for ≥ 30 s wall-clock per condition; sweep T_cap ∈ {85, 90, 95} °C
- **Outputs**: per-T_cap throughput, throttle event count, average TPOT, P99 TPOT, time-above-threshold
- **Success criterion (predeclared)**: TACE beats TACG-port and NeuroTAP-style on throughput by ≥ 1.3× at T_cap = 90 °C; throttle event count down ≥ 30%; avg TPOT delta ≤ 1 °C-worth (≈ ≤ 5% TPOT increase)
- **If C3 fails**: reframe C3 as joint Pareto improvement rather than dominance — `FINAL_PROPOSAL.md` §11 risk
- **Priority**: must run
- **Budget**: 3–5 days

### B6 — ILP optimality gap (rigor)
- **Validates**: solver quality claim
- **Method**: at Q6 cap (n_E=16, n_B=4, n_T=4 = 16 sites), construct 20 random subproblems by sub-sampling experts from each task family; run SA and Gurobi/CBC ILP to optimality (or 1-hour cap, whichever first); report gap = (Form A under SA − Form A under ILP) / Form A under ILP. Optionally rerun at 32×8 (Voxel cross-check scale); ILP may not close — report best-known gap as upper bound.
- **Outputs**: gap distribution; warm-start scaling curve (gap as a function of n_E at fixed n_B, n_T)
- **Success criterion (predeclared)**: median gap ≤ 3% at 16×4; warm-start scaling curve does not blow up
- **Priority**: must run
- **Budget**: 1–2 days

### B7 — CoMeT × Voxel cross-check (substrate credibility)
- **Validates**: simulator-independence of C2
- **Method**: pick the held-out family from B3 with the largest TACE-vs-TACG-port delta; rerun the 6-arm comparison using Voxel at 32×8; compare hotspot location (top-3 hottest banks) and peak T delta
- **Success criterion (predeclared)**: ≥ 3 of 4 (model, family) cells agree on top-3 hottest bank set with Jaccard ≥ 0.67; peak T deltas agree within ±15% in magnitude and *match sign*
- **If disagreement > criterion**: report as a limitation rather than retraction; investigate kernel anisotropy differences
- **Priority**: must run
- **Budget**: 2 days

### B8 — Parameter sweeps (robustness)
- **Validates**: C2/C3 robustness
- **Method**: sweep each axis at ≥ 3 points, all on one anchor task family with TACE vs TACG-port and NeuroTAP-style:
  - Anisotropy ratio R_v / R_l ∈ {0.5×, 1×, 2× of CoMeT default}
  - Ambient T ∈ {35, 45, 55} °C
  - Stack height n_T ∈ {4, 6, 8}
  - Burstiness (sliding-window size for c_{ef}) ∈ {0.5τ, 1τ, 2τ}
  - Thermal threshold T_cap ∈ {85, 90, 95} °C (already covered in B5; reused here)
  - q_e scale ∈ {0.5×, 1×, 2×} (power-model sensitivity)
- **Outputs**: per-axis trend lines; identification of the axis on which TACG-port closes the gap (anti-fragility evidence)
- **Success criterion (predeclared)**: TACE-vs-TACG-port delta stays positive (TACE wins) across ≥ 80% of swept points; identify the closing point on the anisotropy axis
- **Priority**: must run (sweeps are mandatory pre-submission change #11)
- **Budget**: 2–3 days

### B9 — Firebreak ring ablation (optional component)
- **Validates**: firebreak utility (one ablation row from §10 A4)
- **Method**: rerun B3 with firebreak ring on (FB = vertical column through highest-power bank in baseline placement) and off
- **Success criterion**: if firebreak helps by ≥ 0.5 °C peak T on ≥ 2 families, include in headline TACE; otherwise drop and mention as failed ablation
- **Priority**: optional (already counted in B4 as A4, but isolated here for reporting clarity)
- **Budget**: 1 day

## Run Order with Decision Gates

| Milestone | Goal | What runs | Gate (predeclared) | Estimated wall-clock |
|-----------|------|-----------|--------------------|------------------------|
| **M0** | Infrastructure ready | B0 | Trace coverage and simulators usable; if not, scope reduction needed | 0.5–1 day |
| **M1** | Surrogate is faithful | B1 | corr(A, B) ≥ 0.85, or ridge-refit accepted; otherwise stop and reformulate Form A | 1 day |
| **M2** | C1 holds | B2 | LPR token Gini ≤ 0.05 *and* bank Gini ≥ 0.30 *and* ΔT < 1 °C on ≥ 3/4 families. If not, Section 4 hook fails — reconsider paper framing | 1–2 days |
| **M3** | C2 holds | B3 + B4 + B6 | TACE beats TACG-port by ≥ 2 °C on ≥ 3/4 families with p < 0.05 (after Bonferroni); per-term ablations bite; ILP gap ≤ 3%. If TACG-port wins on any family, debug port faithfulness, then escalate to §11 risk and consider Pareto framing | 6–10 days |
| **M4** | C3 holds | B5 | Throughput ≥ 1.3× and throttle ≥ 30% reduction and TPOT ≤ +5%. If TPOT > +5%, reframe C3 as Pareto | 3–5 days |
| **M5** | Cross-substrate credibility | B7 + B8 | Voxel agrees on sign and top-3 hotspots; parameter sweeps preserve TACE wins on ≥ 80% of points | 4–5 days |
| **M6** | Final polish | B9 + writing prep | Firebreak ring decision; commit final claim wordings to paper | 1 day |

**Total wall-clock estimate**: 16–25 days end-to-end, single-CPU node. Parallelism across task families collapses this to 8–14 days on a 4-core machine.

## Risk and Mitigation (cross-referenced to FINAL_PROPOSAL.md §11)

| Risk | Likelihood | Earliest detection | Mitigation |
|------|-----------|---------------------|-------------|
| Trace inventory has empty cells | LOW | B0 | Drop cell from grid; reduce domain-shift folds to surviving cells |
| Form A poorly correlates with Form B | LOW-MED | B1 | Ridge refit; if still < 0.85, switch to per-family-trained weights |
| TACG-port ties TACE on some family | MED | B3 (mid-run) | Confirm port faithfulness via communication-cost check; if port is faithful, report tie + identify anisotropy regime in B8 |
| TPOT cost of anti-clustering > 1 °C-worth | MED | B5 | Reframe C3 as Pareto; surface as finding |
| Voxel disagrees with CoMeT | MED | B7 | Limitation, not refutation; document kernel-anisotropy delta |
| ILP doesn't close at 16×4 in 1 hour | LOW | B6 | Best-known-gap as upper bound (still publishable) |
| 200B–1000B trace family is computationally too large | LOW | B0 | Sub-sample at constant burstiness; report sub-sample protocol explicitly |
| Parameter sweep reveals an axis where TACE loses | MED | B8 | Anti-fragility framing: the win condition is the substrate ARIS targets (3D-NMP); discuss out-of-target regime as limitation |

## Coverage of the 12 Mandatory Pre-Submission Changes (from review)

| # | Mandatory change | Block(s) addressing it |
|---|------------------|-------------------------|
| 1 | Single paper, no atlas split | B2 (Section 4 hook in this same paper) |
| 2 | Anti-clustering recast | B3 (sign of γ in TACE > 0); B4 A2 (pair-term ablation) |
| 3 | Direct T-surrogate | B1 calibration; B4 A5 (λ_max ablation) |
| 4 | TACG-port baseline centerpiece | B3 (mandatory arm, headline figure) |
| 5 | Baselines beyond TACG-port | B3 (6 arms incl. random, even-odd, NeuroTAP, Stratum) |
| 6 | Per-term ablations | B4 (A1–A4 + A5 surrogate + A6/A7 solver) |
| 7 | E2E serving metrics under thermal cap | B5 |
| 8 | Domain-shift evaluation | B3 (Q7 4-fold train-on-3/test-on-1) |
| 9 | Optimality-gap bound | B6 |
| 10 | CoMeT primary, Voxel cross-check | B0 anchor + B7 |
| 11 | Parameter sweeps | B8 |
| 12 | Token-balance ≠ thermal-balance | B2 |

All 12 changes covered; no deferral.

## Compute Budget Summary

- **Single CPU node** sufficient for entire plan (no GPU committed for this stage).
- ILP step depends on Gurobi or CBC; both have free academic options.
- CoMeT and Voxel are open-source.
- Storage: ~50 GB for trace replays + intermediate power maps.

## What Comes After This Plan

When all gates pass:
1. Final paper draft (Section 4 = B2, Sections 5–6 = B3+B4, Section 7 = B5, Section 8 = B6+B7+B8).
2. Optional v2 path: FDR (forecast-driven remapping) using TACE's drift quantification from Q7.
3. Optional separate submission: HC-MoE (scheduling lever).
