"""G0 entrypoint - Pre-flight inventory and simulator anchor.

Runs four checks per refine-logs/GAP_VALIDATION_PLAN.md G0:
  G0.a  Trace coverage matrix  (Patterns Behind Chaos / HF listing)
  G0.b  Substrate plumbing      (.flp + .lcf + ptrace round-trip)
  G0.c  HotSpot smoke-test      (uniform power steady-state, sanity check)
  G0.d  Solver wall-clock       (1-s transient on the locked substrate)

Each check writes a JSON artifact under results/g0/ and a row into the verdict
summary at the end. Exit code is 0 iff all four pass.
"""
from __future__ import annotations

import json
import os
import sys
import time
import traceback
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

import numpy as np

# Allow running from anywhere
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from thermal.floorplan_gen import emit_layer_config, stack_summary
from thermal.hotspot_runner import run_steady_state, run_transient
from thermal.metrics import (
    k_to_c,
    parse_steady_file,
    parse_ttrace,
    peak_temperature_c,
    vertical_gradient_k,
)
from thermal.power_map_gen import write_synthetic_burst_ptrace, write_uniform_ptrace
from thermal.substrate import build_substrate, die_size_m, stack_height_m
from utils.config import (
    G0_WALLCLOCK_TARGET_S,
    HOTSPOT_BIN,
    N_BANKS_PER_TIER,
    N_TIERS,
    RESULTS_ROOT,
    T_AMBIENT_K,
)


# ---- G0.a -----------------------------------------------------------------

TASK_FAMILY_MAP = {
    "chat": ["hellaswag"],
    "code": ["livecodebench"],
    "math": ["HuggingFaceH4"],            # HF MATH-500 prefix
    "multilingual": ["mmlu_ZH_CN", "Chinese-SimpleQA"],
}


def g0a_trace_coverage(out_dir: str, min_requests: int = 500) -> dict:
    """Compute (model x task_family) request count matrix from HF listing."""
    try:
        from huggingface_hub import HfApi
    except Exception as e:
        return {"ok": False, "error": f"huggingface_hub import: {e}"}

    api = HfApi()
    info = api.dataset_info("core12345/MoE_expert_selection_trace")
    counts: Dict[Tuple[str, str], int] = defaultdict(int)
    bench_seen: Counter = Counter()
    for s in (info.siblings or []):
        parts = s.rfilename.split("/")
        if len(parts) < 4:
            continue
        model = parts[0] + "/" + parts[1]
        bench = parts[2]
        if s.rfilename.endswith(".json"):
            counts[(model, bench)] += 1
            bench_seen[bench] += 1

    models = sorted({m for (m, _) in counts.keys()})
    families = list(TASK_FAMILY_MAP.keys())
    matrix: Dict[str, Dict[str, int]] = {m: {fam: 0 for fam in families} for m in models}
    for (m, bench), n in counts.items():
        for fam, prefixes in TASK_FAMILY_MAP.items():
            if any(bench == p or bench.startswith(p) for p in prefixes):
                matrix[m][fam] += n

    # G0 pass: >=3/4 task families have >=min_requests for >=1 model
    family_pass = {
        fam: any(matrix[m][fam] >= min_requests for m in models) for fam in families
    }
    n_pass = sum(1 for ok in family_pass.values() if ok)
    artifact = {
        "ok": True,
        "passed": n_pass >= 3,
        "min_requests_per_family": min_requests,
        "n_families_passing": n_pass,
        "family_pass": family_pass,
        "matrix": matrix,
        "bench_totals": dict(bench_seen.most_common(20)),
        "models": models,
        "families": families,
        "note": (
            "File listing is public; file contents are gated and require "
            "huggingface-cli login + dataset access acceptance for G1."
        ),
    }
    with open(os.path.join(out_dir, "g0a_trace_coverage.json"), "w") as f:
        json.dump(artifact, f, indent=2)
    return artifact


# ---- G0.b -----------------------------------------------------------------

def g0b_substrate_plumbing(out_dir: str) -> dict:
    """Emit floorplan + layer-config + uniform single-step ptrace.

    Validation = files parse and HotSpot accepts them in a tiny steady-state run.
    """
    stack_dir = os.path.join(out_dir, "stack")
    os.makedirs(stack_dir, exist_ok=True)
    lcf = emit_layer_config(stack_dir)
    ptrace = os.path.join(stack_dir, "uniform.ptrace")
    names = write_uniform_ptrace(ptrace, watts_per_bank=0.1, n_steps=1)

    n_silicon_blocks = N_TIERS * N_BANKS_PER_TIER
    artifact = {
        "lcf": lcf,
        "ptrace": ptrace,
        "n_blocks_in_ptrace": len(names),
        "expected_silicon_blocks": n_silicon_blocks,
        "stack": stack_summary(),
        "die_size_m": list(die_size_m()),
        "stack_height_m": stack_height_m(),
        "first_blocks": names[:8],
    }

    ok = len(names) == n_silicon_blocks and os.path.exists(lcf)
    artifact["passed"] = bool(ok)
    if not ok:
        artifact["error"] = "block count mismatch or .lcf missing"

    with open(os.path.join(out_dir, "g0b_substrate.json"), "w") as f:
        json.dump(artifact, f, indent=2)
    return artifact


# ---- G0.c -----------------------------------------------------------------

def g0c_smoke_test(out_dir: str, plumbing: dict) -> dict:
    """Steady-state on uniform power. Sanity-check vertical gradient + peak T."""
    if not plumbing.get("passed"):
        return {"passed": False, "error": "g0b plumbing did not pass"}

    smoke_dir = os.path.join(out_dir, "smoke")
    os.makedirs(smoke_dir, exist_ok=True)
    # 0.1 W/bank * 64 banks = 6.4 W chip total (modest)
    res = run_steady_state(plumbing["lcf"], plumbing["ptrace"], smoke_dir)
    artifact = {
        "wallclock_s": res.wallclock_s,
        "returncode": res.returncode,
        "stderr_tail": res.stderr[-500:] if res.stderr else "",
        "stdout_tail": res.stdout[-500:] if res.stdout else "",
    }
    if res.returncode != 0 or not res.steady_file:
        artifact["passed"] = False
        artifact["error"] = f"hotspot failed rc={res.returncode}"
        with open(os.path.join(out_dir, "g0c_smoke.json"), "w") as f:
            json.dump(artifact, f, indent=2)
        return artifact

    temps_k = parse_steady_file(res.steady_file)
    peak_c, peak_block = peak_temperature_c(temps_k)
    tier_means = vertical_gradient_k(temps_k)
    tier_means_c = {t: k_to_c(v) for t, v in tier_means.items()}

    # Sanity checks:
    # (1) all silicon blocks above ambient (steady_state >= T_amb)
    above_amb = all(v >= T_AMBIENT_K - 0.1 for v in temps_k.values())
    # (2) top tier hotter than bottom tier under uniform power (heat sink at top
    #     in HotSpot's 3D default -> bottom is hottest; we just require a
    #     monotonic gradient existence, not its direction here)
    sorted_tiers = sorted(tier_means_c.items())
    tier_vals = [v for _, v in sorted_tiers]
    monotone = (
        all(a <= b + 1e-6 for a, b in zip(tier_vals, tier_vals[1:]))
        or all(a >= b - 1e-6 for a, b in zip(tier_vals, tier_vals[1:]))
    )
    # (3) peak < melt temp 200 C, > ambient
    peak_sane = 45.0 < peak_c < 200.0

    passed = bool(above_amb and monotone and peak_sane)
    artifact.update(
        {
            "peak_c": peak_c,
            "peak_block": peak_block,
            "tier_means_c": tier_means_c,
            "checks": {
                "all_above_ambient": above_amb,
                "monotone_vertical_gradient": monotone,
                "peak_in_sane_range_45_200_C": peak_sane,
            },
            "passed": passed,
        }
    )
    with open(os.path.join(out_dir, "g0c_smoke.json"), "w") as f:
        json.dump(artifact, f, indent=2)
    return artifact


# ---- G0.d -----------------------------------------------------------------

def g0d_wallclock(out_dir: str, plumbing: dict, smoke: dict) -> dict:
    """1-second-equivalent transient on the locked substrate to anchor solver wall-clock."""
    if not plumbing.get("passed") or not smoke.get("passed"):
        return {"passed": False, "error": "prereq g0b/g0c did not pass"}

    wall_dir = os.path.join(out_dir, "wallclock")
    os.makedirs(wall_dir, exist_ok=True)

    # 1-second worth of samples at HotSpot's default sampling interval.
    # default = 3.333e-6 s per row -> 300k rows for 1 s. That is heavy; for
    # the wall-clock anchor we use a coarser 1 ms sampling (1000 rows = 1 s).
    n_steps = 1000
    coarse_intvl = 1.0e-3  # seconds per step

    # Burst on tier-0 corner banks (worst-case hotspot proxy).
    banks = build_substrate()
    burst_indices = [i for i, b in enumerate(banks) if b.tier == 0 and (b.gx, b.gy) in {(0, 0), (1, 0), (0, 1), (1, 1)}]
    ptrace = os.path.join(wall_dir, "burst.ptrace")
    write_synthetic_burst_ptrace(
        ptrace,
        n_steps=n_steps,
        base_watts=0.1,
        burst_watts=0.6,
        burst_block_indices=burst_indices,
        burst_duty=0.3,
        seed=1,
    )

    res = run_transient(
        plumbing["lcf"],
        ptrace,
        wall_dir,
        extra_args=["-sampling_intvl", f"{coarse_intvl}"],
    )

    artifact = {
        "n_steps": n_steps,
        "sampling_intvl_s": coarse_intvl,
        "wallclock_s": res.wallclock_s,
        "wallclock_target_s": G0_WALLCLOCK_TARGET_S,
        "returncode": res.returncode,
        "stderr_tail": res.stderr[-500:] if res.stderr else "",
    }
    if res.returncode != 0 or not res.transient_file:
        artifact["passed"] = False
        artifact["error"] = f"hotspot failed rc={res.returncode}"
        with open(os.path.join(out_dir, "g0d_wallclock.json"), "w") as f:
            json.dump(artifact, f, indent=2)
        return artifact

    header, temps = parse_ttrace(res.transient_file)
    if temps.size:
        peak_k_per_step = temps.max(axis=1)
        artifact["peak_c_final"] = float(peak_k_per_step[-1] - 273.15)
        artifact["peak_c_max_over_run"] = float(peak_k_per_step.max() - 273.15)
        artifact["n_columns_in_ttrace"] = temps.shape[1]
    artifact["passed"] = bool(res.wallclock_s <= G0_WALLCLOCK_TARGET_S)
    with open(os.path.join(out_dir, "g0d_wallclock.json"), "w") as f:
        json.dump(artifact, f, indent=2)
    return artifact


# ---- driver ---------------------------------------------------------------

def main() -> int:
    os.makedirs(RESULTS_ROOT, exist_ok=True)
    out_dir = os.path.join(RESULTS_ROOT, "g0")
    os.makedirs(out_dir, exist_ok=True)
    timeline = {"started_at": datetime.utcnow().isoformat() + "Z"}

    print(f"[G0] HotSpot bin: {HOTSPOT_BIN}")
    print(f"[G0] Output dir : {out_dir}")
    print(f"[G0] Substrate  : {N_TIERS} tiers x {N_BANKS_PER_TIER} banks = {N_TIERS*N_BANKS_PER_TIER} sites")

    results: Dict[str, dict] = {}
    try:
        print("\n[G0.a] Trace coverage matrix...")
        results["g0a"] = g0a_trace_coverage(out_dir)
        print(f"        passed={results['g0a'].get('passed')}  families_ok={results['g0a'].get('n_families_passing')}/4")

        print("\n[G0.b] Substrate plumbing...")
        results["g0b"] = g0b_substrate_plumbing(out_dir)
        print(f"        passed={results['g0b'].get('passed')}  blocks={results['g0b'].get('n_blocks_in_ptrace')}")

        print("\n[G0.c] HotSpot smoke-test (uniform power steady-state)...")
        results["g0c"] = g0c_smoke_test(out_dir, results["g0b"])
        print(
            f"        passed={results['g0c'].get('passed')}  "
            f"peak={results['g0c'].get('peak_c'):.2f} C  "
            f"wallclock={results['g0c'].get('wallclock_s', 0):.2f} s"
            if results["g0c"].get("passed")
            else f"        passed={results['g0c'].get('passed')}  error={results['g0c'].get('error')}"
        )

        print("\n[G0.d] Solver wall-clock anchor (1-s transient)...")
        results["g0d"] = g0d_wallclock(out_dir, results["g0b"], results["g0c"])
        print(
            f"        passed={results['g0d'].get('passed')}  "
            f"wallclock={results['g0d'].get('wallclock_s', 0):.2f} s  "
            f"(target <= {G0_WALLCLOCK_TARGET_S} s)"
        )

    except Exception:
        traceback.print_exc()
        results["fatal"] = traceback.format_exc()

    timeline["finished_at"] = datetime.utcnow().isoformat() + "Z"
    verdict = {
        "g0a_passed": bool(results.get("g0a", {}).get("passed")),
        "g0b_passed": bool(results.get("g0b", {}).get("passed")),
        "g0c_passed": bool(results.get("g0c", {}).get("passed")),
        "g0d_passed": bool(results.get("g0d", {}).get("passed")),
    }
    verdict["all_passed"] = all(verdict.values())
    summary = {"timeline": timeline, "verdict": verdict, "results": results}
    with open(os.path.join(out_dir, "g0_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\n[G0] Verdict: {verdict}")
    return 0 if verdict["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
