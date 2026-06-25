# Gap Validation — Implementation Subtree

This subtree implements the pre-method gap-validation experiments described in
`refine-logs/GAP_VALIDATION_PLAN.md` and constrained by
`refine-logs/GAP_VALIDATION_IMPLEMENTATION_NOTE.md`.

## Layout

```
gap_validation/
  external/HotSpot/        # vendored upstream HotSpot 6.0 (do not modify)
  thermal/                 # project-owned thermal wrappers
    substrate.py             3D-NMP geometry (4 tiers x 16 banks)
    floorplan_gen.py         emit HotSpot .flp + .lcf
    power_map_gen.py         emit HotSpot .ptrace
    hotspot_runner.py        subprocess wrapper around the hotspot binary
    metrics.py               peak T, vertical gradient, time-above-threshold, Gini
  baselines/               # placement baselines (filled in G1)
  utils/config.py          # locked substrate constants and paths
  results/g0/              # G0 artifacts (JSON + HotSpot output files)
  run_g0.py                # G0 entrypoint
  .venv/                   # project-local venv (numpy / scipy / pandas / matplotlib / huggingface_hub)
```

## Substrate (locked at G0)

- 4 silicon compute tiers, 16 banks per tier (4x4 grid), 2 mm bank pitch
- 8 mm x 8 mm die, alternating Silicon (150 um) + TIM (20 um) layers
- Materials and ambient (45 C) per HotSpot 3D example defaults

## Running G0

```
.venv/bin/python run_g0.py
```

Artifacts: `results/g0/{g0a_trace_coverage,g0b_substrate,g0c_smoke,g0d_wallclock,g0_summary}.json`
plus HotSpot output files under `results/g0/{stack,smoke,wallclock}/`.
