# Video Reasoning: The 2026 Research Map

**Window: 2025-12-18–2026-09-17 · snapshot: 2026-09-17.** This update adds **1,153 arXiv papers** to the existing **42** in-window references, plus **16 proceedings papers** with a separate date basis. [Main survey](../../README.md#paradigms) · [Machine-readable coverage](coverage.json).

The chapters are navigation facets, not ten mutually exclusive reasoning mechanisms. Each new paper has one primary home; the [Reasoning Stack](../../README.md#taxonomy-and-modeling) separates representations, learning, evidence, and interaction. Supporting perception methods, visual bridges, and planning foundations remain distinguishable from direct video reasoning.

## Explore the Landscape

| Chapter | Additions | Central question |
| :--- | ---: | :--- |
| [Grounded Reasoning](language.md) | 137 | Does the reasoning depend on the right visual evidence? |
| [Thinking in Visual Futures](visual.md) | 8 | When do generated frames become useful intermediate computation? |
| [Stateful Intelligence](structured.md) | 82 | What should persist as graphs, objects, geometry, or latent state? |
| [Executable Worlds](executable.md) | 28 | Can inferred rules be executed, checked, and revised? |
| [Active Video Agents](agents.md) | 111 | Which observation or tool call should come next? |
| [Always-On Intelligence](streaming.md) | 74 | What can be answered now, and when should the system speak? |
| [Evidence at Scale](perception.md) | 119 | How much evidence survives selection and compression? |
| [World Models for Action](worlds.md) | 214 | Do predicted futures improve decisions and control? |
| [Beyond Answer Accuracy](benchmarks.md) | 344 | What do benchmarks actually measure and control? |
| [Perspectives & Roadmaps](surveys.md) | 36 | Which concepts and open problems connect these directions? |

The [proceedings supplement](proceedings.md) adds 16 ACL papers across these topics. Its July dates identify proceedings publication, **not verified first-public dates**, so those papers are excluded from the monthly totals below.

<a id="research-shifts"></a>

## Research Shifts

These are survey interpretations of the cited work, not reproduced results or a consensus ranking.

| Shift | Evidence to read | Research priority |
| :--- | :--- | :--- |
| From longer traces to selective, grounded reasoning | [Video-FLAIR](https://arxiv.org/abs/2608.26495), [SER](https://arxiv.org/abs/2606.24726), [LOVER](https://arxiv.org/abs/2609.15224) | Test evidence dependence, process supervision, and stopping rules against direct-answer and shuffled-video controls. |
| From fixed frames to active evidence acquisition | [Weaver](https://arxiv.org/abs/2602.05829), [OmniReasoner](https://arxiv.org/abs/2607.19339), [VLX-VR](https://arxiv.org/abs/2609.09985) | Measure useful tool decisions, recovery from failed retrieval, and total encoder/search/generation cost. |
| From context windows to persistent state | [EgoSG](https://arxiv.org/abs/2606.25842), [VideoLatent](https://arxiv.org/abs/2606.22870), [GROVE](https://arxiv.org/abs/2608.02392) | Preserve identity and provenance; separate observations, inferred state, and imagined futures. |
| From offline answers to timely interaction | [ThinkStream](https://arxiv.org/abs/2603.12938), [OVIBench](https://arxiv.org/abs/2608.22279), [ProactiveBench](https://arxiv.org/abs/2609.12658) | Evaluate prefix-only access, readiness, silence, interruption, latency, and total retained memory. |
| From visual realism to executable mechanics | [SWoMo](https://arxiv.org/abs/2605.16530), [PhysMind](https://arxiv.org/abs/2608.04575), [Code World Model](https://arxiv.org/abs/2608.25927), [Programmable World Model](https://arxiv.org/abs/2609.10540) | Test rule validity, off-screen persistence, action sensitivity, and renderer compliance separately. |
| From one plausible future to calibrated alternatives | [CaliBench](https://arxiv.org/abs/2608.16829), [Twin Rollouts](https://arxiv.org/abs/2608.08982) | Separate scoreable outputs from calibrated distributions; control shared noise when comparing interventions. Twin Rollouts is a framework note with experiments forthcoming. |
| From oracle best-of-many to deployable selection | [Compute-Value Audit](https://arxiv.org/abs/2609.13257), [play-adequacy study](https://arxiv.org/abs/2607.14169) | Count verification costs and decision-critical errors; better sampled candidates need not improve the selected action. |
| From generic QA to diverse, auditable evaluation | [MINERVA-Cultural](https://arxiv.org/abs/2601.10649), [SagaQA](https://arxiv.org/abs/2606.03301), [INFACT](https://arxiv.org/abs/2603.11481), [LongInsightBench](https://aclanthology.org/2026.findings-acl.965/) | Cover languages, audio, cross-video evidence, specialized domains, temporal interventions, and shortcut controls. |

**A useful common protocol:** fix observation/action access, distinguish oracle annotations from pixels, separate held-out episodes and environments, report answer and evidence quality, then charge all preprocessing, memory, sampling, and verification costs. Public-set saturation is not held-out generalization; the [ARC-AGI-3 ablation](https://arxiv.org/abs/2607.15439) makes that limitation explicit.

## Coverage by First-Public Month

Counts are unique arXiv papers, not table rows or estimates of the field's total output. December starts on the 18th; September ends at the review snapshot.

| Month | Previously cataloged | Added | Total |
| :--- | ---: | ---: | ---: |
| 2025-12, from the 18th | 0 | 33 | 33 |
| 2026-01 | 4 | 85 | 89 |
| 2026-02 | 3 | 109 | 112 |
| 2026-03 | 5 | 155 | 160 |
| 2026-04 | 1 | 116 | 117 |
| 2026-05 | 3 | 177 | 180 |
| 2026-06 | 7 | 142 | 149 |
| 2026-07 | 3 | 136 | 139 |
| 2026-08 | 6 | 142 | 148 |
| 2026-09, through the 17th | 10 | 58 | 68 |
| **Total** | **42** | **1,153** | **1,195** |

<a id="review-method"></a>

## Sources, Screening & Limits

**Discovery.** Eight arXiv queries covered video reasoning, long/online video, world models, visual reasoning, benchmarks, related reasoning titles, and audio-visual systems. Every result page was retrieved: **2,476 unique query matches**. CVPR/ACL proceedings, five topic repositories, and targeted title/identity searches broadened discovery to **4,462 primary metadata records**, including out-of-window and unrelated candidates. Secondary lists were discovery aids; paper metadata and proceedings supplied citation evidence.

**Selection.** Broad title/scope triage was followed by targeted abstract excerpts for shortlisted papers and full abstracts for ambiguous mechanisms. This is a broad literature index, not a full-text systematic review. It includes relevant evidence interfaces, evaluations, and action-oriented world models; recognition-only, generic retrieval, and production-only systems were not automatically included. The earlier full-text Code World Model case study remains separately documented.

**Dates and identity.** arXiv `published` supplies first-public dates, even when it differs from the ID prefix. Revisions and conference acceptance do not create new papers. Official CVPR/ACL evidence supports **133 venue matches** across new and historical entries. An additional historical [Video-MMMU](https://arxiv.org/abs/2501.13826) reference was restored to the main benchmark table with its January 2025 date; it is outside the counts above. Unresolved venues remain `arXiv`; proceedings-only records retain their distinct date basis.

**Resources.** Author-linked GitHub, GitHub Pages, and Hugging Face URLs received **455 HTTP checks: 443 returned 200; 12 did not**. New index rows record only successful checks. The proceedings supplement has its own resource-check log. This pass did not systematically audit every historical resource or every project domain; availability does not establish release completeness or reproducibility. `N/A` means no checked link recorded.

**Limits.** Search vocabulary, indexing delay, renamed papers, and domain boundaries can still hide relevant work. ICML, ICLR, and ECCV proceedings and citation chains were not exhaustively screened. Non-English and non-arXiv work may be underrepresented. The logs make these gaps inspectable; the update does not claim provable zero omissions or reproduced experiments.

| Artifact | Contents |
| :--- | :--- |
| [searches.json](searches.json) | Exact queries, pagination counts, source URLs, and retrieval status |
| [screening.jsonl](screening.jsonl) | Candidate decisions, dates, discovery routes, and review depth; broad triage is distinguished from abstract review |
| [catalog.json](catalog.json) | Inclusion, primary chapter, scope, resources, and venue evidence |
| [proceedings.json](proceedings.json) | Supplement records, screened exclusions, dates, and resource checks |
| [venue-evidence.json](venue-evidence.json) | Official venue matches, including historical metadata corrections |
| [resource-checks.json](resource-checks.json) | Link status and redirects at the snapshot date |
| [bibliography.json](../bibliography.json) | Primary title, first-public date, revision date, and source |

Edit the metadata, then run `python3 scripts/build_review.py` from the repository root. `python3 scripts/build_review.py --check` and `python3 scripts/check_catalog.py` validate generated pages and catalog consistency. Update coverage and screening records when membership changes; follow [CONTRIBUTING](../../CONTRIBUTING.md).
