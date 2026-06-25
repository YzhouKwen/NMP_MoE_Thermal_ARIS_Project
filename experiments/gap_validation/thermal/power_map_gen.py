"""HotSpot power-trace (.ptrace) generators.

For G0, two trace generators are needed:
  - uniform: every silicon block has the same power (smoke-test against
    published 3D thermal anchor)
  - synthetic_burst: a 1-second wall-clock anchor for the wall-clock gate

Trace replay over real MoE traces happens in G1.
"""
from __future__ import annotations

from typing import Iterable, List, Sequence

import numpy as np

from thermal.substrate import build_substrate
from utils.config import N_TIERS


def _silicon_block_names() -> List[str]:
    """Block names in HotSpot ptrace order. TIM layers are non-power so omitted."""
    banks = build_substrate()
    return [b.name for b in banks]  # tier-major order, matching .lcf walk


def write_uniform_ptrace(path: str, watts_per_bank: float, n_steps: int = 1) -> List[str]:
    """Uniform power across all silicon blocks. Returns block-name header order."""
    names = _silicon_block_names()
    with open(path, "w") as f:
        f.write("\t".join(names) + "\n")
        row = "\t".join(f"{watts_per_bank:.6f}" for _ in names)
        for _ in range(n_steps):
            f.write(row + "\n")
    return names


def write_synthetic_burst_ptrace(
    path: str,
    n_steps: int,
    base_watts: float,
    burst_watts: float,
    burst_block_indices: Sequence[int],
    burst_duty: float = 0.2,
    seed: int = 0,
) -> List[str]:
    """Bursty power: chosen blocks alternate between base and burst power.

    Used only for wall-clock anchoring (G0.d). Not a calibrated workload.
    """
    rng = np.random.default_rng(seed)
    names = _silicon_block_names()
    n_blocks = len(names)
    burst_set = set(int(i) for i in burst_block_indices)
    with open(path, "w") as f:
        f.write("\t".join(names) + "\n")
        for _ in range(n_steps):
            row = []
            for i in range(n_blocks):
                if i in burst_set and rng.random() < burst_duty:
                    row.append(f"{burst_watts:.6f}")
                else:
                    row.append(f"{base_watts:.6f}")
            f.write("\t".join(row) + "\n")
    return names


def write_per_block_ptrace(path: str, watts_per_block: Iterable[float]) -> List[str]:
    """Single-step ptrace from a per-block power vector (used for steady-state)."""
    names = _silicon_block_names()
    vec = list(watts_per_block)
    if len(vec) != len(names):
        raise ValueError(f"len(watts_per_block)={len(vec)} != n_blocks={len(names)}")
    with open(path, "w") as f:
        f.write("\t".join(names) + "\n")
        f.write("\t".join(f"{w:.6f}" for w in vec) + "\n")
    return names


def per_tier_block_indices(n_tiers: int = N_TIERS) -> List[List[int]]:
    """Return [tier][bank-index-in-flat-order] for selecting per-tier subsets."""
    banks = build_substrate()
    out: List[List[int]] = [[] for _ in range(n_tiers)]
    for flat_i, b in enumerate(banks):
        out[b.tier].append(flat_i)
    return out
