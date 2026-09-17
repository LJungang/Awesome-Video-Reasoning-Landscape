# Structured Catalog

[data/papers.json](../data/papers.json) is the only live paper-data source. [papers.schema.json](../data/papers.schema.json) documents its shape; the Python converter also checks dates, identities, URLs, duplicate placements, and weights/data distinctions. It uses Python 3.10+ and the standard library.

`papers` is keyed by stable ID. Each record renders once per `placements` entry, identified in Markdown by `<!-- paper:ID -->` and the enclosing `<!-- section:ID -->`. Shared citation fields prevent cross-list drift. Every cataloged paper appears in the main README; historical source snapshots remain available under `docs/`.

<a id="paper-fields"></a>

## Paper Fields

Minimal example, using an already cataloged paper as a template rather than a new duplicate:

```json
"2608.25927": {
  "title": "Code World Model: Coding Agent as World Brain",
  "url": "https://arxiv.org/abs/2608.25927",
  "date": "2026-08-26",
  "date_basis": "first-public",
  "venue": "arXiv",
  "input_modalities": ["text", "image"],
  "resources": [],
  "placements": [
    {
      "section": "executable",
      "focus": "Direct video system; executable state and learned rendering"
    }
  ],
  "provenance": {
    "sources": ["https://arxiv.org/abs/2608.25927"],
    "review_level": "abstract"
  }
}
```

Preserve the existing record's resources and evidence when editing it; the example shows only the minimal structure.

| Field | Meaning |
| :--- | :--- |
| Paper key | Unversioned arXiv ID, `acl:2026.acl-long.56`, or stable `paper:slug`; never one new ID per category |
| `title`, `url` | Verified title and primary paper/report URL; links in generated cells use escaped labels |
| `date` | ISO month, day, or UTC timestamp: `YYYY-MM`, `YYYY-MM-DD`, or `YYYY-MM-DDTHH:MM:SSZ`; the table displays the month |
| `date_basis` | `first-public`, or `proceedings` when an earlier preprint is unresolved; the latter renders `(proc.)` |
| `venue` | Plain-text venue, including track qualifiers; otherwise `arXiv` or `Unverified`. The generator adds backticks |
| `input_modalities` | Verified input IDs from the top-level `modalities` registry; `[]` renders `N/A` |
| `resources` | Typed resource objects; an empty list renders `N/A` |
| `placements` | One or more `{section, focus}` objects; `name` supplies the benchmark Name column. Benchmark placements also have `tasks` and optional `task_evidence`. `focus` remains hidden scope metadata |
| `provenance` | Source URLs, review depth, venue evidence, BibTeX, aliases, and notes; retained through reverse imports |

A resource contains `kind`, `label`, and `url`. Kinds are `code`, `data`, `project`, `weights`, `paper`, and `other`. Optional `evidence` stores verification details; optional `badges` stores additional `{alt, url}` images. GitHub repository links automatically display a GitHub badge and a separate Stars badge linking to `/stargazers`; do not store these generated stars in JSON. Project pages use a house badge. Hugging Face and ModelScope distinguish datasets from checkpoints. Branded badges use `resource:kind` alt text and preserve the descriptive `label` in JSON. Other links display `kind: label`. URLs must percent-encode spaces, pipes, and parentheses.

<a id="input-modalities"></a>

## Input Modalities & Colors

`modalities` in `data/papers.json` is the shared vocabulary and palette. Each ID defines a `label`, a unique six-digit uppercase hex `color`, and an input `description`. The README legend is generated from it. Use `text`, `video`, `audio`, or `image` for their actual inputs; use `depth`, `point-cloud`, `action`, `state`, `code`, or `mesh` only when those signals are supplied to the evaluated system. Add a new registry entry only for a distinct input type.

- Label the system or benchmark interface, including supported optional inputs; store scope and primary-source evidence under `provenance.input_modalities`.
- Sampled frames from an observed clip are Video. A standalone reference image is Image. Speech waveforms are Audio; supplied transcripts are Text.
- LLM/MLLM pipelines include Text for questions, fixed instructions, system prompts, and tool instructions. Describe the complete model pipeline, even if a video encoder or query-free memory component does not itself consume text. An external LLM judge alone does not establish a Text input to the evaluated generator.
- Generated videos, inferred graphs, internal code, training-only signals, and task names are not input labels. A controller's output action is not an Action input to that controller.
- Leave unsupported modalities unassigned. `[]` means unrecorded or not applicable, including surveys without one evaluated interface. A partially annotated record is not an exhaustive capability claim.

Badges use shared Markdown references to keep the README compact. The importer verifies reference URLs, labels, and resource purpose; change the registry and regenerate to update colors. Resource styles live in `scripts/catalog.py`; contributors normally supply only typed URLs.

`focus` accepts concise inline Markdown; titles, names, venue names, and link labels are plain text. Do not place raw HTML or line breaks in catalog fields. Entities protect pipes and brackets during conversion. Dates sort newest first, using full precision when known and the stable ID as a tie-breaker.

The `groups` and `sections` objects define order, stable anchors, titles, and descriptions. To add a branch, add a section with an existing `group` (or define a new group). Sections use `<details open>`: expanded by default, with no paper-count summaries. Keep anchors outside `<details>` and blank lines around tables so GitHub renders them correctly. The generated region is bounded by `catalog:start` and `catalog:end`; introductory prose, formulas, the evaluation guide, and related resources live outside it.

## Benchmark Tables

Set a section's `table` to `benchmark` to retain the original columns: **Name, Paper, Link, Task, Time, Venue**. Ordinary sections keep **Input modalities**; benchmark tables instead show the evaluated model family in **Task**.

- `tasks: ["language"]`: reasoning by language models, including multimodal LMs and coding agents.
- `tasks: ["vision"]`: reasoning by image/video generation models.
- Include both only when both families are evaluated. Use `[]` for unresolved or inapplicable cases, such as a latent-control diagnostic without a language or visual-generation reasoning track.
- Generated benchmark data, a VLM judge, and a coding agent's rendered output do not establish a generation-model reasoning track. Record the actual evaluation target in `task_evidence`.

Find the official benchmark name in the abstract, full paper, or project page; it may differ from the proposed method's name or the paper's title. Record source evidence in `name_evidence` with `kind: "author-named"`. An unnamed diagnostic study can use a short descriptive `name` ending in `(study)`, with `kind: "descriptive"`; do not invent an official acronym. Task badges have a separate palette in `BENCHMARK_TASKS` in the converter: `language` uses `#AEC6DF`, `vision` uses `#C3E6CB`. They are not input-modality IDs.

<a id="reverse-import"></a>

## Conversion Commands

Run from the repository root:

```sh
# JSON -> README; changes only the managed catalog block.
python3 scripts/catalog.py render

# Validate data, synchronization, and JSON -> README -> JSON round-trip.
python3 scripts/catalog.py check

# README -> JSON candidate, using existing JSON as the metadata base.
python3 scripts/catalog.py import-readme --output /tmp/papers-import.json

# Alternate paths for isolated previews or tests.
python3 scripts/catalog.py render --data /tmp/papers-import.json --output /tmp/README-preview.md
```

After reviewing the imported candidate, copy it to `data/papers.json`, render, and run `python3 scripts/check_catalog.py`. That repository check also validates local links, Markdown structure, math macros, and archived review consistency. `scripts/build_review.py` remains a compatibility alias for render/check.

Reverse import updates visible paper fields, ordinary-table input modalities, benchmark names/tasks, and section membership. The existing JSON preserves precise dates, hidden inputs for benchmark-only records, placement `focus`, task evidence, branded resource labels, resource evidence, and BibTeX. A new benchmark-only row starts with empty input modalities. Changing the displayed month or date basis resets date precision. A README alone cannot recover metadata it never displayed.

All cross-lists must agree on title, URL, date, venue, resources, and input modalities; inconsistent edits fail. Keep Venue in backticks and retain badge reference definitions. Missing sections, malformed rows, duplicate IDs/URLs, and unexpected removals fail before writing. For a deliberate removal, pass `--allow-removals`; removing the last placement removes that paper record. A new row needs a stable `paper` comment. Normal contributors should add it in JSON instead.

The converter writes atomically after validation. `check` is read-only. It does not fetch sources or certify scientific claims; the [agent skill](../.agents/skills/update-video-survey/SKILL.md) and [contributor rules](../CONTRIBUTING.md) cover evidence review.
