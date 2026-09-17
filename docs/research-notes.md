# Research Log — 2026-09-17

## Review Scope

The first update added **36 papers / 37 rows** (VBVR appears as both a resource and benchmark), retaining English tables and date order. Coverage is selective; experiments were not reproduced.

Discovery used the arXiv Atom API (`https://export.arxiv.org/api/query`) on 2026-09-17: `video reasoning`; January–June and January–April 2026; streaming/online/proactive video titles; world-model/video-generation/visual-reasoning titles. Queries returned 30–45 results each. January–April used relevance order; the rest used submission date. Selection favored distinct mechanisms and evaluation contributions, not a quality ranking.

All **177 existing arXiv IDs** were resolved. The 36 additions received title/date/abstract review, producing an initial **213-record** [bibliography](bibliography.json). This did not include full-paper review, code execution, independent venue confirmation, or comprehensive revalidation of historical links and non-arXiv sources.

Mechanism summaries paraphrase abstracts. Unverified venues remain `arXiv`; the taxonomy and equations are survey synthesis. Scores from different protocols are not ranked together.

## Literature Additions

| Primary paper | First public | Placement | Contribution / scope decision |
| :--- | :--- | :--- | :--- |
| [SVMemAgent: A Streaming Video Memory Agent for Query-Agnostic Online Frame Selection](https://arxiv.org/abs/2609.18540) | 2026-09-16 | Streaming | SVMemAgent: query-agnostic frame replacement/discard policy under a streaming memory budget. |
| [Long-to-Short Video Evidence Reasoning for Grounded Question Answering](https://arxiv.org/abs/2609.15224) | 2026-09-14 | CoT | LOVER: long-to-short evidence curriculum, evidence rewards, and timestamp rendering for grounded QA. |
| [Online Video Agent Harness for Long Video Understanding](https://arxiv.org/abs/2609.12818) | 2026-09-11 | Interleaved / tools | VideoXAgent: query-conditioned expert tools over an available video file; “online” in its title does not imply causal streaming observations. |
| [ProactiveBench: Can Streaming Video Models Really Interact Like Humans?](https://arxiv.org/abs/2609.12658) | 2026-09-11 | Benchmark | ProactiveBench: evaluates whether and when to respond, including silence, premature responses, and duplicate counting. |
| [From Evaluation to Enhancement: Benchmarking and Improving Think-with-Video Reasoning for Video Generative Models](https://arxiv.org/abs/2609.11242) | 2026-09-10 | Benchmark | VWG-Bench: separates rendering fluency, rule adherence, and goal realization; also introduces the Vid-PRE prompt enhancer. |
| [VLX-VR: An Agentic-Aware Video Reasoning Model](https://arxiv.org/abs/2609.09985) | 2026-09-09 | Interleaved / tools | VLX-VR: Think–Memory–Observation loop; adaptive evidence acquisition and memory use. |
| [Video-MOPD: Multi-Teacher On-Policy Distillation for Video Understanding](https://arxiv.org/abs/2609.09300) | 2026-09-08 | CoT | Video-MOPD: distills complementary video experts using routed teacher feedback; distinguishes post-training from a reasoning representation. |
| [Beyond Retrieval: Progressive Latent Memory Evolution for Streaming Video Understanding](https://arxiv.org/abs/2609.04131) | 2026-09-03 | Streaming | LatentStream: hierarchical retrieval internalized into fixed-length latent working memory. |
| [Do Video Generators Track the World Across Segments? A Benchmark and Method for World-State Reasoning in Video Continuation](https://arxiv.org/abs/2609.03673) | 2026-09-03 | CoF / generative | Stateagent/Statebench: explicit entity-state updates for video continuation; retained under generation with structured-state overlap. |
| [Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models](https://arxiv.org/abs/2608.27065) | 2026-08-27 | CoT | Video-OPSD: evidence-focused privileged self-teacher; teacher-only evidence must be disclosed in comparisons. |
| [VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning](https://arxiv.org/abs/2608.26105) | 2026-08-26 | Benchmark | VBVR-Pro: procedural task scaling and deterministic verifiable scorers across visual generation substrates. |
| [OVIBench: Benchmarking Online Video Question Answering under Interruption](https://arxiv.org/abs/2608.22279) | 2026-08-23 | Benchmark | OVIBench: cancellation, false triggers, and correction during answer generation; the proposed protocol uses offline interruption simulation. |
| [StreamArena: Toward Continuous, Interactive, and Long-Horizon Agentic Streaming Video Understanding](https://arxiv.org/abs/2608.05703) | 2026-08-06 | Benchmark | StreamArena: hour-scale interactive open-ended evaluation and tool use. Its StreamMind system is distinct from the 2025 paper with the same name. |
| [GROVE: Growing and Reasoning over Temporally Stratified Memory from Streaming Video Experience](https://arxiv.org/abs/2608.02392) | 2026-08-03 | Streaming | GROVE: causally accumulated moments, episodes, and cross-day patterns; reactive recall and proactive assistance share memory. |
| [OmniReasoner: Thinking with Long Audio-Video via Native Tool Use](https://arxiv.org/abs/2607.19339) | 2026-07-21 | Interleaved / tools | OmniReasoner: temporal zoom-in on both audio and video; timestamp alignment across sampling granularities. |
| [Hierarchical Denoising For Multi-Step Visual Reasoning](https://arxiv.org/abs/2607.15278) | 2026-07-16 | CoF / generative | Hierarchical denoising: coarse-to-fine latent planning for generated visual solutions; streaming generation is distinct from online video QA. |
| [Graph it first! Enabling Reasoning on Long-form Egocentric Videos through Scene Graphs](https://arxiv.org/abs/2606.25842) | 2026-06-24 | Structured / latent | EgoSG: symbolic scene graphs preserve temporal relations in long egocentric videos; graph observations can still contain perception errors. |
| [SER: Learning to Ground Video Reasoning with Semantic Evidence Rewards](https://arxiv.org/abs/2606.24726) | 2026-06-23 | CoT | SER: semantic relevance/localization rewards supplement purely geometric evidence supervision. |
| [EgoSAT: A Comprehensive Benchmark of Egocentric Streaming Interaction Understanding](https://arxiv.org/abs/2606.24422) | 2026-06-23 | Benchmark | EgoSAT: retrospective, current, and prospective egocentric questions under observed-prefix constraints; includes answerability/calibration analysis. |
| [VideoLatent: Video-Language Learning via Latent Self-Forcing](https://arxiv.org/abs/2606.22870) | 2026-06-22 | Structured / latent | VideoLatent: latent injection and self-forcing from video QA triplets; continuous reasoning without explicit text CoT supervision. |
| [Temporal Backtracking Search for Test-time Generative Video Reasoning](https://arxiv.org/abs/2606.13861) | 2026-06-11 | CoF / generative | Temporal Backtracking Search: verify and restart from valid temporal prefixes rather than resampling entire trajectories. |
| [Imagine Before You Predict: Interleaved Latent Visual Reasoning for Video Event Prediction](https://arxiv.org/abs/2606.05769) | 2026-06-04 | Structured / latent | Future-L1: interleaves language and future-oriented visual latents; predicted states must not be treated as observations. |
| [SagaQA: A Multi-hop Reasoning Benchmark for Long-form Narrative Understanding in TV Series](https://arxiv.org/abs/2606.03301) | 2026-06-02 | Benchmark | SagaQA: evidence chains across episodes of long-form narratives rather than only nearby clips. |
| [CaST-Bench: Benchmarking Causal Chain-Grounded Spatio-Temporal Reasoning for Video Question Answering](https://arxiv.org/abs/2605.23216) | 2026-05-22 | Benchmark | CaST-Bench: causal-chain questions with temporal segments and box tracks; evaluates answers and grounded evidence. |
| [Video Models Can Reason with Verifiable Rewards](https://arxiv.org/abs/2605.15458) | 2026-05-14 | CoF / generative | VideoRLVR: rule-based rewards for generated trajectories; separates visual quality from solution validity. |
| [CollabVR: Collaborative Video Reasoning with Vision-Language and Video Generation Models](https://arxiv.org/abs/2605.08735) | 2026-05-09 | Interleaved / tools | CollabVR: separate VLM and video generator cooperate in a plan–generate–verify loop; interleaving does not require one unified model. |
| [OASIS: On-Demand Hierarchical Event Memory for Streaming Video Reasoning](https://arxiv.org/abs/2604.17052) | 2026-04-18 | Streaming | OASIS: demand-driven hierarchical event retrieval; bounded request context is not necessarily bounded total stored history. |
| [MME-CoF-Pro: Evaluating Reasoning Coherence in Video Generative Models with Text and Visual Hints](https://arxiv.org/abs/2603.20194) | 2026-03-20 | Benchmark | MME-CoF-Pro: process-level reasoning coherence with no-hint, text-hint, and visual-hint conditions. |
| [Thinking in Streaming Video](https://arxiv.org/abs/2603.12938) | 2026-03-13 | Streaming | ThinkStream: Watch–Think–Speak updates, reasoning-compressed memory, and response-timing training. |
| [Thinking with Spatial Code for Physical-World Video Reasoning](https://arxiv.org/abs/2603.05591) | 2026-03-05 | Structured / latent | Spatial code: explicit 3D object variables and temporal tracking for physical-world video QA. |
| [A Very Big Video Reasoning Suite](https://arxiv.org/abs/2602.20159) | 2026-02-23 | CoF / generative; Benchmark | VBVR: scalable procedural tasks and rule-based scoring; listed as both a generative training resource and benchmark. |
| [GraphThinker: Reinforcing Temporally Grounded Video Reasoning with Event Graph Thinking](https://arxiv.org/abs/2602.17555) | 2026-02-19 | Structured / latent | GraphThinker: event graphs plus visual-attention rewards for temporally grounded reasoning. |
| [Weaver: End-to-End Agentic System Training for Video Interleaved Reasoning](https://arxiv.org/abs/2602.05829) | 2026-02-05 | Interleaved / tools | Weaver: end-to-end training of dynamic video tool use and interleaved evidence trajectories. |
| [Triage: Hierarchical Visual Budgeting for Efficient Video Reasoning in Vision-Language Models](https://arxiv.org/abs/2601.22959) | 2026-01-30 | CoT | Triage: frame- and token-level budgeting; efficiency support rather than evidence of a new reasoning substrate. |
| [MINERVA-Cultural: A Benchmark for Cultural and Multilingual Long Video Reasoning](https://arxiv.org/abs/2601.10649) | 2026-01-15 | Benchmark | MINERVA-Cultural: culturally situated, native-language long-video reasoning beyond English-centric evaluation. |
| [Watching, Reasoning, and Searching: A Video Deep Research Benchmark on Open Web for Agentic Video Reasoning](https://arxiv.org/abs/2601.06943) | 2026-01-11 | Benchmark | VideoDR: joint video and open-web evidence; retrieval tools and search state are part of the evaluation setting. |

## Corrections

Dates below use primary `published` metadata, which can differ from the arXiv identifier month.

| Primary source | Previous month | Corrected month |
| :--- | :--- | :--- |
| [2512.00805](https://arxiv.org/abs/2512.00805) | 2025-12 | 2025-11 |
| [2506.00318](https://arxiv.org/abs/2506.00318) | 2025-06 | 2025-05 |
| [2501.03230](https://arxiv.org/abs/2501.03230) | 2025-01 | 2024-05 |
| [2412.00161](https://arxiv.org/abs/2412.00161) | 2024-12 | 2024-11 |
| [2512.05969](https://arxiv.org/abs/2512.05969) | 2025-12 | 2025-11 |
| [2508.01875](https://arxiv.org/abs/2508.01875) | 2025-10 | 2025-08 |
| [2501.00584](https://arxiv.org/abs/2501.00584) | 2025-01 | 2024-12 |
| [2412.08646](https://arxiv.org/abs/2412.08646) | 2024-11 | 2024-12 |
| [2512.14691](https://arxiv.org/abs/2512.14691) | 2015-12 | 2025-12 |
| [2512.08228](https://arxiv.org/abs/2512.08228) | 2015-12 | 2025-12 |
| [ViTCoT](https://arxiv.org/abs/2507.09876) | 2025-10 in the interleaved table | 2025-07; matches the original preprint and CoT entry |

[TOMATO's official proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/16ba99f25a235f1100a4014d71d34ad8-Abstract-Conference.html) confirm **ICLR 2025**, correcting CVPR. `Findinds` and `Spotlighht` typos were fixed. Other venue updates use explicit author comments/journal references, not independent proceedings verification.

| Paper | Previous venue | Updated venue | Evidence |
| :--- | :--- | :--- | :--- |
| [2512.03043](https://arxiv.org/abs/2512.03043) | `Arxiv` | `CVPR 2026` | CVPR 2026, Project page: https://github.com/tulerfeng/OneThinker |
| [2512.02425](https://arxiv.org/abs/2512.02425) | `Arxiv` | `CVPR 2026` | CVPR 2026. Project page : https://worldmm.github.io |
| [2512.00805](https://arxiv.org/abs/2512.00805) | `Arxiv` | `CVPR 2026` | Accepted by CVPR 26 |
| [2508.20478](https://arxiv.org/abs/2508.20478) | `Arxiv` | `ICML 2026` | Accepted by ICML 2026. Camera-ready version |
| [2508.11538](https://arxiv.org/abs/2508.11538) | `Arxiv` | `CVPR 2026` | 12 pages CVPR 2026 |
| [2508.07683](https://arxiv.org/abs/2508.07683) | `Arxiv` | `ECCV 2026` | Accepted by ECCV2026 |
| [2508.03100](https://arxiv.org/abs/2508.03100) | `Arxiv` | `CVPR 2026` | CVPR 2026 |
| [2506.00318](https://arxiv.org/abs/2506.00318) | `Arxiv` | `CVPR 2026` | Accepted to the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) 2026 |
| [2505.24869](https://arxiv.org/abs/2505.24869) | `Arxiv` | `TMLR 2026` | Accepted by TMLR (01/2026) |
| [2503.13444](https://arxiv.org/abs/2503.13444) | `Arxiv` | `ICLR 2026` | ICLR 2026 Camera Ready |
| [2512.07469](https://arxiv.org/abs/2512.07469) | `Arxiv` | `CVPR 2026` | Accepted by CVPR 2026, Project Page: https://videocof.github.io/ |
| [2510.05094](https://arxiv.org/abs/2510.05094) | `Arxiv` | `ACL 2026 (Findings)` | ACL 2026 (Findings Paper), ICCV 2025 Workshop Outstanding Paper Award, Project page: https://eyeline-labs.github.io/VChain |
| [2511.20785](https://arxiv.org/abs/2511.20785) | `Arxiv` | `CVPR 2026` | CVPR 2026 |
| [2603.12262](https://arxiv.org/abs/2603.12262) | `Arxiv` | `ECCV 2026` | Accepted by ECCV 2026, project page https://1ranguan.github.io/VST/ |
| [2510.09608](https://arxiv.org/abs/2510.09608) | `Arxiv` | `ICLR 2026` | Published as a conference paper at ICLR 2026. The first two authors contributed equally to this work |
| [2507.05240](https://arxiv.org/abs/2507.05240) | `Arxiv` | `ICRA 2026` | Accepted to ICRA 2026 |
| [2505.15269](https://arxiv.org/abs/2505.15269) | `Arxiv` | `DAC 2026` | Accepted by DAC'26 63rd ACM/IEEE Design Automation Conference (DAC '26), July 2026 |
| [2504.16030](https://arxiv.org/abs/2504.16030) | `Arxiv` | `CVPR 2025` | CVPR 2025. If any references are missing, please contact joyachen@u.nus.edu |
| [2506.21742](https://arxiv.org/abs/2506.21742) | `Arxiv` | `CVPR 2026` | Accepted at CVPR 2026 |
| [2505.24867](https://arxiv.org/abs/2505.24867) | `Arxiv` | `CVPR 2026` | Accepted at IEEE/CVF Conference on Computer Vision and Pattern Recognition 2026 Project page at https://timeblindness.github.io |

Unresolved venue claims remain unchanged: “ICCV format” is not acceptance; AV-SpeakerBench's “Findings of CVPR” is ambiguous; StreamGaze reports acceptance followed by desk rejection. Announced venues do not establish published proceedings.

Title updates: **TimeZero → Time-R1**, **CoT-Vid → VISTA**, **TAR-TVG → TAR**, **MECD → MECD+** for the 2025 follow-up, **ImplicitQA → VRR-QA**, and revised VideoMind, MMGR, COVER, and VideoCoF titles. MECD's 2024 paper remains separate. ImplicitQA's dataset label is retained; a paper rename does not establish a dataset rename.

Catalog repairs:

- [Chain-of-Frames](https://arxiv.org/abs/2506.00318) produces text traces referring to observed frames. Its duplicate in the generated-trajectory CoF table was removed, while its CoT entry and weight link were retained.
- Unified VILA-U and JavisGPT architectures now have an explicitly labeled foundations subsection inside Interleaved; unified understanding/generation alone is not evidence of iterative reasoning.
- [From 128K to 4M](https://arxiv.org/abs/2504.06214) was moved to adjacent foundations because it extends a text LLM's context, not native video support. [3DSRBench](https://arxiv.org/abs/2412.07825) was moved there because its benchmark uses images. Both sources and resource links are retained.
- RVTBench, VCRBench, and SEED-Bench-R1 remain in the benchmark catalog; duplicate benchmark-oriented rows were removed from the CoT methods table. VCRBench and VCR-Bench are distinct papers and are explicitly disambiguated in the selection guide.
- Dataset/project links were moved out of Checkpoint cells into the neighboring resources cells, preserving the links. Long-RL's actual [LongVILA-R1-7B weights](https://huggingface.co/Efficient-Large-Model/LongVILA-R1-7B) replace a training-dataset link, following the paper's author comment. The Eagle collection in the R1-Zero-VSI row was removed from Checkpoint because this review did not verify that association; no nonexistence claim is made.
- HAVEN's JSON file is now labeled Data rather than Hugging Face. StreamingCoT's copied `#minerva` fragment, the wrong Star History destination, malformed contributor URL, orphan `</h2>`, broken TOC anchors, and literal backticked HTML breaks were repaired. Stable explicit anchors now support the expanded contents.

## Resource Checks

Unauthenticated HTTPS checks resolved **16 of 17** selected author resources. ThinkStream redirects to `CASIA-IVA-Lab/ThinkStream`, now used in the catalog. Reachability does not establish release completeness or reproducibility.

Video-MOPD's advertised `https://huggingface.co/LandH/Video-MOPD-8B` returned **HTTP 401**. Its checkpoint is recorded as `N/A`; the response does not identify whether the resource is private, restricted, or removed. Revisit availability in later updates.

The validator checks local structure and metadata, not live links or scientific accuracy. Keep catalog entries and bibliography snapshots consistent.


## World-Model Extension — 2026-09-17

The extension added **six papers**, bringing the bibliography to **219 records**. The catalog separates reasoning engines from interaction loops and labels direct video systems, visual bridges, and planning foundations. WorldCoder-Bench remains a separate bridge evaluation. Existing references and anchors were preserved.

| Primary source | Placement | Evidence reviewed |
| :--- | :--- | :--- |
| [Code World Model: Coding Agent as World Brain](https://arxiv.org/abs/2608.25927) | Executable/hybrid; direct video-world system | v1 full-text Sections 2.3, 3–5, primary metadata, project page, and author repository README |
| [Recursive Code World Models](https://arxiv.org/abs/2609.11499) | Executable/hybrid; single-image reconstruction bridge | Primary metadata and abstract; no inference of demonstrated video dynamics |
| [VisualPatchWorld](https://arxiv.org/abs/2607.25236) | Executable/hybrid; visual-state/planning bridge | Primary metadata and abstract; code link from the abstract |
| [GIF-MCTS](https://arxiv.org/abs/2405.15383) | Executable/hybrid; program-based planning foundation | Primary metadata and abstract; also discussed in Code World Model Section 2.3 |
| [WorldCoder](https://arxiv.org/abs/2402.12275) | Executable/hybrid; program-based planning foundation | Primary metadata and abstract; also discussed in Code World Model Section 2.3 |
| [WorldCoder-Bench](https://arxiv.org/abs/2606.01869) | Related executable-world evaluation; not video QA | Primary metadata and abstract; runtime behavior as an evaluation bridge |

Discovery query: `ti:"worldcoder" OR ti:"code world model" OR ti:"world models in code" OR ti:"world models with code" OR ti:"world models as programs"`, relevance order, 25 results. Supporting abstract pages were also read. Inclusion follows the state/dynamics/perception/rendering connections in [Worlds as Programs](world-models.md), not name matching.

The [perspective](../README.md#world-model-perspective) and agenda are survey synthesis. Code World Model demonstrates qualitative proxy-following using recorded sequences and engine templates, with latency excluded from comparisons. Complete autonomous world construction and autoregressive real-time generation remain undemonstrated. Proposed experiments are labeled accordingly.

CWM's repository, LoRA adapter, inference-example dataset, and VisualPatchWorld's repository returned **HTTP 200**. The adapter is not a standalone base model; inference examples are not the complete training set. No model was run. New venues remain `arXiv` unless separately verified.

The validator scans all survey Markdown for known GitHub-blocked macros, including `\operatorname`. Formulas use fenced `math` and supported `\mathrm` labels; rendering still requires separate verification.