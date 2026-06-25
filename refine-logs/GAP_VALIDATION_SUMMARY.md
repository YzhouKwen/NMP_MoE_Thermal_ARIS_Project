# Gap Validation Summary — Decision Sheet

**Status**: not-started  
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

- G0 passed:
- G1 passed:
- G2 passed:
- G3 passed:

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
