# Refinement Report — CATEP → TACE

**Date**: 2026-06-24
**Stage**: Workflow 1.5, research-refine output
**Verdict**: READY

## What the Method Looked Like Before Refinement

The original headline (I3 / **CATEP** — Co-Activation Thermal Expert Placement) used:

- An **eigenvalue surrogate**: `min Σ_t λ_max(P(t))` as a proxy for peak temperature.
- A **clustering framing**: co-activation-aware placement, terminologically symmetric with TACG (May 2026), distinguished only by cost function.
- A **standalone Atlas paper** (I1) preceding it as a measurement contribution.
- **No mandated TACG-port comparison.**
- **No domain-shift protocol** beyond "evaluate on traces."
- **Bundled HC-MoE (I4) and Cool-Tier (I7)** still alive in the contribution stack.

GPT-5.4's Phase 4 review flagged five of these as submission blockers.

## What Changed in This Refinement Round

| Dimension | Before | After |
|-----------|--------|-------|
| Objective | `Σ_t λ_max(P(t))` | Form A (direct T surrogate in QAP) + Form B (`max_t T_HotSpot` verified at acceptance) |
| Framing | Co-activation-aware placement | **Anti-clustering** — sign of γ is positive; pair term *repels* co-bursting experts |
| Critical baseline | None mandated | TACG-port — same substrate, same trace, faithful port of 2606.01007 §4.2 |
| Paper scope | Atlas (standalone) + CATEP + HC-MoE + Cool-Tier | Single paper: Atlas as §4, TACE as §5–7. HC-MoE deferred. Cool-Tier killed. |
| Drift treatment | Implicit | Train-on-3 / test-on-1, 4-fold (Q7) |
| Evaluation surface | Peak T only | Peak T + TPOT + throughput + throttle events under thermal cap |
| Optimality framing | SA only | Spectral warm-start → SA → ILP gap bound at 16×4 (Q6) |
| Cross-simulator | CoMeT only | CoMeT primary + Voxel cross-check at 32×8 |
| Term decomposition | Implicit | Four named terms (long-run rate, anti-clustering pair, coupling, firebreak) — each ablatable |
| Surrogate fidelity | Unmeasured | B1 calibrates Form A ↔ Form B correlation; ridge fit fallback if < 0.85 |

## Dominant Contribution — Sharpened

**Before:** "co-activation-aware thermal expert placement." Reviewer translation: "TACG with a thermal cost."

**After:** "**Anti-clustering** of high-correlation experts under the anisotropic 3D thermal kernel, with a direct-T objective, refuted against a same-substrate TACG port." Reviewer translation: "TACG and TACE use the same signal in opposite directions; we measure the sign flip and show TACG-port makes hotspots worse."

The sharpening is operational: a same-substrate experiment can falsify or confirm the sign-flip claim. CATEP's original framing did not expose a falsifiable refutation.

## Complexity Intentionally Rejected

Listed in `FINAL_PROPOSAL.md` §4. The most important rejections:

- **Online remapping (FDR / I5).** Defer to v2; static-placement drift quantified in Q7 protocol becomes the natural hook.
- **Headroom-credit scheduling (HC-MoE / I4).** Different lever; separate submission.
- **Cool-Tier shadow experts (I7).** Killed by Phase 4 review.
- **Per-token / per-step solve.** One offline solve per task family; the drift hook is left explicit, not engineered away.

The principle: keep the paper to one mechanism. Every additional knob added would compress one of the claims (peak T, TPOT, throttle rate) below significance.

## Frontier Primitive Necessity

The method uses no LLM / VLM / Diffusion / RL primitive at its core. The MoE workload exists because of LLMs, but the placement algorithm is a QAP — a classical combinatorial primitive. **No frontier necessity test required.** This is intentional and should be defended in the paper: the contribution is the right cost function and the right baseline refutation, not a new optimizer.

## Risks Carried Forward to Experiment Planning

1. TACG-port may not lose by enough at low anisotropy. **Mitigation moved to experiment plan B8 (anisotropy sweep).**
2. Anti-clustering may cost TPOT. **Mitigation moved to experiment plan B5 (thermal-cap E2E).**
3. Form A may not correlate well with Form B. **Mitigation moved to experiment plan B1 (calibration with ridge fallback).**

## Method Status

**READY.** No remaining method-level questions. The experiment plan is the next gate.

## Reviewer Concerns Status Summary

| Concern | Resolution |
|---------|-----------|
| Eigenvalue surrogate is wrong physics | RESOLVED — Form A + Form B |
| TACG natural attack | RESOLVED — §6 TACG-port + headline figure |
| Atlas as standalone | RESOLVED — Atlas folded to §4 |
| Drift attack on static placement | RESOLVED — Q7 protocol |
| Thermal-only wins insufficient | RESOLVED — C3 promoted to required claim |
| HC-MoE bundling | RESOLVED — demoted to separate submission |
| I7 overbuilt | RESOLVED — killed |
| Form A surrogate fidelity | HANDED TO EXP PLAN (B1) |
| TPOT cost of anti-clustering | HANDED TO EXP PLAN (B5) |
| Voxel-CoMeT disagreement | HANDED TO EXP PLAN (B7) |
| Trace inventory completeness | HANDED TO EXP PLAN (B0) |
| Parameter sweep coverage | HANDED TO EXP PLAN (B8) |

All Phase 4 method-level blockers cleared. Validation-level blockers explicitly tracked in `EXPERIMENT_PLAN.md`.
