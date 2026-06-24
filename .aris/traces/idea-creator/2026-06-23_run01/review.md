# Phase 4 Critical Review Trace

**Date**: 2026-06-23
**Skill**: idea-creator (Phase 4)
**Reviewer**: GPT-5.4 via Codex MCP, xhigh reasoning
**Thread**: 019ef48a-0f28-7d93-8cb1-4a436a5e8e96
**Mode**: read-only sandbox

## Bundle reviewed
- I3 — CATEP (top pick)
- I1 — Atlas (Section 4 of bundled paper)
- I4 — HC-MoE (future-work)
- I7 — Cool-Tier (v2 stretch)
- Single-paper packaging: Atlas-as-Section-4 + CATEP as Sections 5–7

## Scores
- I3: 7/10
- I1 standalone: 3/10; as Section 4: 5/10
- I4: 4/10
- I7: 2/10

## Headline verdict
GO-WITH-CHANGES. Kill I7. Recast CATEP as "thermal anti-clustering" not "co-activation-aware placement". Replace eigenvalue surrogate with direct temperature prediction. TACG-port baseline mandatory. Domain-shift + thermal-cap end-to-end eval non-negotiable. Do not split atlas into separate paper.

## New prior art surfaced
- Gimbal (arXiv 2606.15177, 2026-06-13): coordinated MoE serving, source-aware placement + cross-level scheduling. GPU substrate, not thermal — competes with I4 framing only.

## Mandatory changes for HPCA/MICRO/ISCA
1. Single paper, do not spin out Atlas.
2. Drop "Atlas" as a branded contribution; keep as motivation/characterization section that derives CATEP's objective terms.
3. Recast CATEP as anti-clustering of high-power high-correlation experts under anisotropic 3D thermal kernel.
4. Direct temperature surrogate (max_t T(t), top-q hottest banks, time-above-threshold) replaces λ_max(P).
5. Same-substrate TACG port becomes the centerpiece baseline.
6. Add Stratum, NeuroTAP-style frequency, random, even-odd baselines.
7. Ablate each objective term (rate, pair co-activation, thermal kernel, firebreak).
8. End-to-end serving metrics under thermal cap: TPOT, throughput, throttle events, time-above-threshold.
9. Domain-shift: place on one task family, evaluate on another.
10. Optimality gap: ILP/MIP exact solve on small instances.
11. CoMeT primary, Voxel cross-check on subset; reproduce one published 3D thermal trend.
12. Sweep: ambient T, package/TIM resistance, stack height/tier count, burstiness, threshold.

## Killed
- I7 (Cool-Tier Shadow Experts). Worst novelty/effort ratio. Overlap with CRAFT replication and Tasa heterogeneity. Hardware answer to a software problem.

## Strongest residual objections
- Bundle: "Incremental placement heuristic on top of simulators, weak novelty over TACG/NeuroTAP, and no proof that lower temperature translates to better serving performance under realistic workload drift."
- I4: "Inference semantics changed by thermal rerouting; quality, fairness, stability unproven."

## Source citations from reviewer
- TACG (2606.01007), Gimbal (2606.15177), Patterns Behind Chaos (2510.05497), Tasa (2508.07252), Stratum (2510.05245), CoMeT (2109.12405), Voxel (2604.26821), CRAFT (2603.28768)
