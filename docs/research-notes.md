# Research update — 2026-09-17

## Scope and evidence

This update retains the repository's English tables and reverse chronological ordering, adds 36 distinct papers (37 new catalog rows because VBVR contributes a method/resource and a benchmark), and completes the task, modeling, and evaluation narrative. It is a selective literature update, not an exhaustive or systematic review, and does not reproduce experimental results.

Discovery used the arXiv Atom API (`https://export.arxiv.org/api/query`) on 2026-09-17. Queries covered the exact phrase `video reasoning`, January–June 2026, January–April 2026, streaming/online/proactive video titles, and world-model/video-generation/visual-reasoning titles. Retrieval was capped at 30–45 results per query; the January–April query used relevance ordering, while the others used submission-date ordering. This balances recent discoveries with earlier 2026 work but can miss relevant papers and terminology. Candidate selection favored distinct modeling or evaluation contributions and direct video relevance; inclusion is not a quality ranking.

All 177 distinct arXiv IDs already linked in the original README were resolved through the primary API. The 36 new papers were checked against their primary titles, first-public dates, and abstracts. [bibliography.json](bibliography.json) records 213 checked primary records, including version URLs and author comments when fetched for existing entries. This is metadata and abstract-level verification, not a claim of full-paper review, code execution, dataset inspection, or independent venue confirmation. Existing non-arXiv citations and every historical resource link were not comprehensively revalidated.

New claims about mechanisms below are paraphrases of the authors' abstracts. No author-reported leaderboard result is promoted to a cross-paper ranking. New papers remain labeled `arXiv` where venue acceptance was not separately checked. The README's modeling equations and cross-axis taxonomy are editorial synthesis, not a formulation attributed to all cited papers.

## New literature and placement

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

## Corrections and retained scope

The following first-public months were corrected from primary `published` metadata, not inferred from arXiv identifier prefixes. A paper's identifier month can differ from its first public date.

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

[TOMATO's official ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/16ba99f25a235f1100a4014d71d34ad8-Abstract-Conference.html) identify **ICLR 2025**, correcting the original CVPR label. `Findinds` and `Spotlighht` spelling errors were fixed. Other venue changes below use explicit author comments/journal references from the primary metadata snapshot; acceptance announcements are distinguished from independent proceedings verification.

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

Ambiguous statements were not promoted: “ICCV format” is not acceptance; the AV-SpeakerBench “Findings of CVPR” wording needs clarification; StreamGaze's author comment describes acceptance followed by desk rejection, so it remains `arXiv`. A later venue name alone is not treated as evidence that proceedings have already appeared.

Significant title changes were reconciled with the current primary records: **TimeZero → Time-R1**, **CoT-Vid → VISTA**, **VideoMind**'s temporal-grounded title, **TAR-TVG → TAR**, **MECD → MECD+** for the 2025 follow-up, **ImplicitQA → VRR-QA**, and the expanded **MMGR**, **COVER**, and **VideoCoF** titles. Older aliases remain here for searchability; MECD's separate 2024 paper remains a separate entry. ImplicitQA's historical benchmark label is retained alongside its updated paper title rather than asserting that a dataset was renamed.

Classification/resource repairs:

- [Chain-of-Frames](https://arxiv.org/abs/2506.00318) produces text traces referring to observed frames. Its duplicate in the generated-trajectory CoF table was removed, while its CoT entry and weight link were retained.
- Unified VILA-U and JavisGPT architectures now have an explicitly labeled foundations subsection inside Interleaved; unified understanding/generation alone is not evidence of iterative reasoning.
- [From 128K to 4M](https://arxiv.org/abs/2504.06214) was moved to adjacent foundations because it extends a text LLM's context, not native video support. [3DSRBench](https://arxiv.org/abs/2412.07825) was moved there because its benchmark uses images. Both sources and resource links are retained.
- RVTBench, VCRBench, and SEED-Bench-R1 remain in the benchmark catalog; duplicate benchmark-oriented rows were removed from the CoT methods table. VCRBench and VCR-Bench are distinct papers and are explicitly disambiguated in the selection guide.
- Dataset/project links were moved out of Checkpoint cells into the neighboring resources cells, preserving the links. Long-RL's actual [LongVILA-R1-7B weights](https://huggingface.co/Efficient-Large-Model/LongVILA-R1-7B) replace a training-dataset link, following the paper's author comment. The Eagle collection in the R1-Zero-VSI row was removed from Checkpoint because this review did not verify that association; no nonexistence claim is made.
- HAVEN's JSON file is now labeled Data rather than Hugging Face. StreamingCoT's copied `#minerva` fragment, the wrong Star History destination, malformed contributor URL, orphan `</h2>`, broken TOC anchors, and literal backticked HTML breaks were repaired. Stable explicit anchors now support the expanded contents.

## Resource verification and limitations

Author-linked resources were checked with unauthenticated HTTPS GET requests. Sixteen of 17 checked resources resolved successfully, including official project pages, GitHub repositories, VWG-Bench data, and LongVILA-R1 weights. This is a reachability check, not proof that code, data, and checkpoints are complete or runnable. The ThinkStream repository redirects from `johncaged/ThinkStream` to `CASIA-IVA-Lab/ThinkStream`; the catalog uses the resolved destination.

The Video-MOPD abstract advertises `https://huggingface.co/LandH/Video-MOPD-8B`, but the endpoint returned **HTTP 401** during this review. The catalog therefore records `N/A` for its checkpoint rather than presenting an accessible verified release. HTTP 401 cannot distinguish private, restricted, removed, or otherwise inaccessible resources. Other new rows without author-linked verified resources also use `N/A`; availability should be revisited in later updates.

The static validator checks all catalog tables, local references, ordering, first-public dates, and repeated-paper metadata. It does not check network availability or scientific correctness. Bibliographic snapshots are checked evidence from this update, not an automatically maintained database. Future changes should update both the visible catalog and relevant snapshot records.
