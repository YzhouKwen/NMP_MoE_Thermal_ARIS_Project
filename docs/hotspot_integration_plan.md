# HotSpot Integration Plan

## Purpose

This document records the intended role of HotSpot in the project so ARIS outputs stay aligned with a realistic validation path.

## Minimum Viable Thermal Pipeline

1. derive routing/activity traces from MoE execution scenarios
2. map trace activity to bank/tier/expert-region power estimates
3. export time-windowed power maps into `experiments/hotspot/power_maps/`
4. prepare floorplan and thermal config inputs in `experiments/hotspot/floorplan/` and `experiments/hotspot/configs/`
5. run HotSpot or a HotSpot-compatible flow
6. report peak temperature, spatial variance, hotspot persistence, and performance-thermal tradeoff

## Modeling Boundaries

- Early-stage runs may use relative or normalized power estimates.
- Any claim about absolute temperature must clearly state calibration assumptions.
- Thermal comparison can still be useful even before full silicon-accurate calibration.

## Target Outputs

- hotspot-ready power trace format
- floorplan assumptions for 3D-stacked NMP tiers
- comparison table for baseline vs thermal-aware strategy
