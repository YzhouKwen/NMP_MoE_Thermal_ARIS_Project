# Raw Idea Pool — Thermal-Aware MoE on 3D-Stacked NMP

**Date**: 2026-06-23
**Generator**: GPT-5.4 (Codex MCP, xhigh reasoning)
**Direction**: full lever sweep across placement, scheduling, remapping, throttling, architecture co-design.
**Baselines to beat**: Tasa, Sieve, HD-MoE, NeuroTAP, ViBE, LPR.

## Lever Coverage

| ID | Title | Primary Lever | Risk | Effort | Contribution |
|----|-------|---------------|------|--------|--------------|
| I1 | Routing-to-Temperature Atlas for 3D MoE | measurement | LOW | 2-3 wk | empirical/diagnostic |
| I2 | Balanced Tokens, Unbalanced Heat | counter-result | LOW-MED | 1-2 wk | empirical |
| I3 | Correlation-Aware Thermal Expert Placement (CATEP) | placement | MED | 3-5 wk | method |
| I4 | Headroom-Credit MoE Scheduler (HC-MoE) | scheduling | MED | 4-6 wk | method |
| I5 | Forecast-Driven Expert Remapping (FDR) | remapping | HIGH | 1-2 mo | method+system |
| I6 | Feedback-Stable Thermal Reroute Control | thermal-control | MED | 1-2 mo | method+theory |
| I7 | Cool-Tier Shadow Experts | arch-codesign | MED | 1-2 mo | architecture |
| I8 | Thermal Firebreak Banks for MoE | arch-codesign | MED-HIGH | 3-5 wk | architecture |

## I1 — Routing-to-Temperature Atlas for 3D MoE
**Summary**: First systematic measurement study mapping MoE routing-skew shape (top-k Gini, bimodal-tail mass, temporal burst length) to bank/tier-level peak T, lateral/vertical gradients, and sustained-hotspot duration on a 3D-NMP substrate.
**Mechanism**: Replay Mixtral / Qwen3-MoE / DeepSeek-V3 / GPT-OSS routing traces over a fixed expert→bank assignment in a 3D-stacked HBM-PIM model; convert per-bank activity to a power trace; feed CoMeT/MFIT for transient T fields; correlate against routing statistics.
**Hypothesis**: Three regimes emerge — (a) low-skew/uniform: small T excursions, (b) bimodal-skew: persistent vertical hot stripe spanning 2-4 banks per tier, (c) temporal-burst: transient peaks > 5 °C above mean within 100 ms windows. Predictive T peak model from routing stats achieves R² > 0.8.
**Differentiators**: Tasa is dense LLM, no expert skew; Sieve/HD-MoE thermal-blind; NeuroTAP is generic DNN; ViBE rack-level not bank-level. **Atlas itself does not exist anywhere.**
**Min Experiment**: 1 GPU for trace generation (16-token batches × 4 models × 2 prompt sets). Voxel or HBM-PIM analytical model + CoMeT (HotSpot wrapper). Compute: ~12 GPU-hr trace gen + CPU-hours for thermal solve.
**Top objection**: "Why is this more than a measurement paper?" — Response: We use the atlas to derive a *closed-form predictor* T_peak = f(routing-skew, placement) and a placement-feasibility theorem; this transforms it from data to actionable design law.

## I2 — Balanced Tokens, Unbalanced Heat
**Summary**: A counter-result that algorithmic load-balancing (LPR, Switch-style aux loss) achieves uniform token counts but *fails* to eliminate thermal hotspots when expert→bank placement is fixed, due to per-token cost heterogeneity (FFN-up vs gate vs activation memory) and burst-correlation across layers.
**Mechanism**: Replay LPR-balanced vs vanilla routing traces; show that token uniformity (Gini ≤ 0.05) coexists with bank-level activity Gini ≥ 0.3 because compute-energy-per-token varies 1.4-2.1× across experts and tier-vertical co-location amplifies thermal coupling.
**Hypothesis**: ΔT_peak (LPR vs vanilla) < 1 °C in steady state on 4-tier HBM-PIM, while runtime claim by LPR is "near-uniform load." Effective thermal entropy stays within 5% of imbalanced baseline.
**Differentiators**: LPR claims load balance; nobody has measured the *thermal* effect. Forces a clean separation of "physical" vs "count" balance.
**Min Experiment**: Same trace pipeline as I1, plus LPR baseline. ~6 GPU-hr.
**Top objection**: "Could LPR + uniform random placement fix this?" — Response: Add a third arm with placement randomization, show vertical coupling still produces > 2 °C residual hotspot due to stack physics independent of routing.

## I3 — Correlation-Aware Thermal Expert Placement (CATEP)
**Summary**: Offline expert→bank/tier mapping that minimizes peak T by jointly considering (a) per-expert long-run activation rate, (b) cross-expert temporal co-activation correlation, (c) 3D thermal coupling matrix from CoMeT.
**Mechanism**: Formulate as quadratic assignment: minimize Σ_t λ_max(P(t)) where P is the bank power matrix, with constraints from co-activation graph and thermal Green's function. Solve via simulated annealing + thermal-aware spectral relaxation. Apply once per task family using profiled traces.
**Hypothesis**: 4-7 °C peak-T reduction vs. random/even-odd placement; 1-3 °C reduction vs. NeuroTAP (which ignores expert co-activation graph); negligible TPOT change.
**Differentiators**: NeuroTAP places generic DNN tensors by access frequency, no expert co-activation; ViBE is rack-level GPU placement, not 3D bank-level; HD-MoE places by HBM-access optimization, thermal-blind. **Co-activation-aware vertical placement is unique.**
**Min Experiment**: Trace pipeline + QAP solver + CoMeT eval. Compare 5 placements: random, even-odd (2507.19142), NeuroTAP-style frequency, ViBE-style hot-cold, CATEP. ~20 CPU-hr solver + thermal sim.
**Top objection**: "Static placement breaks under task drift." — Response: That is exactly the motivation for I5; CATEP handles persistent skew, I5 handles drift. Show drift sensitivity curves to justify boundary.

## I4 — Headroom-Credit MoE Scheduler (HC-MoE)
**Summary**: Online scheduler that issues expert-token batches based on a per-bank thermal-headroom credit (T_max - T_now)/T_max, deferring or migrating tokens before a thermal violation rather than reacting to throttling.
**Mechanism**: Each bank publishes a credit; router multiplies token routing weights by credit-weighted gates; if bank credit < threshold, redirect to backup expert via top-k re-selection or copy-cast to cool replica (links to I7). Avoids reactive DVFS/throttle.
**Hypothesis**: Sustained-hotspot duration ↓ 60-80% vs. reactive throttling at iso-throughput; TPOT degrades < 3% under bursty workloads where Sieve/HD-MoE see > 10% throttle penalty.
**Differentiators**: Sieve splits exec GPU↔PIM by arithmetic intensity (thermal-blind); HD-MoE schedules by util; Tasa uses op-type partitioning, not expert-level. **Credit-driven proactive routing on MoE is unique.**
**Min Experiment**: Cycle-approx 3D-NMP simulator + thermal RC model in inner loop + routing replay. Sweep workload bursts. ~30 GPU-hr equivalent (mostly CPU sim).
**Top objection**: "Token quality degrades under credit gating." — Response: Bound credit-induced top-k swaps to top-2k options; measure perplexity drift < 0.5 with full evaluation on Mixtral.

## I5 — Forecast-Driven Expert Remapping (FDR)
**Summary**: Online expert→bank migration triggered by short-horizon routing forecasts and bank thermal trajectories; uses task-conditioned routing predictability (#19) and predictive expert caching (#13) to amortize migration cost.
**Mechanism**: Lightweight Markov/transformer on routing-decision history predicts next-100-ms hot-expert set; Kalman filter on thermal sensors predicts next-1-s peak; controller solves migration cost vs. predicted ΔT benefit; migration uses copy-on-write between tiers via TSV-bandwidth budget.
**Hypothesis**: Under task-mix drift, FDR maintains peak T within 3 °C of CATEP-oracle while static CATEP drifts by 8-12 °C; migration cost amortized over > 10⁴ tokens per move.
**Differentiators**: Edge MoE migration (#28) is rack-scale; ExpertFlow (#13) caches but doesn't move; Sangam (#4) is CXL-level. **Bank-level online migration with thermal forecast is empty.**
**Min Experiment**: Build forecast model + sim controller + migration cost model. Validate on 4 task-mix drift scenarios. Higher risk because migration physics requires careful TSV bandwidth modeling.
**Top objection**: "Migration cost dominates benefit." — Response: Provide closed-form break-even: migration is worth it when forecast horizon × predicted ΔT > c·migration_overhead, with c calibrated empirically.

## I6 — Feedback-Stable Thermal Reroute Control
**Summary**: Closes the routing → power → temperature → router loop with a control-theoretic guarantee against the positive-feedback amplification of skew (G7), where throttling hot experts can shift routing back toward them via latency-aware load balancing.
**Mechanism**: Model as MIMO discrete-time controller; derive stability margin and oscillation conditions; design a damping policy on the routing soft-max temperature that prevents the hot-bank-throttle-then-reroute oscillation observed in naive thermal-aware routers.
**Hypothesis**: Naive thermal-aware routing exhibits 2-3% throughput oscillation amplitude with 3-5 s period; damped variant reduces amplitude < 0.5% and improves mean throughput 2-4%.
**Differentiators**: No prior MoE thermal-router has formal stability analysis. Tasa runs at op-type granularity, no feedback. ViBE is offline binning. **Stability-theoretic MoE thermal controller is unique.**
**Min Experiment**: Build closed-loop sim, demonstrate oscillation in baseline, prove + demo damped controller. Theory + simulation paper, light on physical eval.
**Top objection**: "Real systems don't oscillate that visibly." — Response: Show a regime parameter (load × thermal time constant) where oscillation appears; confirm naive prior schedulers (Sieve+throttle, HD-MoE+DVFS) fall in this regime.

## I7 — Cool-Tier Shadow Experts
**Summary**: Architecture co-design that adds a thin "cool tier" — a memory tier with extra heatsink budget but lower compute/BW — hosting low-frequency-but-burst experts as shadows of hot experts; routing offloads bursts to the cool tier under thermal pressure.
**Mechanism**: Heterogeneous 3D stack: top tier near logic die (high BW, hot), one or two cool tiers further from heatsink-coupled side; runtime decides which expert instance fires per token based on thermal state. Differs from Tasa by using *expert duplication*, not op-type partitioning.
**Hypothesis**: 3-5 °C peak-T reduction at < 5% throughput loss; storage overhead 10-20% (only hot experts duplicated); strictly dominates Tasa on MoE workloads.
**Differentiators**: Tasa partitions by op type (compute vs attention), not duplication; HD-MoE uses TP/EP, not heterogeneous tiers; Sieve splits GPU/PIM. **Expert-duplication-based heterogeneous 3D stack is empty.**
**Min Experiment**: DSE on tier configurations using Voxel + thermal solver; trace replay; sweep duplication ratio. Hardware proposal validated in simulation only.
**Top objection**: "Storage overhead is unacceptable." — Response: Duplicate only the top-K hot experts identified by routing analysis (typically K ≤ 8 of N=64), bounding overhead.

## I8 — Thermal Firebreak Banks for MoE
**Summary**: Architecture co-design that reserves a small set of "firebreak" banks with mostly-idle (low-power) workloads between high-activity expert banks, breaking lateral and vertical thermal coupling paths.
**Mechanism**: Extend the bank power matrix: hot experts mapped only to banks with at least one firebreak neighbor; firebreak banks hold cold experts, KV-cache fragments, or are gated. Reduces thermal coupling Green's function magnitude between hot regions.
**Hypothesis**: Lateral coupling reduced 30-50% per firebreak ring; peak T drops 2-4 °C with < 5% capacity overhead.
**Differentiators**: NeuroTAP places by frequency without explicit isolation; nobody has applied firebreak-style placement to MoE on 3D-NMP. Architectural-level isolation is novel for this substrate.
**Min Experiment**: Sweep firebreak ratio in CATEP optimization with thermal coupling matrix; measure trade-off. Can be combined with I3.
**Top objection**: "Wastes capacity." — Response: Firebreak banks still hold cold experts (<5% activation rate); marginal capacity loss but dominant thermal benefit.

## Top-3 Recommendation (per GPT-5.4 review)

1. **I1** — safest defensible wedge; G1 is open; gives the field its first measurement substrate.
2. **I3** — clean mechanism, MoE-specific novelty, beatable baseline (NeuroTAP), QAP solvable.
3. **I4** — best balance of runtime novelty and pilotability; closes part of the routing→thermal→policy loop.

Combined narrative: I1 is the foundation, I3 is the offline mechanism, I4 is the online mechanism. Together they form a coherent thermal-aware MoE-NMP framework.
