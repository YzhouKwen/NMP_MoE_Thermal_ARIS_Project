# Research Brief

## Problem Statement

I want to use ARIS Workflow 1 to identify strong, publishable research ideas around thermal problems caused by irregular MoE routing in 3D-stacked NMP architectures.

The core issue is that MoE expert routing is often highly non-uniform across tokens and time. In a 3D-stacked NMP system, that irregularity may create spatially concentrated activity across particular banks, tiers, or near-memory compute regions. This can generate hotspots, aggravate thermal coupling across stacked layers, and potentially change the real optimal mapping or scheduling policy compared with a thermally oblivious design.

I do not want a generic "thermal-aware system" topic. I want the workflow to help identify the sharpest architecture problem inside this space: what exact routing-induced thermal bottleneck matters most, what mechanism is novel, and what experiment path can credibly validate it, potentially with HotSpot.

## Background

- **Field**: computer architecture / accelerator systems / large model inference
- **Sub-area**: 3D-stacked NMP architectures for MoE inference
- **Architecture family of interest**:
  - 3D-stacked NMP / PIM systems
  - bank-distributed memory-centric accelerators
  - hybrid NPU-NMP or NPU-PIM systems when relevant
- **Current research family**:
  - MoE routing skew and expert imbalance
  - expert placement / tensor placement / data placement
  - activity-aware scheduling and remapping
  - thermal hotspot formation in stacked memory systems
  - thermal-aware architecture/runtime co-design
- **Key terminology**:
  - irregular routing
  - expert skew
  - hotspot
  - thermal coupling
  - 3D stack
  - near-memory processing
  - processing-in-memory
  - MoE inference
  - expert placement
  - thermal-aware scheduling
  - HotSpot
- **What I already know**:
  - the broad direction is memory-centric accelerator architecture
  - I want to focus on thermal behavior driven by irregular MoE routing
  - HotSpot may be part of the validation flow
- **What I do not want**:
  - pure algorithm-level MoE routing methods with no architecture contribution
  - vague thermal balancing ideas without a concrete bottleneck
  - evaluation stories that require unrealistic infrastructure from the first iteration

## Constraints

- **Compute**: currently not fixed; prefer ideas that admit a model-driven, trace-driven, or simulator-assisted first validation pass
- **Timeline**: current stage is problem sharpening and idea selection, not full implementation
- **Target venue style**: architecture / systems style
- **Current goal**: identify one active, defensible idea that can later move into workflow 1.5

## What I'm Looking For

- [x] A ranked set of candidate ideas inside the routing-thermal problem family
- [x] A focused top proposal with a mechanism-level contribution
- [x] A credible experiment roadmap that can eventually include HotSpot
- [x] Clarity on the primary control lever:
  - thermal-aware expert placement
  - thermal-aware routing regularization
  - thermal-aware scheduling / throttling
  - thermal-aware remapping / migration
  - thermal-aware architecture co-design
- [ ] A generic survey only
- [ ] Immediate large-scale implementation
- [ ] Pure model-quality optimization

## Domain Knowledge

- Irregular MoE routing can create bursty and localized expert activation.
- In 3D-stacked NMP systems, localized activation may map to concentrated bank/tier power density rather than smooth average utilization.
- Thermal hotspots may feed back into performance, throttling, reliability margin, or mapping feasibility.
- A strong idea should answer:
  - what exact routing-induced thermal bottleneck is attacked
  - why 3D-stacked NMP makes this bottleneck especially important
  - what mechanism is new relative to performance-only balancing
  - how a reviewer can be convinced empirically
- A strong first evaluation path may use:
  - routing trace statistics
  - activity-to-power proxy models
  - HotSpot-compatible power traces
  - comparative thermal metrics such as peak temperature, spatial gradient, sustained hotspot duration, and thermal-performance tradeoff

## Non-Goals

- broad thermal surveys without prioritization
- generic NoC / datacenter thermal work that is not specific to NMP or stacked-memory MoE inference
- compiler-only or serving-only work with no architecture bottleneck
- full physical accuracy claims without enough modeling support

## Existing Results (if any)

- No committed active idea yet in this project directory
- This setup is intended to start a fresh ARIS workflow for the MoE-routing thermal problem family

## Expected Output from Workflow 1

I want Workflow 1 to produce:

1. a ranked idea report across the most relevant routing-thermal ideas
2. a compact candidate summary for later switching
3. one refined top proposal
4. one experiment roadmap with a minimum viable HotSpot-compatible path
5. clarity on whether the best problem is primarily:
   - placement
   - scheduling
   - remapping
   - thermal control
   - architecture co-design

## Preferred Search and Review Behavior

- Prioritize papers that connect MoE execution behavior, PIM/NMP architecture, and thermal or power density implications.
- When direct papers are sparse, allow bridging from adjacent literature:
  - MoE systems
  - 3D-stacked thermal modeling
  - PIM/NMP mapping and scheduling
  - thermal-aware accelerator scheduling
- Explicitly reject ideas that are too broad, too obvious, experimentally weak, or merely "do load balancing plus HotSpot."
