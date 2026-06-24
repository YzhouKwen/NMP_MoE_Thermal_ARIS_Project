# CLAUDE.md

## Project Overview

This project uses ARIS in single-project mode to explore publishable research ideas around thermal problems caused by irregular MoE routing in 3D-stacked NMP architectures.

The intended outcome is not a generic MoE systems survey. The intended outcome is a focused architecture idea with a defensible bottleneck, a credible experimental path, and a clear thermal evaluation story.

## Research Scope

The current active scope includes:

1. irregular MoE routing and expert skew under large-model inference
2. spatial and temporal activity imbalance across 3D-stacked NMP tiers, banks, and compute islands
3. thermal hotspot formation and propagation in stacked memory-centric systems
4. thermal-aware data placement, tensor placement, and expert placement
5. thermal-aware scheduling, throttling, remapping, or routing regularization
6. architecture and runtime co-design using HotSpot-compatible thermal traces

The agent should treat these as one connected problem family: routing skew creates non-uniform activity, non-uniform activity creates localized power density, and localized power density affects performance, reliability, or mapping decisions.

## Non-Goals

The agent should avoid drifting into:

- generic MoE algorithm improvements without architecture relevance
- generic thermal management surveys with no NMP or stacked-memory specificity
- pure circuit-level thermal modeling without a system-level mechanism
- ideas that require full-chip RTL or fabrication-only evidence
- vague "load balance better" proposals without a thermal mechanism or evaluation path

## Workflow Preference

For the current stage, prefer:

- idea discovery before heavy implementation
- architecture-reviewer critique over generic LLM novelty framing
- compact, high-signal candidates instead of broad brainstorming
- mechanisms that can be validated with trace-driven or model-driven experiments
- explicit planning for HotSpot integration, even if the first pass uses simplified power models

## Paper Library

Primary local paper directories for ARIS workflows:

- `papers/`
- `literature/`

## Evaluation Preference

When evaluating literature or ideas, prioritize:

- thermal realism in 3D-stacked systems
- routing skew sensitivity
- bank/tier-level activity observability
- performance-thermal tradeoff clarity
- mapping / scheduling controllability
- feasibility of building a HotSpot-based validation path
- publishability in architecture / systems venues

## Codebase Status

- This project is in early ARIS setup stage.
- `experiments/hotspot/` is a placeholder for future HotSpot inputs, not a validated simulator setup yet.
- Reuse external repos selectively, but keep this directory as the source of truth for this topic.

## Execution Environment

### Local Environment

- OS: Linux / WSL-compatible shell workflow
- Shell: bash
- Workspace root: `/home/liudy/workspace/dev/projects`
- Main project repo: `/home/liudy/workspace/dev/projects/NMP_MoE_Thermal_ARIS_Project`
- ARIS repo: `/home/liudy/workspace/dev/projects/Auto-claude-code-research-in-sleep`
- Suggested default environment: fill before workflow 1.5 execution

### Remote Environment

- SSH: `[FILL BEFORE REMOTE RUNS]`
- GPU / server: `[FILL BEFORE REMOTE RUNS]`
- Conda / venv: `[FILL BEFORE REMOTE RUNS]`
- Remote code dir: `[FILL BEFORE REMOTE RUNS]`

## Pipeline Status

- stage: workflow-1.5-complete (ready for /run-experiment)
- project_goal: identify a strong architecture-level research idea for thermal-aware MoE execution on 3D-stacked NMP systems
- active_idea: TACE — Thermal Anti-Clustering of Experts (anti-clustering QAP with direct max_t T(t) surrogate; TACG-port refutation centerpiece)
- current_focus: execute B0 (pre-flight inventory) → B1 (surrogate calibration) → B2 (Section 4 hook) to unlock M0–M2 gates
- active_tasks:
  - run B0: trace coverage matrix + CoMeT/Voxel smoke-test against published 3D thermal anchor + solver wall-clock at 16x4
  - run B1: Form A ↔ Form B correlation calibration (target ≥ 0.85, ridge-refit fallback)
  - run B2: token-balance ≠ thermal-balance proof (C1) on 4 task families
- completed:
  - ARIS project skeleton created
  - workflow 1 input brief drafted
  - workflow 1 phases 1–5.5 (research-lit → idea-creator → research-review)
  - workflow 1.5 research-refine-pipeline on 2026-06-24 (TACE locked; 12 mandatory changes covered)
- next:
  - /run-experiment starting at B0
- contract: docs/research_contract.md
- locked_inputs: Q5=max_t T(t); Q6=ILP cap 16x4 (Voxel cross-check 32x8); Q7=train-on-3/test-on-1 4-fold
- key_artifacts: refine-logs/FINAL_PROPOSAL.md, refine-logs/EXPERIMENT_PLAN.md, refine-logs/PIPELINE_SUMMARY.md

## Rules for This Project

1. Always read `RESEARCH_BRIEF.md` before running Workflow 1.
2. Treat `RESEARCH_BRIEF.md` as the primary task brief and this file as project-level policy.
3. During Workflow 1, behave like an architecture reviewer, not a generic LLM-paper reviewer.
4. Prefer ideas with a clear bridge from routing statistics to power density to thermal consequences.
5. If HotSpot assumptions are used, state them explicitly and separate estimated power traces from measured or simulator-derived traces.
6. Do not commit to a full implementation plan until the bottleneck and evaluation story are both sharp enough.
<!-- ARIS:BEGIN -->
## ARIS Skill Scope
ARIS skills installed in this project: 80 entries.
Manifest: `.aris/installed-skills.txt` (lists every skill ARIS installed and its upstream target).
For ARIS workflows, prefer the project-local skills under `.claude/skills/` over global skills.
Do not modify or delete files inside any skill that is a symlink (symlinks point into `/home/liudy/workspace/dev/projects/Auto-claude-code-research-in-sleep`).
Update with: `bash /home/liudy/workspace/dev/projects/Auto-claude-code-research-in-sleep/tools/install_aris.sh`  (re-runnable; reconciles new/removed skills).
<!-- ARIS:END -->
