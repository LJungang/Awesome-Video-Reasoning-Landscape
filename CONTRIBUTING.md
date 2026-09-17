# Contributing

This repository is an English-language, curated survey of video reasoning. Keep the existing Markdown tables and newest-first ordering. Contributions may add papers, correct metadata, improve the taxonomy, or clarify evaluation practice.

## Scope and placement

Include a primary paper or technical report with a clear connection to reasoning **over** videos or **through** generated visual trajectories. Explain the contribution beyond generic recognition, captioning, or visual quality. General-purpose architectures and image-only benchmarks may be retained as explicitly labeled foundations, rather than counted as dedicated video-reasoning methods or benchmarks.

Organize the catalog at two levels. Under **Reasoning Representations and Mechanisms**, place language-led reasoning under CoT, generated visual trajectories under CoF, explicit graphs or continuous reasoning states under Structured and Latent, and persistent transition programs or code/learned-model combinations under Executable and Hybrid World Models. Under **Orchestration and Interaction**, place iterative evidence/tool/generation loops under Interleaved and causal online processing under Streaming. These levels are complementary; do not present all branches as mutually exclusive paradigms.

For executable/hybrid entries, state whether the work is a **direct video-world system**, a **bridge from visual evidence**, or a **planning foundation**. Distinguish static scene construction, state description, executable dynamics, learned execution prediction, and visual rendering. Record where state comes from and whether video generation determines transitions or realizes externally specified state. Bridge benchmarks must be visibly separated from direct video benchmarks.

Cross-list only when a work contributes to both sections; reuse the same paper title, first-public date, and venue. A method that introduces a benchmark may appear in both catalogs. For perspective sections, distinguish paper-supported findings, author-proposed capabilities, and the survey's own testable research agenda. See the [world-model case study](docs/world-models.md) for an example.

## Table format

For a method with input modalities:

```markdown
| [Paper title](https://arxiv.org/abs/YYMM.NNNNN) | [GitHub](https://github.com/author/repo) | `N/A` | Text; Video | YYYY-MM | `arXiv` |
```

For a method in an existing five-column table, omit the modality cell. For a benchmark:

```markdown
| Benchmark name | [Paper title](https://arxiv.org/abs/YYMM.NNNNN) | [Data](https://huggingface.co/datasets/author/dataset) | Streaming; temporal QA | YYYY-MM | `arXiv` |
```

Preserve existing modality badges where used. Prefer readable resource labels and `<br>` for multiple links inside a cell; do not wrap `<br>` in backticks. Escape literal pipe characters within cells as `\|`.

## Evidence and metadata

- Link the primary abstract, proceedings paper, or official technical report. Use stable, unversioned arXiv `/abs/` links for the live catalog. Record the checked version/date in research notes when a version matters.
- `Time` is the first public paper date in `YYYY-MM`, not the latest revision or acceptance date. Use primary metadata, not the arXiv identifier prefix: these can differ. Sort each table by this date descending; ties may preserve the existing order.
- Record a venue only when supported by official proceedings or an unambiguous author acceptance statement. Preserve workshop, Findings, and track qualifiers. Submission, “conference format,” and ambiguous acceptance statements are not proof of publication. Otherwise use `arXiv`.
- Use the current verified title. Record significant renames and former aliases in research notes so readers can find the older literature.
- **Checkpoint** is for model weights or a relevant model collection, not training data, test data, a project page, or an unrelated model. Place datasets and project pages in the code/resources column. `N/A` means no verified resource is recorded here; it does not establish that none exists.
- Verify that resource links refer to the correct project. HTTP success verifies reachability only, not repository contents or reproducibility. Report access failures without calling a resource nonexistent.
- Separate author-reported results from independently reproduced findings. Do not rank papers with unmatched backbones, frame/audio inputs, tool budgets, or evaluation protocols.

## Review and validation

Explain the new entry's task, representation, evidence acquisition, and evaluation relevance. For research updates, add a dated source trail to [research notes](docs/research-notes.md); [bibliography.json](docs/bibliography.json) stores checked title/date metadata and author venue statements, not a claim that all older links have been revalidated.

Run:

```sh
python3 scripts/check_catalog.py
git diff --check
```

The script checks Markdown table shape, reverse chronological order, local links/anchors, duplicate identities within a table, cross-list metadata consistency, known first-public dates, and checkpoint/data separation. External availability and scientific accuracy require a separate source review. Inspect the rendered Markdown when changing layout or equations. Use GitHub's fenced `math` blocks and supported macros; `\operatorname` is currently blocked by GitHub, so use an appropriate supported alternative such as `\mathrm`. The static check flags known unsupported macros but cannot replace MathJax or published-page verification. Preserve established explicit anchors when restructuring sections.
