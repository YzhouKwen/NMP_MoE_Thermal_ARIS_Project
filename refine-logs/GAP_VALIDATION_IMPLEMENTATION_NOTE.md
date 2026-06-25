# Gap Validation Implementation Note

**Date**: 2026-06-24  
**Purpose**: constrain how Claude should implement the gap-validation experiments  
**Status**: active implementation guidance

## Core Rule

For gap validation, Claude must **build on top of existing open-source thermal analysis codebases** and integrate them into this project. Claude should **not** create a thermal simulator from scratch.

This is a hard implementation preference, not a soft suggestion.

## Primary Implementation Home

All experiment-driving code, wrappers, glue logic, result tables, and analysis scripts should live in:

- `H:\PhD_Workspace\Research_Projects\NMP_MoE_Thermal_ARIS_Project`

This project is the source of truth for:

- experiment scripts
- trace preprocessing
- placement baseline implementations
- thermal input generation
- metric collection
- result summaries

External repositories should be treated as:

- **reference implementations**
- **solver/tool backbones**
- **integration targets**

They should **not** become the main working repo for this paper.

## Required Local Code Directory

All **new experiment code for this gap-validation stage** must be placed under:

- `H:\PhD_Workspace\Research_Projects\NMP_MoE_Thermal_ARIS_Project\experiments`

More specifically, Claude should create and use a dedicated subtree:

- `H:\PhD_Workspace\Research_Projects\NMP_MoE_Thermal_ARIS_Project\experiments\gap_validation`

Claude should **not** scatter experiment scripts across:

- project root
- `refine-logs/`
- external open-source repositories

Those locations may contain:

- notes
- plans
- solver backbones
- reference implementations

But the actual experiment-driving code added for this project should be centralized under `experiments/gap_validation/`.

## Hard Rule: Where Core Development Code Must Live

For this stage, the phrase **"core development code"** means:

- code that Claude newly writes for this project,
- code that Claude modifies for this project's experiment logic,
- wrapper / bridge / adapter code built on top of open-source thermal tools,
- patched integration code that this project itself must maintain,
- baseline placement implementations used in the gap-validation study.

All such **core development code must live under**:

- `H:\PhD_Workspace\Research_Projects\NMP_MoE_Thermal_ARIS_Project\experiments\gap_validation\`

This is a hard requirement.

Claude must **not** place core development code in:

- the project root
- `refine-logs/`
- unrelated directories under the project
- the original external open-source repository as the primary place of modification

If Claude writes or changes code that the paper's experiments depend on, that code must be traceable to `experiments/gap_validation/`.

## Hard Rule: Where Open-Source-Based Development Must Live

When Claude develops **based on** an open-source project such as HotSpot, the project-local code split must be:

1. **External source code**
   - original upstream or minimally vendored code
   - stored separately from the project's own logic

2. **Project-owned development code**
   - wrappers
   - adapters
   - input generators
   - output parsers
   - patched runners
   - experiment orchestration
   - metric extraction

All **project-owned development code** must live under:

- `experiments/gap_validation/`

This includes code that is conceptually "based on HotSpot" or "based on CoMeT".  
Being based on an external project does **not** justify placing the project's maintained logic outside `experiments/gap_validation/`.

## Allowed Split Between External Code and Project Code

The allowed split is:

- `experiments/gap_validation/external/`
  - optional location for vendored or locally patched copies of external upstream code, when unavoidable

- `experiments/gap_validation/thermal/`
  - project-owned thermal wrappers and integration logic

- `experiments/gap_validation/baselines/`
  - project-owned placement baseline implementations

- `experiments/gap_validation/utils/`
  - project-owned shared utilities

- `experiments/gap_validation/run_g*.py`
  - project-owned execution entrypoints

If a file is part of the project's maintained experimental logic, it belongs in one of the project-owned locations above.

## What Claude Must Assume by Default

Unless the user explicitly overrides this later, Claude must assume:

- external solver/tool repositories remain external,
- this project's maintained implementation lives in `experiments/gap_validation/`,
- all new glue logic and experiment logic belongs there,
- all baseline implementation code belongs there,
- all thermal integration code belongs there.

## Recommended Substructure

Claude should prefer a clean structure such as:

- `experiments/gap_validation/run_g0.py`
- `experiments/gap_validation/run_g1.py`
- `experiments/gap_validation/run_g2.py`
- `experiments/gap_validation/run_g3.py`
- `experiments/gap_validation/baselines/`
- `experiments/gap_validation/thermal/`
- `experiments/gap_validation/results/`
- `experiments/gap_validation/utils/`

The exact filenames may differ, but the principle is fixed:

- baseline logic stays under `experiments/gap_validation/`
- thermal wrappers stay under `experiments/gap_validation/`
- run scripts stay under `experiments/gap_validation/`
- generated experimental outputs should be written to a results subdirectory under that same subtree, unless the project later standardizes a separate results root

## Thermal Backbone Policy

### Required principle

Claude must prefer:

1. **wrapping or calling an existing thermal solver**
2. **modifying existing interfaces / input generators / parsers**
3. **adding project-specific glue code**

Claude must avoid:

1. implementing a brand-new thermal solver
2. inventing a new RC solver from scratch unless explicitly required later
3. replacing an existing open-source thermal engine with a custom approximate model as the primary path

## Preferred Open-Source Thermal Foundations

### Tier 1: preferred primary backbone

- **HotSpot** or **HotSpot-compatible thermal flow**

Reason:

- architecture community familiarity
- easy to justify in paper writing
- suitable for repeated trace-driven comparison
- aligned with the project's current thermal-analysis direction

Claude should first look for:

- an existing local HotSpot checkout
- a project-local HotSpot wrapper
- an input-generation path that can produce floorplan/power traces for HotSpot-style runs

### Tier 2: preferred cross-check / secondary path

- **CoMeT**
- **Voxel**

Use:

- as secondary validation if locally available
- as cross-check path if integration cost is reasonable

Do not block gap validation on full CoMeT/Voxel integration if HotSpot-compatible evaluation can be made to work first.

### Tier 3: non-primary high-fidelity reference

- **ANSYS Fluent**

Policy:

- do not use as the first implementation target for this stage
- do not require Fluent to unblock gap validation
- only mention as a possible later high-fidelity reference path

## Implementation Strategy for Claude

Claude should follow this order:

1. **Inspect this repo first**
   - look for existing thermal placeholders, wrappers, scripts, or input directories
   - especially under `experiments/`, `src/`, `docs/`, and any HotSpot-related folders

2. **Inspect locally available open-source thermal repos**
   - find a usable HotSpot or HotSpot-compatible codebase already present on disk
   - prefer adapting an existing local checkout over downloading/building a new stack

3. **Create glue code inside this project's `experiments/gap_validation/` subtree**
   - trace → placement assignment → power map / power trace
   - power trace → thermal solver input
   - thermal solver output → metrics table

4. **Keep solver logic external**
   - do not copy large external solver internals into this repo
   - wrap them, call them, or generate their inputs

## Baseline Implementation Policy

For the gap-validation stage, Claude does **not** need to fully reproduce every prior paper's full system stack.

Claude should implement:

- **paper-faithful placement proxies**

This means:

- if a paper defines a clear placement rule, implement that rule faithfully
- do not attempt full-stack reproduction unless the repository is already available and trivial to reuse

### Acceptable baseline proxy implementations

- **Even-odd / spread placement**
  - simple deterministic placement rule
  - intended to approximate A3D-MoE-style spread placement behavior

- **Access-likelihood tiering**
  - compute access/use statistics from traces
  - map hotter/more frequently used experts according to tier preference
  - intended to approximate Stratum-style access-likelihood placement

- **Frequency-only placement**
  - rank by long-run expert activation frequency
  - place by cooler/favored sites without pairwise co-burst logic

- **TACG-port**
  - only if needed as a transferred opposite-sign control
  - not required to be the first implementation target

## What Claude Must Not Do

Claude must not:

- invent a custom thermal simulator because integration looks inconvenient
- bypass open-source thermal tools and claim a custom approximation is equivalent
- spend the first implementation pass on method-heavy TACE engineering before validating the thermal premise
- make TACG-port the only meaningful baseline for gap validation

## Minimum Deliverable for Gap Validation

The first usable implementation only needs to support:

1. loading a trace subset
2. generating several fixed expert placements
3. converting those placements into a thermal-analysis input for an open-source thermal backbone
4. computing:
   - peak temperature
   - time above threshold
   - hotspot concentration
   - if feasible, thermal-cap throughput/throttle metrics

That is sufficient for:

- `G0`
- `G1`
- and likely `G2`

It is not necessary to complete the full TACE solver stack before this.

## If Multiple Thermal Codebases Are Available

Claude should choose according to this priority:

1. easiest local HotSpot-compatible path that is actually runnable
2. project-consistent path that can be defended in the paper
3. secondary cross-check path if incremental effort is reasonable

Claude should explicitly record:

- which codebase was selected
- what wrappers or adapters were added
- what was reused vs newly written
- what was deferred
- which files were created under `experiments/gap_validation/`

## Expected Output from Claude Before Coding Deeply

Before major implementation, Claude should briefly state:

1. which local open-source thermal repo it will build on
2. where in this project it will place integration code
3. which baselines will be implemented as paper-faithful proxies
4. what the first runnable `G0/G1` path will be

## Summary Rule

For this stage:

- **reuse and integrate open-source thermal analysis code**
- **do not build a new thermal simulator from scratch**
- **validate the thermal premise first**
- **only then escalate into TACE-specific method engineering**
