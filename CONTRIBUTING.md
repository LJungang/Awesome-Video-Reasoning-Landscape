# Contributing

Keep the survey in English, preserve catalog tables and stable anchors, and sort papers newest first.

## Scope & Placement

Include work on reasoning over video, through visual generation, or with world models relevant to prediction and action. State its contribution beyond recognition or visual quality.

| View | Branches |
| :--- | :--- |
| **Reasoning Engines** | CoT; CoF; Structured & Latent; Executable & Hybrid |
| **Interaction Loops** | Interleaved; Streaming |

These views overlap. Cross-list only for distinct contributions, using consistent titles, dates, and venues. Mark executable-world entries as **direct video systems**, **visual bridges**, or **planning foundations**. Separate bridge benchmarks from video-QA benchmarks.

Distinguish state descriptions, transition models, executed programs, and visual renderers. Separate reported results from proposed capabilities and the survey's research agenda.

## Entry Format

Method with modalities; omit the modality cell in five-column tables:

```markdown
| [Paper title](https://arxiv.org/abs/YYMM.NNNNN) | [GitHub](https://github.com/author/repo) | `N/A` | Text; Video | YYYY-MM | `arXiv` |
```

Benchmark:

```markdown
| Name | [Paper title](https://arxiv.org/abs/YYMM.NNNNN) | [Data](https://huggingface.co/datasets/author/dataset) | Streaming; temporal QA | YYYY-MM | `arXiv` |
```

Retain existing badges. Use `<br>` between resources and escape cell-internal pipes as `\|`.

The dated review uses a compact five-column index:

```markdown
| [Paper title](https://arxiv.org/abs/YYMM.NNNNN) | [GitHub](https://github.com/author/repo) | Contribution / scope | YYYY-MM | `arXiv` |
```

Edit [catalog.json](docs/review-2026/catalog.json) and [bibliography.json](docs/bibliography.json), then run `python3 scripts/build_review.py`; do not edit generated chapter tables directly. Each new paper has one primary chapter. Chapter counts cover additions, while previously cataloged in-window papers remain in the main survey. Preserve source-backed scope labels and distinguish proposed frameworks from evaluated systems.

For proceedings papers with unresolved preprint dates, use [proceedings.json](docs/review-2026/proceedings.json) and its separate publication-date table. Do not count conference publication as a new first-public date. Update coverage, screening decisions, and the review map when adding or reclassifying papers.

## Source Rules

- **Paper:** primary abstract, proceedings, or official report; prefer unversioned arXiv `/abs/` URLs.
- **Title:** current verified title; preserve significant former aliases in research notes.
- **Time:** first public date, not revision or acceptance. Check metadata; arXiv prefixes can differ. Preserve order within tied months.
- **Venue:** official proceedings or explicit author acceptance; retain workshop/Findings/track qualifiers. Otherwise use `arXiv`.
- **Checkpoint:** relevant weights or model collections. Put datasets and project pages in resources. `N/A` means no verified link recorded.
- **Claims:** distinguish author reports from reproduced results; compare matched inputs, models, and budgets. Reachable links do not certify reproducibility.

Record review scope and sources in [research notes](docs/research-notes.md); update [bibliography.json](docs/bibliography.json) when changing checked metadata.

## Validation

```sh
python3 scripts/build_review.py --check
python3 scripts/check_catalog.py
git diff --check
```

The scripts check generated pages, recursive Markdown links, tables, dates, cross-list consistency, review membership and counts, resource columns, and known blocked math macros. Verify sources and external links separately.

Use fenced `math` blocks and GitHub-supported macros (`\mathrm` rather than the currently blocked `\operatorname`). Check MathJax, Mermaid, and published output when changing formulas or diagrams.
