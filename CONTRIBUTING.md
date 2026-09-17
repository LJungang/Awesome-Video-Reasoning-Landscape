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
python3 scripts/check_catalog.py
git diff --check
```

The script checks tables, dates, local links, cross-list consistency, resource columns, and known blocked math macros. Verify sources and external links separately.

Use fenced `math` blocks and GitHub-supported macros (`\mathrm` rather than the currently blocked `\operatorname`). Check MathJax, Mermaid, and published output when changing formulas or diagrams.
