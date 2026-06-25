"""Thin subprocess wrapper around the HotSpot binary.

We call HotSpot in two modes used by G0:
  - steady_state: solve to thermal equilibrium under a single-step ptrace,
    write the per-block .steady file
  - transient: solve transient over a multi-step ptrace, write the per-block
    .ttrace file

Both modes use the 3D grid model with `-detailed_3D on`.
"""
from __future__ import annotations

import os
import subprocess
import time
from dataclasses import dataclass
from typing import Optional

from utils.config import HOTSPOT_BIN, HOTSPOT_DIR


@dataclass
class HotspotResult:
    returncode: int
    wallclock_s: float
    stdout: str
    stderr: str
    steady_file: Optional[str] = None
    transient_file: Optional[str] = None


def _config_path() -> str:
    """Use the example4 config (3D-stack-tested) as our default thermal config."""
    return os.path.join(HOTSPOT_DIR, "examples", "example4", "example.config")


def run_steady_state(
    lcf_path: str,
    ptrace_path: str,
    out_dir: str,
    config_path: Optional[str] = None,
    extra_args: Optional[list] = None,
) -> HotspotResult:
    """Run HotSpot in steady-state grid mode."""
    os.makedirs(out_dir, exist_ok=True)
    steady_file = os.path.join(out_dir, "steady.out")
    grid_steady_file = os.path.join(out_dir, "steady.grid.out")

    cfg = config_path or _config_path()
    cmd = [
        HOTSPOT_BIN,
        "-c", cfg,
        "-p", ptrace_path,
        "-grid_layer_file", lcf_path,
        "-model_type", "grid",
        "-grid_rows", "16",
        "-grid_cols", "16",
        "-steady_file", steady_file,
        "-grid_steady_file", grid_steady_file,
    ]
    if extra_args:
        cmd.extend(extra_args)

    t0 = time.time()
    proc = subprocess.run(cmd, cwd=os.path.dirname(lcf_path), capture_output=True, text=True)
    return HotspotResult(
        returncode=proc.returncode,
        wallclock_s=time.time() - t0,
        stdout=proc.stdout,
        stderr=proc.stderr,
        steady_file=steady_file if proc.returncode == 0 else None,
    )


def run_transient(
    lcf_path: str,
    ptrace_path: str,
    out_dir: str,
    init_file: Optional[str] = None,
    config_path: Optional[str] = None,
    extra_args: Optional[list] = None,
) -> HotspotResult:
    """Run HotSpot in transient grid mode (writes per-block .ttrace)."""
    os.makedirs(out_dir, exist_ok=True)
    ttrace_file = os.path.join(out_dir, "transient.ttrace")
    grid_ttrace = os.path.join(out_dir, "transient.grid.ttrace")

    cfg = config_path or _config_path()
    cmd = [
        HOTSPOT_BIN,
        "-c", cfg,
        "-p", ptrace_path,
        "-grid_layer_file", lcf_path,
        "-model_type", "grid",
        "-grid_rows", "16",
        "-grid_cols", "16",
        "-o", ttrace_file,
        "-grid_transient_file", grid_ttrace,
    ]
    if init_file:
        cmd.extend(["-init_file", init_file])
    if extra_args:
        cmd.extend(extra_args)

    t0 = time.time()
    proc = subprocess.run(cmd, cwd=os.path.dirname(lcf_path), capture_output=True, text=True)
    return HotspotResult(
        returncode=proc.returncode,
        wallclock_s=time.time() - t0,
        stdout=proc.stdout,
        stderr=proc.stderr,
        transient_file=ttrace_file if proc.returncode == 0 else None,
    )
