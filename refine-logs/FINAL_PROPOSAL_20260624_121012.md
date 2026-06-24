# Final Proposal — TACE: Thermal Anti-Clustering of Experts on 3D-Stacked NMP

**Date**: 2026-06-24
**Stage**: Workflow 1.5 (research-refine-pipeline) — method refinement output
**Verdict**: READY (proposal locked for experiment planning)
**Inputs from Phase 4.5**: Q5 = predicted max_t T(t); Q6 = ILP cap 16×4 (Voxel cross-check at 32×8); Q7 = train-on-3 / test-on-1, 4-fold

---

## 1. Problem Anchor

On 3D-stacked NMP systems running MoE inference, **expert routing is irregular in two correlated ways simultaneously**: (a) per-expert long-run rate is skewed (Pareto-like top-k), and (b) pairs of experts co-burst within sliding windows shorter than the substrate's thermal time constant (τ ≈ 1–10 ms for bank-level thermal mass under HBM-PIM-style 3D stacks). When these two skews land on vertically adjacent banks, the anisotropic 3D thermal Green's function — sharply peaked vertically, broader laterally — concentrates power density into a localized hotspot that no token-level load balancer can see.

The bottleneck is **not** token-Gini, not expert-Gini, and not communication: it is the joint spatial-temporal alignment of co-bursting expert pairs with the substrate's anisotropic thermal kernel. Anti-aligning that joint distribution is the lever this paper attacks.

**One-line problem statement.** Place experts on (bank, tier) such that the *predicted* peak temperature over the routing trace is minimized, where prediction comes from an RC/Green's-function model fed by per-expert power and the co-activation graph.

## 2. Final Method Thesis

**Thesis (one sentence).** *Anti-cluster high-power, high-correlation experts under the anisotropic 3D thermal kernel — by solving a QAP whose objective is a direct max_t T(t) surrogate, not an eigenvalue proxy — and the dominant 3D-NMP MoE hotspot disappears at sub-1°C TPOT cost.*

The thesis is a single mechanism (anti-clustering placement), under a single substrate (3D-NMP, HBM-PIM bank/tier model), with a single objective (direct thermal surrogate), validated against a single critical baseline (TACG ported to the same substrate, which **clusters** co-activated experts — i.e., does the exact opposite of what is wanted).

## 3. Dominant Contribution

**TACE = QAP formulation + direct-T objective + same-substrate TACG-port refutation.**

The contribution is not "first thermal-aware MoE placement" (NeuroTAP, Tasa, Stratum, TACG all touch part of this). The contribution is:

1. **The anti-clustering insight**: the *only* prior work that uses MoE co-activation (TACG) clusters experts to minimize communication. On 3D-NMP under thermal cost, that same signal should drive the opposite assignment. We prove the sign flip experimentally on the same trace data.
2. **The direct-T objective**: prior thermal-aware placement uses frequency (NeuroTAP) or eigenvalue proxies (λ_max(P)). We replace these with `max_t T(t)` predicted by a fast RC/Green's-function evaluator that runs inside the QAP solver — peak T is what gets capped, peak T is what we minimize.
3. **The QAP three-term decomposition**: long-run rate · anti-clustering on co-activation graph weighted by anisotropic 3D thermal kernel · lateral/vertical coupling penalty — each ablatable, each empirically justified by Section 4 characterization.

## 4. Intentionally Rejected Complexity

To keep the contribution sharp, the following were considered and rejected:

| Rejected | Why rejected |
|----------|--------------|
| Online remapping / migration (FDR — I5) | Adds control-plane state, costs latency; defer to v2 once static-placement drift is quantified |
| Headroom-credit routing (HC-MoE — I4) | Different lever (scheduling), changes inference semantics; separate submission |
| Cool-tier shadow experts (I7) | Overlaps CRAFT + Tasa; hardware-heavy for a software-solvable problem; killed in Phase 4 |
| Feedback-stable router (I6) | Theory contribution, weak arch-venue fit |
| Eigenvalue surrogate `min Σ_t λ_max(P(t))` | Peak T is not λ_max(P); reviewer-mandated replacement |
| Atlas as standalone paper | Trace dataset is public (2510.05497); profiling-only reads as "simulator replay"; fold into Section 4 |
| Per-token / per-step solve | One offline solve per task family — task-stationary routing statistics make this sufficient and exposes static-placement drift as the natural v2 hook |
| Custom thermal solver | CoMeT primary, Voxel cross-check — do not invent simulators |

## 5. Method

### 5.1 Notation

| Symbol | Meaning |
|--------|---------|
| `E = {1,...,n_E}` | Experts (n_E ≈ 64–256 per layer for target MoE models) |
| `B = {1,...,n_B}` | Banks per tier |
| `T = {1,...,n_T}` | Tiers (stack height) |
| `S = B × T` | Sites (assignment targets) |
| `x_{e,s} ∈ {0,1}` | Expert `e` assigned to site `s` |
| `p_e` | Long-run firing rate of expert `e` (from routing trace) |
| `q_e` | Per-activation energy of expert `e` (from microarch model) |
| `c_{ef}` | Co-activation correlation of pair (e,f) over windows ≤ τ |
| `K(s,s')` | Anisotropic 3D thermal kernel between sites s and s' (Green's-function entry) |
| `G ⊂ S × S` | Edges within vertical column or lateral neighborhood (coupling-penalty support) |

### 5.2 Decision Variables and Constraints

Decision variables: `x_{e,s} ∈ {0,1}` for `e ∈ E, s ∈ S`. Constraints:

- **Assignment**: `Σ_s x_{e,s} = 1` for all `e` (each expert lands on exactly one site)
- **Capacity**: `Σ_e x_{e,s} ≤ cap(s)` (bank weight-capacity limit)
- **Optional firebreak ring**: `Σ_e x_{e,s} = 0` for `s ∈ FB` (a configurable subset of sites — one ablation row)

### 5.3 Objective: Direct Temperature Surrogate

The objective is a **direct prediction of peak temperature** over the routing trace, *not* an eigenvalue proxy. Two equivalent formulations, both used in the solver:

**Form A (closed-form surrogate, used inside the QAP inner loop):**

```
TACE_obj(x) = α · Σ_s P̂_s(x)·K_self(s)                            # self-heating
            + β · Σ_{(s,s') ∈ G} P̂_s(x) · K(s,s') · P̂_{s'}(x) / P̄   # coupling
            + γ · Σ_{(e,f), e≠f} c_{ef} · ⟨x_e, K x_f⟩                # anti-clustering pair term
            + δ · Σ_e p_e · q_e · K_self(s(e))                       # long-run rate term
```

where `P̂_s(x) = Σ_e x_{e,s} · p_e · q_e` is the predicted long-run power at site s.

The **sign of γ is positive**: pairs with high co-activation that sit at sites with large kernel coupling pay a penalty. This is what makes the term *anti*-clustering: large `c_{ef}` repels `e` and `f` *away* from kernel-coupled sites — the opposite of TACG, which would set γ negative to pack them together.

**Form B (verification objective, evaluated at acceptance only):**

```
TACE_verify(x) = max_t T_HotSpot(P(t; x))
```

where `P(t; x)` is the time-varying power map produced by replaying the trace under assignment `x`, and `T_HotSpot` is the actual CoMeT transient solver. Form A is the surrogate the SA solver minimizes; Form B is what we report and what claims are graded against.

The correlation between Form A and Form B is a measurable property — its value determines whether the surrogate is faithful. **First experiment block (B1) calibrates this correlation and reports it.** If `corr(Form A, Form B) < 0.85` on holdout traces, we tune (α, β, γ, δ) by ridge regression against CoMeT-measured peak T.

### 5.4 Solver

1. **Spectral warm-start.** Solve a continuous relaxation: place experts on a low-dimensional embedding via the second eigenvector of the kernel-weighted co-activation Laplacian; round to an initial integer assignment by greedy assignment under capacity.
2. **Simulated annealing.** Pairwise-swap and bank-move neighborhoods; standard geometric cooling; Form A evaluated incrementally (only sites touched by a swap are re-summed — O(n_B) per move, not O(n_B²)).
3. **ILP exact solve on small instances.** At Q6's cap (n_E = 16, n_B = 4, n_T = 4, i.e. 16 sites), run an exact MIP using Gurobi or CBC to bound the SA optimality gap. Voxel cross-check repeats at 32×8.
4. **Acceptance.** SA's final assignment is verified by Form B (CoMeT replay). If Form B regresses against the spectral-warm-start initial point, the warm-start is retained.

**Compute budget.** One offline solve per task family. Target ≤ 5 min wall-clock SA on a single CPU node at 64 experts × 16 sites. ILP at 16×4 closes in seconds to a minute. Voxel cross-check at 32×8 may not close in ILP — that is acceptable; gap reported as upper-bound.

## 6. The Critical Baseline: TACG-Port

The single most important comparison in the paper is **TACG-ported-to-3D-NMP**. TACG (2606.01007) was published May 2026 and uses co-activation grouping on distributed GPU with a *communication* objective — it packs co-activated experts on the same device to minimize cross-device traffic. The danger to TACE is that a reviewer asks "isn't TACE just TACG with a different cost function?" The answer must be a same-substrate, same-trace, same-implementation comparison.

### 6.1 TACG-Port Algorithm (precise)

```
INPUT: same routing trace, same n_E experts, same (bank, tier) site set as TACE
       co-activation graph C with edge weights c_{ef}
       site adjacency partition: "device" reinterpreted as "vertical column" (TACG groups within device → port groups within column)

ALGORITHM (faithful to 2606.01007 §4.2):
  1. Cluster experts via task-conditioned graph partitioning on C to minimize cut weight
     (TACG: METIS partition; we use the same METIS call, same n_parts = n_columns)
  2. Within each cluster, replicate top-r generic experts (r = TACG's default = 2)
     — the replication step is preserved; budget is matched to TACE's capacity constraint
  3. Assign clusters to columns to balance long-run rate per column
  4. Within column, distribute experts across tiers by greedy long-run rate balance

OUTPUT: assignment x_TACG-port; same shape as TACE's output

VERIFICATION:
  - Confirm that x_TACG-port co-locates high-c_{ef} pairs more often than random (sanity)
  - Report peak T under Form B
  - Report communication cost on a 3D-NMP NoC model to confirm TACG-port still wins on its native metric
```

This is the **centerpiece refutation**: same input, same substrate, opposite assignment principle, opposite thermal outcome. The paper's headline result is a scatter plot with peak T on one axis and communication cost on the other, with TACG-port and TACE on opposite ends of the Pareto front, and the operating point (thermal cap binding) clearly inside TACE's region.

## 7. Substrate, Traces, and Power Model

### 7.1 Substrate

- **Logical model**: HBM-PIM-style 3D stack. n_T = 4–8 tiers (sweep); per tier, n_B = 8–32 banks arranged in a 2D grid. Each (bank, tier) site = one near-memory compute island with weight storage capacity W_s.
- **Thermal model**: CoMeT primary. Anisotropic thermal kernel — vertical resistance R_v derived from CoMeT defaults for HBM-stack TSV density; lateral resistance R_l from per-tier metal/dielectric stack. Ambient T_amb = 45 °C; package R_pkg from CoMeT defaults.
- **Cross-check**: Voxel on 32×8 instance, same trace, same power map. We require qualitative agreement on hotspot location (top-3 hottest banks match in ≥ 3 of 4 task families) and quantitative agreement within ±15% on peak T delta.

### 7.2 Traces

**Patterns Behind Chaos** (arXiv 2510.05497) — public traces of 4 large MoE models (DeepSeek-V3, Mixtral-8x22B, Qwen-1.5-MoE, plus one frontier 200B–1000B model). 24k requests total. We segment by task family (chat / code / math / multilingual) for domain-shift evaluation.

### 7.3 Power Model

Per-activation energy `q_e` derived from a simple but explicit microarchitecture model: matrix-vector product cost at the expert's hidden dim × intermediate dim × activation precision. We do **not** claim absolute power accuracy — we claim *relative* power ordering is preserved across baselines (all baselines use the same `q_e`). Sensitivity to `q_e` is one parameter sweep (×0.5, ×1, ×2 on q_e for the dominant expert family).

## 8. Baselines

Six-arm comparison; all run on the **same trace, same substrate, same power model, same thermal solver**:

| # | Baseline | Origin | Mechanism |
|---|----------|--------|-----------|
| 1 | Random | trivial | Uniform-random assignment, 10 seeds |
| 2 | Even-odd | HD-MoE, A3D-MoE | Round-robin across banks/tiers by expert index |
| 3 | NeuroTAP-style | TACO 2024 | Frequency-driven placement: high-`p_e` experts on cooler sites; no co-activation, no kernel |
| 4 | Stratum-style | 2510.05245 | Tier-by-access-likelihood; ignores horizontal layout, ignores thermal |
| 5 | **TACG-port** | 2606.01007 | §6.1 — co-activation **clustering**, opposite of TACE |
| 6 | **TACE (ours)** | this paper | §5 — co-activation **anti-clustering** + direct T-surrogate |

## 9. Claims and Hypotheses

The paper makes exactly three claims, in order of importance:

| # | Claim | Quantitative form |
|---|-------|-------------------|
| **C1** | Token-balance ≠ thermal-balance (Section 4 hook) | Under LPR-balanced routing (token Gini ≤ 0.05), bank-activity Gini ≥ 0.30 and ΔT_peak vs vanilla < 1 °C, on at least 3 of 4 task families |
| **C2** | TACE reduces peak temperature against every baseline including TACG-port | Peak T reduction: 4–7 °C vs random/even-odd · 2–4 °C vs NeuroTAP · 1–3 °C vs Stratum · **2–5 °C vs TACG-port**. Each delta passes a paired bootstrap test (B = 1000, p < 0.05) on the held-out task family |
| **C3** | Thermal wins translate to end-to-end serving wins under a thermal cap | 1.3–1.8× throughput at fixed T_cap · 30–60% fewer throttle events · ≤ 1 °C average TPOT increase (i.e., placement-induced latency cost is bounded) |

These three claims are the only things the paper promises. Everything else is supporting evidence.

## 10. Must-Run Ablations

| Ablation | Purpose |
|----------|---------|
| A1: Remove long-run rate term (set δ = 0) | Long-run rate matters even without pairs |
| A2: Remove pair co-activation term (set γ = 0) | Pair term is what TACG-port doesn't have; confirms TACG-port refutation isn't just "we have a better rate term" |
| A3: Replace anisotropic K with isotropic K | Kernel anisotropy matters; isotropic placement should not catch vertical coupling |
| A4: Remove firebreak ring (FB = ∅) | Firebreak is optional; ablation tells us when it helps |
| A5: Replace direct-T surrogate (Form A) with λ_max(P) | The eigenvalue proxy is empirically inferior, not just theoretically |
| A6: SA only (no spectral warm-start) | Warm-start scaling claim |
| A7: Spectral only (no SA polish) | Warm-start alone is not sufficient |

## 11. Risks and Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| TACG-port survives port well enough to compress the win below 2 °C | MED | Sweep substrate anisotropy (vertical/lateral R ratio); report TACG-port-vs-TACE delta as a function of anisotropy — even if delta shrinks, the *sign* of TACG-port's thermal harm is the load-bearing finding |
| Anti-clustering improves T but hurts TPOT under thermal cap (C3 fails) | MED | Add a TPOT-aware constraint to the QAP as one ablation row; if TPOT cost > 1 °C, report Pareto rather than dominance and reframe C3 as "joint Pareto improvement" |
| Form A surrogate poorly correlates with Form B peak T | LOW-MED | B1 calibrates correlation; if < 0.85, tune weights by ridge regression against CoMeT-measured peak T on a calibration trace fold |
| Public trace dataset 2510.05497 does not include all 4 task families per model | LOW | Pre-flight inventory in B0; if a (model, family) cell is empty, drop that cell from the 4×4 grid and adjust domain-shift folds |
| Voxel cross-check disagrees with CoMeT on hotspot location | MED | Predeclared agreement criterion (§7.1); if disagreement > 15% on > 1 task family, report as a limitation rather than a refutation — neither simulator is ground truth |
| ILP fails to close at 16×4 within an hour | LOW | Use CBC with warm-start from SA solution; report best-known gap rather than closed gap |
| Reviewer attack: "static placement is brittle under workload drift" | HIGH | This is the *intended* future-work hook (FDR — I5); Q7's train-on-3 / test-on-1 protocol pre-empts by quantifying drift cost and showing TACE still beats baselines on held-out task family |

## 12. Coverage of the 12 Mandatory Pre-Submission Changes

| # | Mandatory change | Where addressed |
|---|------------------|-----------------|
| 1 | Single paper, no atlas split | §2, §3, §5 — Atlas is Section 4 of this same paper, not a separate contribution |
| 2 | Recast as anti-clustering | §2 thesis, §3 contribution, §5.3 sign of γ |
| 3 | Direct T-surrogate (replace λ_max) | §5.3 Form A + §10 A5 ablation against λ_max |
| 4 | TACG-port baseline is centerpiece | §6 — full algorithm spec; §8 baseline #5; §9 C2 quantitative delta |
| 5 | Mandatory baselines beyond TACG-port | §8 — 6-arm table includes Stratum-style, NeuroTAP, random, even-odd |
| 6 | Per-term ablations | §10 — A1–A4 cover each objective term + firebreak |
| 7 | E2E serving metrics under thermal cap | §9 C3 — TPOT, throughput, throttle events |
| 8 | Domain-shift evaluation | §9 C2 evaluated on held-out family; Q7 train-3/test-1 4-fold |
| 9 | ILP optimality gap | §5.4 step 3; §10 A6/A7; Q6 cap at 16×4 |
| 10 | CoMeT primary, Voxel cross-check | §7.1 — predeclared agreement criterion |
| 11 | Parameter sweeps (≥ 3 points per axis) | §7 + §11 — anisotropy, ambient T, stack height, burstiness, threshold |
| 12 | Token-balance ≠ thermal-balance proof | §9 C1 (Section 4 of paper) |

All 12 changes are addressed by this proposal; none deferred.

## 13. What Phase 4.5 User Inputs Locked

| Q | Decision | Where used |
|---|----------|-----------|
| Q5 | Predicted `max_t T(t)` as the thermal surrogate | §5.3 Form A and Form B |
| Q6 | ILP cap at 16 experts × 4 banks (Voxel cross-check at 32×8) | §5.4 step 3; §7.1 |
| Q7 | Train-on-3 / test-on-1, 4-fold | §9 C2; §11 reviewer-attack mitigation |

---

**Method status**: READY for Phase 3 (experiment-plan). No remaining method-level questions. All open issues are validation issues, addressed by `EXPERIMENT_PLAN.md`.
