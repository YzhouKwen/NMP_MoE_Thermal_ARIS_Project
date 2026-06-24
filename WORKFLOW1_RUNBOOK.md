# Workflow 1 Runbook

## Goal

Run ARIS Workflow 1 in single-project mode to identify and rank research ideas for thermal-aware MoE execution in 3D-stacked NMP architectures.

## Before Running

Make sure the following are ready:

- the ARIS repo is available locally
- your coding agent can read this project directory
- `RESEARCH_BRIEF.md` exists in the project root
- `CLAUDE.md` exists in the project root
- local paper directories `papers/` and `literature/` are ready to receive PDFs and notes

## Recommended First Command

```text
/idea-discovery "thermal-aware MoE execution in 3D-stacked NMP architectures" — AUTO_PROCEED: false, compact: true
```

## Recommended Priming Prompt

```text
Please first read RESEARCH_BRIEF.md and CLAUDE.md in the current project.
Use RESEARCH_BRIEF.md as the primary task context and CLAUDE.md as the project policy file.
The objective is to identify the strongest publishable architecture idea linking irregular MoE routing to thermal hotspots in 3D-stacked NMP systems.
Prioritize mechanism-level ideas with a credible validation path that can eventually incorporate HotSpot.
Explicitly compare candidates across placement, scheduling, remapping, thermal control, and architecture co-design.
```

## Expected Outputs

After a successful Workflow 1 run, expect:

- `IDEA_REPORT.md`
- `IDEA_CANDIDATES.md`
- `refine-logs/FINAL_PROPOSAL.md`
- `refine-logs/EXPERIMENT_PLAN.md`
- `refine-logs/EXPERIMENT_TRACKER.md`

## What To Do After Workflow 1

1. read `IDEA_CANDIDATES.md`
2. select one active idea
3. update `docs/research_contract.md`
4. refine `refine-logs/EXPERIMENT_PLAN.md`
5. only then decide whether to implement HotSpot integration, power modeling, or scheduling code
