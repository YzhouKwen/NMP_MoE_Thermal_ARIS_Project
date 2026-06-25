"""3D-NMP substrate model for gap validation.

Layout (G0-locked):
- n_T = 4 silicon compute tiers (each with N_BANKS_PER_TIER banks on a GRID_X x GRID_Y grid)
- TIM layers between adjacent silicon tiers
- HBM-PIM-style: each (bank, tier) is one near-memory compute island

This module produces the geometric description (bank positions and sizes) that
the floorplan / power-map / metric modules consume. The thermal solver itself
lives in `external/HotSpot/`.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from utils.config import (
    BANK_SIZE_M,
    GRID_X,
    GRID_Y,
    N_BANKS_PER_TIER,
    N_TIERS,
    SILICON_THICKNESS_M,
    TIM_THICKNESS_M,
)


@dataclass(frozen=True)
class Bank:
    tier: int          # 0 = bottom silicon tier
    idx: int           # 0..N_BANKS_PER_TIER-1
    gx: int            # column 0..GRID_X-1
    gy: int            # row    0..GRID_Y-1
    x_m: float         # bottom-left corner, meters
    y_m: float
    w_m: float
    h_m: float

    @property
    def name(self) -> str:
        return f"B_t{self.tier}_b{self.idx:02d}"


def build_substrate(
    n_tiers: int = N_TIERS,
    n_banks_per_tier: int = N_BANKS_PER_TIER,
    grid_x: int = GRID_X,
    grid_y: int = GRID_Y,
    bank_size_m: float = BANK_SIZE_M,
) -> List[Bank]:
    """Return a list of Bank descriptors for the full 3D-NMP stack."""
    if grid_x * grid_y != n_banks_per_tier:
        raise ValueError(
            f"grid_x*grid_y ({grid_x*grid_y}) must equal n_banks_per_tier ({n_banks_per_tier})"
        )
    banks: List[Bank] = []
    for t in range(n_tiers):
        for idx in range(n_banks_per_tier):
            gx = idx % grid_x
            gy = idx // grid_x
            banks.append(
                Bank(
                    tier=t,
                    idx=idx,
                    gx=gx,
                    gy=gy,
                    x_m=gx * bank_size_m,
                    y_m=gy * bank_size_m,
                    w_m=bank_size_m,
                    h_m=bank_size_m,
                )
            )
    return banks


def die_size_m(grid_x: int = GRID_X, grid_y: int = GRID_Y, bank_size_m: float = BANK_SIZE_M) -> Tuple[float, float]:
    return (grid_x * bank_size_m, grid_y * bank_size_m)


def stack_height_m(n_tiers: int = N_TIERS) -> float:
    """Total stack height, including TIM between tiers."""
    return n_tiers * SILICON_THICKNESS_M + max(0, n_tiers - 1) * TIM_THICKNESS_M
