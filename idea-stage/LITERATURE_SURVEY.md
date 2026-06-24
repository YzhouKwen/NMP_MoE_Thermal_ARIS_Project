# Literature Survey — Thermal-Aware MoE on 3D-Stacked NMP

**Date**: 2026-06-23
**Direction**: irregular MoE routing → spatial/temporal activity imbalance → bank/tier-level power density → hotspot formation in 3D-stacked NMP, with control via placement, scheduling, remapping, throttling, or co-design.
**Sources searched**: arXiv (10 query clusters) + WebSearch venue pass + partial Semantic Scholar (rate-limited). No Zotero/Obsidian MCP; local `papers/` and `literature/` are empty placeholders.

## Landscape Table

| # | Paper | arXiv | Date | Theme | Relevance |
|---|-------|-------|------|-------|-----------|
| 1 | **Sieve: Dynamic Expert-Aware PIM Acceleration for Evolving MoE** | 2605.11277 | 2026-05 | HBM-PIM MoE scheduler (Ramulator 2.0). Bimodal expert distribution → arithmetic-intensity disparity. Splits expert exec between GPU and PIM. | **Closest direct competitor.** Thermal-blind. Establishes bimodal-skew framing. |
| 2 | **HD-MoE: Hybrid & Dynamic Parallelism for MoE on 3D NMP** | 2509.09420 | 2025-09 | 3D NMP accelerator; offline auto hybrid TP/EP mapping + online dynamic schedule. 1.1–1.8× speedup. | **Closest 3D-NMP MoE work.** Thermal-blind. Treats placement+schedule as comm/util problem only. |
| 3 | **TokenStack: Heterogeneous HBM-PIM for LLM** | 2605.05639 | 2026-05 | HBM-PIM runtime for KV-cache attention. | Adjacent: PIM LLM architecture, not MoE-specific. |
| 4 | **Sangam: Chiplet DRAM-PIM with CXL for LLM** | 2511.12286 | 2025-11 | Chiplet PIM, KV-cache focus. | Adjacent PIM-LLM substrate. |
| 5 | **P3-LLM: NPU-PIM Hybrid for Edge LLM** | 2511.06838 | 2025-11 | NPU+PIM hybrid, edge inference. | Hybrid NMP-NPU pattern relevant to placement co-design. |
| 6 | **LP-Spec: LPDDR-PIM Speculative LLM** | 2508.07227 | 2025-08 | Architecture-dataflow co-opt on LPDDR-PIM. | Mobile PIM; orthogonal but useful prior art for PIM dataflow. |
| 7 | **Sparse Attention Remapping on PIM** | 2505.05772 | 2025-05 | Clustering-based remap for PIM attention decoding. | Method template for runtime remapping logic. |
| 8 | **MFIT: Multi-Fidelity Thermal Model for 2.5D/3D Chiplets** | 2410.09188 | 2024-10 | Days→seconds thermal solver, 16×3 3D chiplet validation. | **Key validation tool candidate** for HotSpot-grade evaluation. |
| 9 | **NN Surrogate for HBM Junction Temperature & Hotspot Position** | 2503.04049 | 2025-03 | ML surrogate predicting HBM hotspot under varying thermal conditions. | Fast inner-loop thermal estimator for online schedulers. |
| 10 | **On the Thermal Vulnerability of 3D-Stacked HBM** | 2509.00633 | 2025-08 | Shows bank-level vertical+lateral thermal coupling is exploitable for performance-degradation attacks. | **Strong physical motivation:** confirms bank-granular thermal coupling is real and observable. |
| 11 | **CoMeT: Integrated Interval Thermal Toolchain 2D/2.5D/3D Processor-Memory** | 2109.12405 | 2021-09 | HotSpot-compatible integrated thermal pipeline. | **HotSpot validation path** — cleanest reusable infrastructure. |
| 12 | **MORE-Stress: TSV Thermal Stress for 2.5D/3D ICs** | 2411.12690 | 2024-11 | TSV thermo-mechanical stress solver. | Reliability angle; orthogonal but supports thermal-stress claim. |
| 13 | **ExpertFlow: Predictive Expert Caching + Token Scheduling** | 2410.17954 | 2024-10 | GPU-only; routing-path prediction + token grouping. | Prior art for predictive routing models the scheduler can reuse. |
| 14 | **HOBBIT: Mixed-Precision Expert Offloading** | 2411.01433 | 2024-11 | Precision-level expert offloading. | Orthogonal lever (precision ≠ thermal), but shows expert-level heterogeneity is acceptable. |
| 15 | **DALI: Workload-Aware MoE Offloading on PCs** | 2602.03495 | 2026-02 | Local-PC CPU-GPU offload. | Adjacent serving system. |
| 16 | **Fine-Grained Expert Offloading for MoE Serving** | 2502.05370 | 2025-02 | Latency-memory trade. | Serving systems baseline. |
| 17 | **OD-MoE: On-Demand Expert Loading (cacheless)** | 2512.03927 | 2025-12 | Edge-distributed MoE serving. | Distributed serving baseline. |
| 18 | **Latent Prototype Routing (LPR)** | 2506.21328 | 2025-06 | Algorithmic near-perfect load balance (Gini 0.70→0.035). | **Important: shows algorithmic balancing exists** — any architecture idea must distinguish *physical* (thermal) balance vs *count* balance. |
| 19 | **Task-Conditioned Routing Signatures** | 2603.11114 | 2026-03 | Routing structure persists by task; predictable. | Justifies offline placement + online correction. |
| 20 | **Not All Experts Are Equal (Pruning/Skipping)** | 2402.14800 | 2024-02 | Hot vs cold experts. | Foundational evidence for persistent skew. |
| 21 | **Tasa: Thermal-aware 3D-Stacked Architecture for LLM Inference** | 2508.07252 | 2025-08 | Heterogeneous 3D stack: high-perf core for compute-heavy ops + high-eff core for attention; cross-stack thermal balancing; bandwidth-sharing scheduler. 5.55–9.37 °C peak-T reduction, 2.85× over GPU. | **Single most direct thermal competitor.** Dense-LLM only; routing skew and per-expert mapping are absent. |
| 22 | **ViBE: Co-Optimizing Workload Skew & Hardware Variability for MoE Serving** | 2606.00735 | 2026-06 | Variability-Informed Binning of Experts: hot experts → faster GPUs based on per-GPU perf model + activation profiling. | Closest *expert-placement-vs-skew* work; but thermal is *outside-stack* (rack stragglers), not bank/tier coupling. |
| 23 | **Context-Aware MoE on CXL-Enabled GPU-NDP** | 2512.04476 | 2025-12 | Prefill-stage activation stats guide decoding-stage expert placement; hot experts pinned in HBM, cold to CXL-NDP; mixed-precision per expert. 8.7× decoding throughput. | Strong placement prior art on NDP; thermal-blind. |
| 24 | **Voxel: 3D-Stacked AI Chip Simulation Framework** | 2604.26821 | 2026 | Compiler-aware end-to-end simulator for 3D-stacked AI chips; tile-to-core, tensor-to-bank mapping, NoC, energy/thermal constraints; validated on real silicon. | **Strongest infrastructure asset** for routing→bank-mapping→thermal evaluation. |
| 25 | **NeuroTAP: Thermal & Memory-Access-Pattern-Aware Data Mapping on 3D DRAM (TACO 2024)** | — (DOI 10.1145/3677178) | 2024 | Thermal-aware data mapping on 3D DRAM for DNN performance. | **Closest prior art on the data-mapping-vs-thermal axis** for DNNs; explicitly not MoE-aware. |
| 26 | **3D Heterogeneous Integration MoE Accelerator** | 2507.19142 | 2025-07 | Hardware-resource-aware fusion scheduler + even-odd expert mapping for HBM access reduction. | MoE+3D HBM but performance-only; thermal absent. |
| 27 | **Area-Efficient In-Memory Computing for MoE** | 2602.10254 | 2026-02 | IMC for MoE via multiplexing & caching. | IMC variant; orthogonal substrate option. |
| 28 | **Latency-Optimized Expert Placement for Distributed Edge MoE** | 2508.12851 | 2025-08 | Activation-aware expert placement w/ runtime migration across edge servers. | Useful migration cost model; rack-scale not bank-scale. |
| 29 | **DSE for Distributed 3D-Stacked AI Accelerators** | 2604.04750 | 2026 | DSE framework with thermal model + DVFS for distributed 3D AI accelerators. | Tooling; can support our DSE phase. |
| 30 | **Rethinking Compute Substrates for 3D-Stacked Near-Memory LLM Decoding** | 2604.04253 | 2026 | NMP compute substrates for memory-bound LLM decoding. | Substrate-level priors. |

## Theme Clusters

1. **MoE-on-PIM/NMP architecture (#1, #2, #5, #23, #26, #27)** — actively published 2025–2026; all optimize for throughput, comm, or utilization; thermal is absent.
2. **PIM-LLM substrate (non-MoE) (#3, #4, #6, #7, #30)** — KV-cache or attention focus; provides building blocks but not the MoE thermal story.
3. **3D-stacked thermal modeling/tools (#8, #9, #11, #12, #29)** — mature; usable as evaluation backbone.
4. **3D-stacked thermal-aware design for LLM/DNN (#21, #25)** — *active competitor cluster*. Tasa addresses thermal+LLM but not MoE; NeuroTAP addresses thermal data-mapping for DNN but not MoE.
5. **3D thermal physics & vulnerability (#10)** — independent evidence of bank-level vertical+lateral coupling.
6. **MoE serving / placement on conventional HW (#13–17, #22, #28)** — confirms expert skew; rack/server-level placement, not bank/tier.
7. **Algorithmic routing balance (#18, #19, #20)** — must be the algorithmic baseline against which any *thermal-physical* lever is differentiated.
8. **3D-stacked AI simulation infrastructure (#24)** — Voxel is a candidate evaluation backbone alongside CoMeT/MFIT/HotSpot.

## Recurring Patterns

- **Expert skew is real and bimodal**, persisting across MoE families (Mixtral, Qwen3-MoE, DeepSeek-V3, GPT-OSS, Llama-4). Confirmed independently by #1, #18, #20, #22.
- **Thermal-aware 3D-stacked LLM design exists but is dense-LLM-shaped (Tasa).** Tasa partitions by *operator type* (compute vs attention) and proves that bank/tier-level temperature in 3D stacks is the binding constraint. It does *not* model expert-level skew.
- **MoE-on-NMP work is thermal-blind (Sieve, HD-MoE, 2507.19142, 2512.04476).** All optimize utilization/communication.
- **Thermal-aware data mapping for 3D DRAM exists (NeuroTAP) but is DNN-generic, not MoE.** It is the closest prior art on the *placement-vs-thermal* axis and must be cited as the natural baseline.
- **3D-stack thermal coupling is bank-granular** (#10 is independent evidence; Tasa exploits it heterogeneously; Voxel models it).
- **Algorithmic load balance ≠ thermal balance.** LPR (#18) reaches near-uniform Gini but does not consider where experts sit physically.
- **HotSpot integration paths exist** via CoMeT (#11), MFIT (#8), Voxel (#24) — multiple credible backbones.

## Structural Gaps (sharpened after WebSearch venue pass)

| Gap | What's missing | Why it matters |
|-----|----------------|----------------|
| **G1. Routing-skew → bank/tier thermal coupling not characterized for MoE.** | No paper reports peak temperature, spatial gradient, or sustained hotspot duration as a function of MoE routing distribution on 3D-NMP. Tasa shows the constraint exists for dense LLMs; nobody has specialized this to expert-level skew. | Without this measurement, the thermal lever is not even quantified. This is a strong systems/measurement contribution by itself. |
| **G2. Thermal-aware *expert* placement on 3D-NMP is absent.** | Sieve/HD-MoE/2507.19142/2512.04476 place by compute/comm/HBM-access; ViBE places by *device-level* variability (rack stragglers); NeuroTAP places generic DNN tensors by thermal but is not expert-aware. | Vertical adjacency of two persistently hot experts is the most direct mechanism-level lever. The intersection (MoE × 3D thermal × bank-level placement) is empty. |
| **G3. Thermal-aware *online expert remapping* under temporal routing skew is unexplored.** | Sieve schedules expert *execution* between GPU and PIM but does not move experts; HD-MoE's online schedule is thermal-blind; edge-MoE migration (#28) is rack-scale. | Routing skew is also temporal; static placement under-performs when the hot expert set drifts across prompts/tasks. |
| **G4. No closed mechanism: routing → power density → temperature → policy feedback.** | Each component exists separately. No work has assembled the full loop with HotSpot-grade evaluation for MoE on 3D-NMP. | A unified framework is publishable infrastructure as well as a method. Voxel + MFIT/CoMeT could form the substrate. |
| **G5. Algorithmic balance vs physical balance distinction.** | LPR-style algorithmic balancing is being adopted, but its thermal effect on 3D NMP is unstudied. | Strong counter-result candidate: "uniform routing does not eliminate thermal hotspots when placement is fixed and bank-coupled." |
| **G6. Thermal-perf-energy Pareto for MoE-NMP unknown.** | No baseline that trades sustained T_peak against TPOT/throughput/energy for MoE on 3D-NMP. | Reviewer-grade evaluation requires this Pareto. |
| **G7. Thermal-induced positive-feedback amplification of skew is unmodeled.** | Throttling hot banks slows hot experts, which can shift token routing if dynamic, or extend latency if not — possibly aggravating skew or coupling layers. | A subtle, MoE-specific mechanism that thermally-blind dense-LLM thermal designs (Tasa) cannot capture. |

## Implications for Idea Generation

- **Strongest wedge**: pair the *physical-placement* control surface (which expert lives on which bank/tier) with the *temporal-routing* surface (which expert gets hot when), inside a closed routing→power→thermal→policy loop. Sieve, HD-MoE, Tasa, and NeuroTAP each leave one axis open.
- **Defensible bottleneck candidates**: (a) inter-tier vertical thermal coupling of co-placed hot experts; (b) bank-level transient hotspots from bursty routing; (c) thermal-induced throttling that *amplifies* MoE skew (positive feedback); (d) algorithmic-vs-physical balance gap.
- **HotSpot path**: CoMeT (#11) + MFIT (#8) + NN surrogate (#9) for inner loop; Voxel (#24) for full-stack 3D-NMP modeling.
- **Baselines to beat**: Tasa (thermal-aware dense LLM 3D), HD-MoE (3D-NMP MoE, thermal-blind), Sieve (HBM-PIM MoE, thermal-blind), NeuroTAP (thermal data mapping for DNN, MoE-blind), and an algorithmic-balance variant (LPR or load-balancing loss only, fixed placement).

## Notes on Search Coverage

- arXiv search was the primary source; semantic-scholar/deepxiv/exa not enabled (would catch IEEE/ACM venue-only papers like recent HPCA/MICRO submissions). Recommend running `— sources: web, semantic-scholar` if any candidate idea needs venue-paper confirmation in Phase 3.
- A handful of arXiv queries returned off-topic physics/accelerator hits; those were filtered out of the table.
