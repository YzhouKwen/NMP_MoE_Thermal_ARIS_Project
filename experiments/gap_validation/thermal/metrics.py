"""HotSpot output parsers and thermal metrics."""
from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np


def parse_steady_file(path: str) -> Dict[str, float]:
    """Parse HotSpot .steady -> {block_name: temperature_K}."""
    out: Dict[str, float] = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                try:
                    out[parts[0]] = float(parts[1])
                except ValueError:
                    continue
    return out


def parse_ttrace(path: str) -> Tuple[List[str], np.ndarray]:
    """Parse a HotSpot transient .ttrace.

    Returns:
        names: list of block names in column order
        temps: ndarray shape (n_steps, n_blocks) in Kelvin
    """
    with open(path) as f:
        header = f.readline().strip().split()
        rows = []
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            try:
                rows.append([float(x) for x in parts])
            except ValueError:
                continue
    arr = np.asarray(rows, dtype=float) if rows else np.zeros((0, len(header)))
    return header, arr


def k_to_c(t_k: float) -> float:
    return t_k - 273.15


def peak_temperature_c(temps_k: Dict[str, float], silicon_only: bool = True) -> Tuple[float, str]:
    """Return (peak_temp_C, block_name).

    By default restrict to silicon compute blocks (named ``B_t...``); HotSpot
    .steady files also include package/heatsink/internal nodes which are not of
    interest for the gap-validation peak metric.
    """
    if not temps_k:
        return float("nan"), ""
    candidates = temps_k
    if silicon_only:
        candidates = {n: v for n, v in temps_k.items() if "B_t" in n}
        if not candidates:
            candidates = temps_k
    name = max(candidates, key=lambda n: candidates[n])
    return k_to_c(candidates[name]), name


def vertical_gradient_k(temps_k: Dict[str, float], name_prefix: str = "B_t") -> Dict[int, float]:
    """Mean temperature per silicon tier in K.

    HotSpot prefixes block names with `layer_<N>_` in the .steady output, so we
    accept both bare `B_t<tier>_b<idx>` and `layer_<N>_B_t<tier>_b<idx>`.
    """
    by_tier: Dict[int, List[float]] = {}
    for n, t in temps_k.items():
        # strip optional HotSpot "layer_<N>_" prefix
        bare = n.split("layer_", 1)[-1]
        # after layer_, format is "<N>_<original>" so we still need to advance
        if bare != n:  # had a layer_ prefix
            # skip "<N>_" portion
            if "_" in bare:
                bare = bare.split("_", 1)[1]
        if not bare.startswith(name_prefix):
            continue
        try:
            tier = int(bare.split("_")[1][1:])
        except (IndexError, ValueError):
            continue
        by_tier.setdefault(tier, []).append(t)
    return {t: float(np.mean(v)) for t, v in by_tier.items()}


def gini(values: np.ndarray) -> float:
    """Gini coefficient on a non-negative vector."""
    v = np.asarray(values, dtype=float).flatten()
    if v.size == 0:
        return 0.0
    if np.any(v < 0):
        v = v - v.min()
    s = v.sum()
    if s == 0:
        return 0.0
    v = np.sort(v)
    n = v.size
    cum = np.cumsum(v)
    return float((n + 1 - 2 * np.sum(cum) / s) / n)


def time_above_threshold(ttrace_K: np.ndarray, threshold_K: float, dt_s: float) -> float:
    """Total seconds during which any block exceeded threshold."""
    if ttrace_K.size == 0:
        return 0.0
    any_over = (ttrace_K > threshold_K).any(axis=1)
    return float(any_over.sum() * dt_s)
