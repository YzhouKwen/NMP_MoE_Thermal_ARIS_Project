# Gap Validation Summary — Decision Sheet

**Status**: G0 complete (conditional pass) — 2026-06-25; awaiting two user decisions before G1
**Owner stage**: pre-method validation

## Questions this summary must answer

1. Do current NMP-style expert placements create a real thermal disadvantage?
2. Which placement heuristic is thermally worst, and why?
3. Does that disadvantage escalate into thermal risk or thermal-cap degradation?
4. Is the evidence strong enough to justify a new thermal-aware expert placement paper?
5. Should TACE remain the next step, or should the paper be reframed?

## Final Answers

### 1. Real thermal disadvantage?
- pending

### 2. Thermally worst heuristic?
- pending

### 3. Thermal risk / cap degradation?
- pending

### 4. Evidence strong enough for a paper?
- pending

### 5. Recommended next step
- pending

## Decision Template

Choose exactly one after `G4`:

- **Proceed to TACE**
  - Use if thermal disadvantage is clearly supported and the evidence is strong enough that a corrective placement method is justified.

- **Reframe as characterization-first**
  - Use if thermal disadvantage is real, but escalation into risk is weak, conditional, or insufficient for a strong method-first paper.

- **Stop / re-scope**
  - Use if thermal disadvantage is weak, inconsistent, or not consequential enough.

## Evidence Checklist

- G0 passed: **conditional** (simulator path PROVEN — g0b/c/d; trace coverage gate FAILS as specified — only 2/4 families ≥ 500 reqs). Detailed verdict and per-check artifacts in `GAP_VALIDATION_RESULTS.md` § G0.
- G1 passed: pending (blocked on two user decisions — see below)
- G2 passed:
- G3 passed:

## G0 provisional verdict (2026-06-25)

- **Simulator infrastructure**: ready. HotSpot 6.0 vendored, 3D-stack `.lcf` validated, steady-state ≈ 0.3 s / placement, transient 1 s @ 1 ms ≈ 93 s ≤ 180 s target. G1/G2/G3 are computationally feasible on the locked substrate (4 tiers × 16 banks).
- **Trace coverage**: HF dataset listing is sufficient to map (model × task-family) request counts. Result: `chat` and `multilingual` pass ≥ 500; `code` is marginal (479); `math` (MATH-500) is unusable at 30 reqs/model. English `mmlu` totals 51 627 reqs and is a viable 4th-family substitute.
- **Recommended verdict**: **conditional pass** — infrastructure does not block G1, but the 4-family grid as originally specified does. Two decisions are needed before G1 launches:
  1. Task-family grid revision: (a) drop math, add English `mmlu`; or (b) drop math + code, run 2-family; or (c) relax threshold to 100 reqs/family. Recommend (a).
  2. HuggingFace dataset access: accept gated terms + set `HF_TOKEN` for the venv. Required for G1 to read trace contents (G0 only needed the listing).

## Recommended follow-up if TACE proceeds

- Reopen `FINAL_PROPOSAL.md` and `EXPERIMENT_PLAN.md`
- Rewrite them so TACE is explicitly framed as the response to a validated thermal disadvantage, and specify whether the paper leans on inefficiency alone or on full thermal risk
- Promote the strongest G1/G2 evidence into the paper's motivation / Section 4

## Recommended follow-up if characterization-first

- Reduce method ambition
- Turn the paper into:
  - current NMP placements leave thermal disadvantage
  - routing/load balance metrics miss that disadvantage
  - some regimes may escalate into risk, but not strongly enough for a method-first claim
  - thermal-aware placement becomes future work or short add-on
