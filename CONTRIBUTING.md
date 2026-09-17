# Contributing

**Edit one file: [data/papers.json](data/papers.json).** Every paper has one stable ID; its `placements` list selects README tables. Cross-listed papers share title, date, venue, and resources. The older bibliography and nine-month review JSON files are historical evidence, not additional editing targets.

## Three Steps

1. Add or update a paper in `data/papers.json`. Reuse an existing ID when the work is already listed. Use the unversioned arXiv ID, `acl:ANTHOLOGY-ID`, or a stable `paper:slug` for other sources. Copy a nearby entry or the [minimal example](docs/catalog.md#paper-fields).
2. Regenerate the README and check it, using Python 3.10+ with no third-party dependencies:

   ```sh
   python3 scripts/catalog.py render
   python3 scripts/check_catalog.py
   git diff --check
   ```

3. Review the JSON and README diff, then include both in your commit or pull request. The generator handles sorting, resource badges, colors, and tables that are expanded by default.

Do not hand-edit generated rows for routine contributions. If you intentionally edit README tables, keep their paper/section ID comments and import the changes:

```sh
python3 scripts/catalog.py import-readme --output /tmp/papers-import.json
```

Review that file before replacing `data/papers.json`, then render and check again. The import uses the existing JSON to retain precise dates, source evidence, and other undisplayed metadata. It rejects inconsistent cross-lists and unexpected missing rows. See [reverse-import details](docs/catalog.md#reverse-import).

## With an Agent or BibTeX

Ask the agent to read [.agents/skills/update-video-survey/SKILL.md](.agents/skills/update-video-survey/SKILL.md), then provide paper URLs, DOI/arXiv IDs, pasted BibTeX, or a `.bib` file. For example:

> Read `.agents/skills/update-video-survey/SKILL.md`. Add the papers from `/path/to/new-papers.bib`, verify primary metadata and scope, update `data/papers.json`, regenerate the README, and run the checks. Summarize unresolved metadata.

The repository's [AGENTS.md](AGENTS.md) points compatible agents to this workflow. Other agents can read the skill directly. BibTeX supplies candidate citations; its `year`, `month`, or `booktitle` alone does not establish first-public dates or confirmed venue status. The skill does not require a separate BibTeX parser or grant publishing permission.

## Scope & Evidence

- Include reasoning over video, visual generation used for reasoning, and world models relevant to prediction or action. Identify supporting perception methods and visual/planning bridges.
- Separate representation, training, evidence acquisition, and interaction. For executable worlds, distinguish state descriptions, inferred/supplied dynamics, execution, and rendering.
- Use the current primary-source title and first-public date. Keep month-only precision if that is all the source establishes; do not infer a date from an arXiv prefix. Use `date_basis: "proceedings"` when an earlier preprint remains unresolved.
- Confirm venues from proceedings or explicit author acceptance, retaining track/Findings/workshop qualifiers. Otherwise use `arXiv` or `Unverified` as appropriate.
- Set `input_modalities` from verified inputs, using the [shared vocabulary and colors](docs/catalog.md#input-modalities). Text, Video, Audio, and Image describe inputs; tasks, generated outputs, and internal states do not belong in this column. Use `[]` when unsupported or not applicable.
- Include Text for LLM/MLLM pipelines, including fixed/system prompts. Check benchmark names in primary sources; use the actual suite name rather than a title fragment. Mark descriptive labels for unnamed diagnostics with `(study)` and retain `name_evidence`.
- Preserve benchmark columns: **Name, Paper, Link, Task, Time, Venue**. In a benchmark placement, set `name` and `tasks`: `language` for language-model reasoning, `vision` for visual-generation reasoning, both when both are evaluated. This is separate from input modalities; a VLM judge or synthetic test video does not determine Task. Retain evidence in `task_evidence`.
- Keep code, data, projects, and weights in typed `resources`. Weights use `kind: "weights"`; datasets are not checkpoints. GitHub and linked Stars badges, house icons for project pages, and other platform badges are automatic. Do not duplicate generated stars in `badges`. Store Venue as plain text; the generator adds backticks.
- Record primary evidence and review depth in `provenance`. Distinguish author reports, proposed capabilities, and reproduced results. A reachable URL does not establish reproducibility.

Use concise English, consistent chapter emoji, and practical research guidance. Omit editing logs and paper-count summaries; keep sections expanded with `<details open>` and preserve stable anchors. For equations, follow [Modeling Notes](docs/modeling.md): edit the TeX source, regenerate its SVG, inspect it, and check the published image. The rendered SVG is independent of GitHub's client-side math support.

When changing conversion code, also run `python3 -m unittest discover -s tests -v`. The tests exercise round-trip preservation, imports, conflicts, removals, and the complete repository catalog.
