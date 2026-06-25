# Gap Validation Results — NMP/MoE Expert Placement Thermal Risk

**Date opened**: 2026-06-24
**Status**: G0 complete (conditional pass) — awaiting two user decisions before G1

Use this file as the append-only execution log for `G0–G4`.

---

## G0 — Pre-flight inventory and simulator anchor

### Status
- complete (conditional pass) — 2026-06-25
- artifacts: `experiments/gap_validation/results/g0/{g0a_trace_coverage,g0b_substrate,g0c_smoke,g0d_wallclock,g0_summary}.json`
- runner: `experiments/gap_validation/run_g0.py`

### Inputs checked
- trace coverage: HF dataset `core12345/MoE_expert_selection_trace` (file listing only; contents gated)
- HotSpot: 6.0 (UVa, vendored at `experiments/gap_validation/external/HotSpot/`)
- CoMeT / Voxel: not exercised at G0 (HotSpot 3D grid model is sufficient for the substrate anchor)
- substrate model: locked at G0 — n_T=4 silicon tiers, n_B=16 banks per tier (4×4 grid), 2 mm pitch, 8×8 mm die, alternating Si (150 µm) + TIM (20 µm), ambient 45 °C
- power model: synthetic (uniform 0.1 W/bank for smoke; tier-0 corner burst 0.6 W with 30 % duty for transient anchor)

### Per-check results

| Check | Pass | Wall-clock | Notes |
|-------|------|-----------|-------|
| G0.a — trace coverage matrix (HF API listing) | **FAIL** | <2 s | 2/4 task families ≥ 500 reqs/model. `math` (HuggingFaceH4 / MATH-500) only **30 reqs/model**, unusable. `code` (livecodebench) **479 reqs/model**, marginal. `chat` (hellaswag, Llama-4 only) and `multilingual` (mmlu_ZH_CN + Chinese-SimpleQA) pass. English `mmlu` totals 51 627 reqs — viable substitute family. |
| G0.b — substrate plumbing | PASS | <1 s | `.flp` × 8 + `.lcf` (4 Si + 4 TIM) + 64-block `.ptrace` round-trip; HotSpot accepts. Stack height 0.66 mm, die 8×8 mm. |
| G0.c — HotSpot smoke-test (uniform 0.1 W/bank steady-state) | PASS | 0.32 s | Peak 47.92 °C on `B_t0_b05`, tier means C: t0=47.87 → t3=46.90 (monotone, top tier coolest as expected with HotSpot's heat sink at top). All silicon blocks ≥ ambient. |
| G0.d — solver wall-clock (1 s transient @ 1 ms steps, tier-0 corner burst) | PASS | 93.43 s | Target ≤ 180 s. Peak 49.48 °C max-over-run. Transient cost is the binding constraint; steady-state is ~1 s/eval and easily handles G1's 6 baselines × 4 families × 10 seeds. |

### Key observations
- **Simulator path is proven**. HotSpot 6.0 builds and runs on the locked substrate; both steady-state (~0.3 s) and 1 s of transient at 1 ms resolution (~93 s) are within budget. G3's closed-loop thermal-cap loop is feasible.
- **Critical config lessons** (preserved in code, recorded for posterity): `-detailed_3D on` is for *heterogeneous* TIM/TSV layers and hangs HotSpot when the TIM is uniform; with our homogeneous TIM the standard 3D grid model with `-grid_rows 16 -grid_cols 16` is the correct invocation. HotSpot prepends `layer_<N>_` to block names in `.steady`/`.ttrace`; metric parsers strip this and filter package/heatsink nodes via the `B_t` prefix.
- **Trace gate fails in its current form**, but the *coverage problem is bounded*: only the math family is fundamentally short. Three resolution paths are open (see "Blockers for G1").
- **Dataset content is gated**, not the file listing. G0.a only needed listing metadata, so this didn't block G0; it does block G1.

### Gate decision
- **CONDITIONAL PASS**. Simulator infrastructure (g0b/c/d) is green; trace coverage gate (g0a) fails on math, marginal on code. Per `GAP_VALIDATION_PLAN.md` G0 exit criterion ("if traces are too sparse or simulator path is broken, stop here"), the simulator path is *not* broken, but the trace coverage *is* too sparse for the 4-family grid as originally specified.

### Blockers for G1
1. **Task-family grid revision** — three options to resolve (user decision):
   - **(a) Drop `math`, keep `code` at 479, add English `mmlu` as a 4th family (51 627 reqs total).** Most defensible: keeps four families with diverse routing pressures.
   - **(b) Drop `math` and `code`, run on a 2-family grid (chat + multilingual).** Loses code-routing-specific evidence but keeps everything ≥ 500 reqs per the gate.
   - **(c) Relax the per-family request threshold to 100** and accept code+math as marginal. Requires explicit caveat in the paper that math evidence is single-benchmark and small-N.
2. **HuggingFace dataset access** — current `huggingface_hub` calls return 401 on file content. To unblock G1 the user must accept the dataset terms at `https://huggingface.co/datasets/core12345/MoE_expert_selection_trace` and either run `huggingface-cli login` or set `HF_TOKEN` for the venv. G0.a verified the listing is enough for the coverage matrix — content is needed only when actual routing traces are consumed.

### Next action
- Surface decisions (1) and (2) to the user; do **not** start G1 until both are resolved.
- Once resolved, G1 will reuse `experiments/gap_validation/thermal/{floorplan_gen,power_map_gen,hotspot_runner,metrics}.py` as-is and add `experiments/gap_validation/baselines/` + `run_g1.py`.

---

## G1 — Static thermal-risk comparison of NMP-native placements

### Status
- not-started

### Placements compared
- random
- even-odd / spread
- access-likelihood tiering
- frequency-only
- TACG-port (optional transferred control)

### Result table placeholder

| Task family | Best thermal baseline | Worst thermal baseline | Peak T | Time above threshold | Thermal violations | Notes |
|-------------|------------------------|------------------------|--------|----------------------|--------------------|-------|
| chat | | | | | |
| code | | | | | |
| math | | | | | |
| multilingual | | | | | |

### Key observations
- 

### Gate decision
- H1 supported / weak / failed

### Next action
- 

---

## G2 — Token-balance vs thermal-balance

### Status
- not-started

### Routing variants
- vanilla
- LPR-balanced
- aux-loss-free-balanced

### Result table placeholder

| Task family | Routing | Token Gini | Bank-activity Gini | Peak T | Comment |
|-------------|---------|------------|--------------------|--------|---------|
| chat | | | | | |
| code | | | | | |
| math | | | | | |
| multilingual | | | | | |

### Key observations
- 

### Gate decision
- H2 supported / weak / failed

### Next action
- 

---

## G3 — Thermal-cap serving sensitivity

### Status
- not-started

### Result table placeholder

| Task family | Placement | T_cap | Throughput | Throttle events | Avg TPOT | Collapse / unsafe? | Comment |
|-------------|-----------|-------|------------|-----------------|----------|--------------------|---------|
| chat | | | | | | |
| code | | | | | | |
| math | | | | | | |
| multilingual | | | | | | |

### Key observations
- 

### Gate decision
- system-level risk visible / weak / absent

### Next action
- 

---

## G4 — Final decision

### Hypothesis verdict
- H1:
- H2:

### Paper-direction verdict
- proceed to TACE / characterization-first / stop-and-rescope

### Notes
- 
