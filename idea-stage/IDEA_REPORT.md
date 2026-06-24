# Idea Discovery Report — Thermal-Aware MoE on 3D-Stacked NMP

**Direction**: thermal-aware MoE execution in 3D-stacked NMP architectures — full lever sweep across placement, scheduling, remapping, throttling, and architecture co-design.
**Date**: 2026-06-23
**Stage**: Phase 2 + 3 + 4 complete (deep novelty + GPT-5.4 critical review). Phase 4.5 pending user approval.
**Pipeline**: research-lit → idea-creator (this file) → novelty-check → research-review → research-refine-pipeline
**Mode**: AUTO_PROCEED=false, COMPACT=true
**Reviewer verdict**: GO-WITH-CHANGES. Kill I7. Recast CATEP as thermal anti-clustering. Replace eigenvalue surrogate with direct T-prediction. TACG-port baseline + domain-shift + thermal-cap E2E eval non-negotiable. Do not split atlas.

## Executive Summary (post-review)

Eight candidate ideas generated → 4 survived first-pass filter → 3 survive Phase 4 critical review (I7 killed). Headline contribution recast on reviewer demand:

1. **TACE (Thermal Anti-Clustering of Experts)** — formerly I3/CATEP. Single-paper headline mechanism. Score: **7/10** at top-tier arch venue bar.
2. **Atlas as Section 4** — formerly I1, no longer branded as separate contribution. Sole job: derive TACE's objective terms from data. Score: **5/10 as section** (3/10 standalone — do not split).
3. **HC-MoE** — formerly I4. Future-work / separate submission. Score: **4/10** (quality and stability concerns).

**Killed**: I7 (Cool-Tier Shadow Experts) — worst novelty/effort ratio, overlaps CRAFT replication and Tasa heterogeneity.

**Reviewer recommendation**: GO-WITH-CHANGES on the bundled paper. Submission-blocking changes are listed in §"Mandatory Pre-Submission Changes" below. If the user cannot deliver TACG-port + thermal-cap E2E eval + CoMeT/Voxel cross-check, do not submit to HPCA/MICRO/ISCA.

## Updated Landscape (Post-Search + Post-Review)

The Phase 1 survey's baseline list has been extended in filtering and review. **Two new entries added in Phase 4**: TACG (2606.01007, May 2026) — task-conditioned co-activation grouping on distributed GPU MoE; and Gimbal (2606.15177, June 2026) — coordinated cross-level MoE serving with source-aware placement. Both compress the novelty boundary.

Final closest-prior-work table:

| Theme | Closest prior work | What they do | What they leave open for us |
|-------|--------------------|--------------|----------------------------|
| MoE on 3D NMP, perf-driven | HD-MoE, A3D-MoE (2507.19142), Stratum (2510.05245), ELMoE-3D (2604.14626) | hybrid TP/EP, even-odd mapping, tiered Mono3D-DRAM access-likelihood placement, hybrid-bonded speculative decoding | thermal axis on all four |
| MoE on HBM-PIM | Sieve (2605.11277), 2602.10254 (IMC-MoE) | bimodal-skew GPU/PIM split, multiplexed IMC | 3D-stack vertical thermal coupling |
| Thermal-aware 3D LLM | Tasa (2508.07252) | op-type partitioning (compute vs attention) on heterogeneous 3D | expert-level skew |
| Thermal-aware DNN data placement | NeuroTAP (TACO 2024), US Patent 20210034256 | frequency-driven placement, temperature-gradient placement | co-activation graph, MoE expert semantics |
| Thermal-aware scheduling on PIM | THERMOS (2508.10691) | MO-RL Pareto scheduler on heterogeneous chiplet PIM | MoE-specific, 3D-stacked, credit-based proactive |
| MoE co-activation placement | **TACG (2606.01007, May 2026)** | task-aware co-activation grouping + generic-expert replication on distributed GPU; communication objective | **3D-NMP substrate, thermal Green's function, *anti-clustering* objective** |
| MoE coordinated serving | **Gimbal (2606.15177, Jun 2026)** | source-aware placement + cross-level scheduling for vLLM-like GPU systems | thermal axis, 3D-stack physics |
| MoE expert migration | MoNDE (2405.18832), Decoupling Expert Residency (2604.02715) | hot/cold migration to GPU, residency optimization | bank-level granularity, thermal trigger |
| Expert replication for serving | CRAFT (2603.28768), Fast MoE Prefetch (2605.11537) | memory-budget-aware replication for load balance | thermal-driven replica selection |
| Algorithmic balance | LPR (2506.21328), aux-loss-free (2408.15664) | near-uniform Gini | physical thermal balance gap unmeasured |
| MoE expert traces | Patterns Behind Chaos (2510.05497) | public traces of 4 large 200B-1000B MoE models | thermal characterization on top of these traces |
| Thermal modeling | CoMeT (2109.12405), MFIT (2410.09188), Voxel (2604.26821) | HotSpot-grade transient T-fields for 3D | MoE-specific power model |
| Thermal vulnerability | 2509.00633 | adversarial heat injection bank-level | benign-workload-driven hotspot |

## All Eight Generated Ideas (Post-Phase-4 Status)

| ID | Title | Lever | Risk | Effort | Phase-4 Score | Final Status |
|----|-------|-------|------|--------|---------------|--------------|
| I1 | Routing-to-Temperature Atlas | measurement | LOW | 2-3 wk | 3/10 standalone, 5/10 as section | **MERGE → Section 4** |
| I2 | Balanced Tokens, Unbalanced Heat | counter-result | LOW-MED | 1-2 wk | included in Section 4 score | **MERGE → Section 4** |
| I3→**TACE** | Thermal Anti-Clustering of Experts (recast) | placement | MED | 3-5 wk | **7/10** | **HEADLINE** |
| I4 | HC-MoE — Headroom-Credit Scheduler | scheduling | MED | 4-6 wk | 4/10 | **DEMOTE → separate submission** |
| I5 | FDR — Forecast-Driven Remapping | remapping | HIGH | 1-2 mo | not reviewed | **DEMOTE → v2** |
| I6 | Feedback-Stable Thermal Router | thermal-control | MED | 1-2 mo | not reviewed | **DEMOTE → TCAD path** |
| I7 | Cool-Tier Shadow Experts | arch-codesign | MED | 1-2 mo | **2/10** | **KILLED** |
| I8 | Thermal Firebreak Banks | arch-codesign | MED-HIGH | 3-5 wk | included in TACE | **MERGE → TACE constraint** |

## Survivors (Ranked, Post-Review)

### 🏆 TACE — Thermal Anti-Clustering of Experts (recast from I3/CATEP) — TOP PICK
**Headline thesis**: On 3D-NMP MoE, vertically co-located experts with high temporal co-activation correlation create the dominant thermal coupling load. TACE *anti-clusters* high-power high-correlation experts under an anisotropic 3D thermal kernel, directly minimizing a temperature surrogate derived from the RC/Green's-function model — not an eigenvalue proxy.

- **Mechanism (recast)**: QAP on expert → (bank, tier). Objective is a direct temperature surrogate: predicted max_t T(t) (or top-q hottest banks, or time-above-threshold) computed from a fast RC/Green's-function evaluation of the bank power matrix. Constraints encode bank capacity and an optional firebreak ring. Term structure: (a) per-expert long-run rate, (b) **anti-clustering** term on the expert co-activation correlation graph weighted by the anisotropic 3D thermal kernel, (c) lateral/vertical coupling penalty. Solver: simulated annealing with spectral-relaxation warm start; small instances cross-validated by ILP/MIP exact solve to bound optimality gap. One offline solve per task family.
- **Hypothesis (sharpened)**:
  - 4–7 °C peak-T reduction vs. random/even-odd
  - 2–4 °C vs. NeuroTAP-style frequency placement
  - 1–3 °C vs. Stratum-style access-likelihood
  - **2–5 °C vs. TACG-ported-to-3D-NMP** (TACG packs co-activated experts → opposite of what's wanted)
  - ≤ 1 °C TPOT change
  - At thermal-cap-bound serving: 1.3–1.8× throughput and 30–60% fewer throttle events vs. best baseline
- **Differentiators (Phase-4 sharpened)**:
  - TACG (2606.01007): GPU/distributed substrate, communication objective, **clusters** co-activated experts. TACE anti-clusters under thermal kernel on 3D-NMP. Same-substrate TACG port is mandatory baseline.
  - Stratum (2510.05245): access-likelihood tiering on Mono3D-DRAM, no thermal, no co-activation
  - NeuroTAP: DNN-generic frequency placement, no expert semantics, no co-activation
  - HD-MoE / A3D-MoE: HBM-access / even-odd, thermal-blind
  - Tasa: op-type partitioning for dense LLM, not expert
  - ViBE: rack-scale GPU, not bank-level
  - Gimbal: GPU serving, source-aware not thermal-aware
- **Min experiment**: Public traces (2510.05497) → co-activation graph + per-bank power → CoMeT thermal solver → QAP solver. 6-arm comparison: random, even-odd, NeuroTAP-style, Stratum-style, **TACG-ported**, TACE. CoMeT primary; Voxel cross-check on a subset; reproduce one published 3D thermal trend (anchor credibility).
- **Risk**: MEDIUM. Risks are: (a) TACG-ported survives the port well enough to compress the win; (b) anti-clustering improves T but hurts TPOT under thermal cap.
- **Top reviewer objection**: "Incremental placement heuristic; weak novelty over TACG/NeuroTAP; no proof that lower T translates to better serving under workload drift." Mitigations are in §"Mandatory Pre-Submission Changes" below.

### Section 4 of the bundled paper — Routing-to-Temperature Characterization (formerly I1, no longer a separate contribution)
**Role**: motivation/characterization section whose only job is to derive TACE's objective terms from data. Not branded as a standalone contribution; not split into a separate paper.

- **What this section must prove**:
  1. **Token-balance ≠ thermal-balance**: under LPR-balanced routing (token Gini ≤ 0.05), bank-activity Gini stays ≥ 0.3 and ΔT_peak vs. vanilla is < 1 °C — algorithmic balance fails physically. (Formerly I2.)
  2. **Pairwise co-burst + vertical coupling are the missing variables**: pure frequency placement (NeuroTAP-style) leaves measurable hot stripes when co-bursting expert pairs land on vertically adjacent banks.
  3. **Three workload regimes** emerge from the public traces (uniform / bimodal / burst) and each demands a different objective term.
- **Why not a standalone paper**: the trace dataset is public (2510.05497), so a CoMeT-replay characterization paper would read as "profiling + simulator replay" without a mechanism. Pulled inside the bundled paper, it becomes the empirical justification for TACE's three objective terms.

### Future-work / separate submission — HC-MoE Headroom-Credit Scheduler (I4)
**Status**: Not in the bundled submission. Reviewer flagged inference-semantics / control-stability risk (score 4/10). Carry as v2 once TACE results unlock the substrate.

- **Mechanism unchanged**: bank publishes credit = (T_max − T_now)/(T_max − T_amb); router multiplies softmax weights by credit; credit < threshold redirects to top-2k backup expert. Proactive, not reactive.
- **New competitor surfaced**: Gimbal (2606.15177) does coordinated cross-level MoE serving with source-aware placement on GPU. HC-MoE's wedge stays 3D-stacked + thermal-credit, but the framing now competes with Gimbal on the cross-level claim.
- **Mandatory before HC-MoE submission**: perplexity sweep, control-loop stability proof, anti-oscillation evidence against naive thermal-aware routing, throughput wins vs. throttle + load-shed baselines.

### KILLED — I7 Cool-Tier Shadow Experts
**Reviewer score**: 2/10. Worst novelty-to-effort ratio. Overlaps CRAFT (replication) and Tasa (heterogeneous tiers). Reviewer flagged this as "overbuilt hardware answer to a software problem; unrealistic evaluation burden." Removed from active candidate pool.

## Mandatory Pre-Submission Changes (from Phase 4 review)

These are submission-blocking. If any cannot be delivered, do not submit to HPCA/MICRO/ISCA.

1. **Single paper, do not spin out the atlas**. Section 4 is motivation/characterization, not a branded contribution.
2. **Recast as anti-clustering**. The mechanism is "anti-cluster high-power high-correlation experts under anisotropic 3D thermal kernel," not "co-activation-aware placement."
3. **Direct temperature surrogate**. Replace `min Σ_t λ_max(P(t))` with predicted `max_t T(t)` (or top-q hottest banks, or time-above-threshold) computed from the RC/Green's-function model. Peak T is not an eigenvalue.
4. **TACG-port baseline is the centerpiece**. Same-substrate TACG must run on the 3D-NMP model and the paper must show TACG packs co-activated experts together → makes hotspots worse. Without this baseline beating exercise, the paper reads as "TACG ported."
5. **Mandatory baselines beyond TACG-port**: Stratum-style access-likelihood, NeuroTAP-style frequency, random, even-odd.
6. **Per-term ablations**: long-run rate, pair co-activation, anisotropic thermal kernel, firebreak ring. One ablation row per term.
7. **End-to-end serving metrics under thermal cap**: TPOT, throughput, throttle events, time-above-threshold. Thermal-only wins (peak-T reduction in isolation) are insufficient.
8. **Domain-shift evaluation**: place on one task family, evaluate on another. Workload drift is the natural reviewer attack on static placement.
9. **Optimality-gap bound**: ILP/MIP exact solve on small instances; report the SA-vs-exact gap and warm-start scaling curves.
10. **CoMeT primary, Voxel cross-check**. Reproduce one published 3D thermal trend to anchor credibility.
11. **Parameter sweeps**: ambient T, package/TIM resistance, stack height/tier count, workload burstiness, thermal threshold. Each axis at minimum 3 points.
12. **Token-balance ≠ thermal-balance proof in Section 4**: LPR token Gini ≤ 0.05 with bank-activity Gini ≥ 0.3 and ΔT_peak < 1 °C — the empirical hook that justifies Section 5+.

## Demoted / Merged / Killed (preserved for future iterations)

- **I2 → folded into Section 4** of the bundled paper as the "balanced tokens, unbalanced heat" empirical hook (mandatory change #12).
- **I8 → folded into TACE** as an optional firebreak-ring constraint within the QAP. One ablation row.
- **I5 (FDR)** — natural extension once TACE exposes static-placement drift sensitivity. Defer to v2.
- **I6 (Feedback-stable router)** — theoretical contribution; weak arch-venue fit. Possible IEEE TCAD path; defer.
- **I7 (Cool-Tier) — KILLED in Phase 4**. Reviewer score 2/10. Worst novelty/effort ratio; overlaps CRAFT replication and Tasa heterogeneity. Not carried forward.
- **I4 (HC-MoE)** — kept alive but moved to *separate submission*. Reviewer score 4/10 with inference-semantics and stability concerns. Pursue after TACE results land.

## Pilot Phase

**Skipped this iteration.** No GPU is committed for this stage and the surviving ideas are evaluable on CPU + simulator (CoMeT/Voxel) with public traces. All three top ideas are flagged as "needs simulator-driven pilot" rather than "needs GPU pilot." The trace-driven pilot for I1+I3 is the natural first run after Phase 4.5.

## Suggested Execution Path (post-Phase-4)

1. ~~Phase 3 (deep novelty)~~ — DONE. TACG and Gimbal added to baseline list.
2. ~~Phase 4 (critical review)~~ — DONE. Verdict: GO-WITH-CHANGES, recast as TACE, kill I7, demote I4.
3. **Phase 4.5 (next)**: `/research-refine-pipeline` to:
   - Lock the Problem Anchor on TACE (anti-clustering under anisotropic 3D thermal kernel)
   - Reformulate the QAP objective with direct temperature surrogate (replace λ_max(P))
   - Define the TACG-port baseline algorithm precisely
   - Produce `refine-logs/FINAL_PROPOSAL.md` and `refine-logs/EXPERIMENT_PLAN.md` covering all 12 mandatory pre-submission changes
4. **Phase 5**: finalize this report + write `IDEA_CANDIDATES.md` compact for downstream skills.
5. **Phase 6 (downstream)**: `/run-experiment` on the trace-driven pilot (CoMeT primary + TACG-port baseline + token-balance≠thermal-balance proof).

## Open Questions for User (Phase 4.5 inputs)

| # | Question | User answer |
|---|----------|------------|
| Q1 | Paper packaging? | **Single paper, Atlas-as-Section-4 + TACE as Sections 5–7** — confirmed |
| Q2 | Include HC-MoE in same submission? | **Separate follow-up** — confirmed by Phase-4 review |
| Q3 | Primary thermal simulator? | **CoMeT primary, Voxel cross-check** — confirmed |
| Q4 | Carry I7 as v2 stretch? | **KILLED** — reviewer score 2/10 |

## Phase 4.5 Inputs Needed

The refine pipeline needs three more decisions before locking the Problem Anchor:

| # | Decision | Default |
|---|----------|---------|
| Q5 | Direct temperature surrogate choice: predicted max_t T(t), top-q hottest banks, or time-above-threshold? | predicted max_t T(t) — most direct mapping from objective to peak-T claim |
| Q6 | Optimality-gap protocol: ILP/MIP cap at N=16 experts × 4 banks, or N=32×8? | N=16×4 (faster) with Voxel cross-check at N=32×8 |
| Q7 | Domain-shift protocol: 4 task families round-robin, or train-on-3 / test-on-1? | Train-on-3 / test-on-1, repeated across 4 folds |

