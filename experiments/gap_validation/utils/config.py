"""Project-wide constants and paths for gap-validation experiments.

Substrate (locked at G0): n_T = 4 silicon compute tiers, n_B = 16 banks per tier
arranged as a 4x4 grid. Alternating Silicon + TIM stack per HotSpot 3D
example convention.
"""
from __future__ import annotations

import os

GAP_VAL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.dirname(GAP_VAL_ROOT))
HOTSPOT_DIR = os.path.join(GAP_VAL_ROOT, "external", "HotSpot")
HOTSPOT_BIN = os.path.join(HOTSPOT_DIR, "hotspot")
RESULTS_ROOT = os.path.join(GAP_VAL_ROOT, "results")

# Substrate locked at G0 (per user selection 2026-06-25)
N_TIERS = 4              # silicon compute tiers
N_BANKS_PER_TIER = 16    # 4 x 4 grid
GRID_X = 4
GRID_Y = 4
BANK_SIZE_M = 0.002      # 2 mm per bank side -> 8 mm x 8 mm die
SILICON_THICKNESS_M = 1.5e-4    # 150 um per silicon tier
TIM_THICKNESS_M = 2.0e-5        # 20 um TIM between tiers

# Materials (HotSpot 3D example defaults)
SILICON_CP = 1.75e6      # J/(m^3 K)
SILICON_R = 0.01         # (m K)/W = 100 W/(m K) conductivity
TIM_CP = 4.0e6
TIM_R = 0.25             # 4 W/(m K)

# Thermal envelope
T_AMBIENT_K = 318.15     # 45 C
T_CAP_C = 90.0           # default thermal cap for G3
SAMPLING_INTVL_S = 3.333e-6  # HotSpot default

# G0 wall-clock anchor target.
#
# G1 uses steady-state per placement (one HotSpot solve = ~1.1 s on this
# substrate). Even at 6 baselines x 4 families x 10 seeds the steady-state
# path comes in at <5 min total. The transient anchor here is a safety
# margin: we want one second of 1-ms-resolution transient to finish in under
# three minutes so that G3's thermal-cap closed loop is feasible. Earlier
# 60 s value was an arbitrary first cut.
G0_WALLCLOCK_TARGET_S = 180.0
