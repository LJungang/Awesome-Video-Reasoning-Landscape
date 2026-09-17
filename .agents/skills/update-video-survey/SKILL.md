---
name: update-video-survey
description: Maintain the Awesome Video Reasoning Landscape catalog from paper URLs, arXiv or DOI identifiers, BibTeX, or research notes; verify metadata and placement, edit the canonical JSON, and synchronize README tables.
---

# Update the Video Survey

Run from the repository root. Read [CONTRIBUTING.md](../../../CONTRIBUTING.md) for scope and [docs/catalog.md](../../../docs/catalog.md) for fields and conversion commands. This skill is shared with the repository; another agent can read this file directly.

## Intake and placement

- Treat URLs, DOI/arXiv IDs, BibTeX entries, and `.bib` files as candidate citations. For BibTeX, extract title, authors, identifiers, URL, and venue claims; preserve useful original citation text under `provenance.bibtex`. Read nested/protected titles carefully. No particular BibTeX parser is required.
- Search `data/papers.json` by stable ID, primary URL, title, and aliases before adding. A revision, renamed preprint, or conference version is usually the same work. Keep distinct papers with similar acronyms separate.
- Resolve title and publication date from primary metadata or proceedings. BibTeX publication year/month and the arXiv ID prefix are not first-public evidence. Keep month precision when necessary. If an earlier preprint date is unresolved, use the proceedings date with `date_basis: "proceedings"`; do not invent a day.
- Read at least the abstract to establish scope. Choose an existing `placements[].section`; add a concise `focus` as hidden scope metadata when useful. Cross-list only for distinct contributions. Preserve placement names, resource badges, and provenance.
- Set paper-level `input_modalities` using the registry in `data/papers.json`. Label supplied inputs, including optional conditioning; exclude tasks, generated outputs, inferred state/code, and training-only signals. For example, observed clip frames are Video, a reference image is Image, and speech is Audio. Keep `[]` when evidence is insufficient or no single interface applies. Record sources and interface limits under `provenance.input_modalities`.
- For an LLM/MLLM reasoning pipeline, include `text`: questions, fixed instructions, system prompts, and tool instructions all count. Annotate the full paper-level pipeline; a query-free video encoder or memory module does not make the downstream language-model system video-only. Do not infer a language-model input solely from an external evaluation judge.
- Preserve benchmark layout **Name, Paper, Link, Task, Time, Venue** (`sections[].table: "benchmark"`). Set placement `name` and `tasks`: `language` for evaluated language models, including MLLMs and coding agents; `vision` for evaluated image/video generators; both only for both families. Store the evaluation target and source in `task_evidence`. Do not classify from input modality, synthetic benchmark data, VLM judges, or rendered coding-agent output. Leave `tasks: []` when unresolved or inapplicable.
- Find the benchmark's actual name in its abstract, paper, or official project page; it may differ from the paper title or proposed method. Record `name_evidence`. For an unnamed diagnostic study, use a concise descriptive label ending in `(study)` with `name_evidence.kind: "descriptive"`; do not invent an official acronym or leave `N/A` without checking sources.
- Keep supplied state/rules, inferred dynamics, simulation, and learned rendering distinct. Label visual bridges and planning foundations. Do not present a framework proposal as an evaluated capability.

## Update and verify

1. Edit **only `data/papers.json`** for paper data. Each paper owns shared citation/resources and a list of placements. Read the schema reference for optional fields or a new section. Older bibliography/review JSON files are frozen evidence, not sources to synchronize by hand.
2. Verify resource purpose before assigning `kind`; datasets are not weights. Resource badges are automatic: GitHub plus Stars linking to `/stargazers`, a house icon for project pages, and typed Hugging Face/ModelScope badges. Do not store generated star badges in JSON. Store plain-text Venue; rendering adds backticks. Use the shared input palette and the separate benchmark Task palette; never mix the two vocabularies.
3. Run:

   ```sh
   python3 scripts/catalog.py render
   python3 scripts/check_catalog.py
   git diff --check
   ```

4. Review retained citations, benchmark names/tasks, inputs, dates, and narrative/formulas. Keep the README focused on research routes and comparisons; use consistent chapter emoji and stable anchors. Omit editing logs and paper-count summaries. Use `<details open>` and blank table boundaries. If conversion code changed, run `python3 -m unittest discover -s tests -v`. Equations live in [Modeling Notes](../../../docs/modeling.md) with editable `assets/math/*.tex` and checked-in SVGs: run `npm ci --prefix tools/math`, `npm run render --prefix tools/math`, and `npm run check --prefix tools/math`, then inspect the images and published links. Do not equate the presence of GitHub math markup with successful client rendering.
5. Report additions/corrections, validation, and unresolved sources. Commit/merge/push only when the user has authorized those actions in the active task; the skill itself grants no publishing permission.

## Intentional README edits

JSON editing is the normal path. To import an edited README, retain `catalog`, `section`, and `paper` comments, then use:

```sh
python3 scripts/catalog.py import-readme --output /tmp/papers-import.json
```

Inspect the candidate before replacing `data/papers.json`, then render/check. Retain backticks around Venue, registered modality badges, and shared badge definitions. Import preserves hidden focus and source metadata using the existing JSON. Conflicting cross-lists are errors; fix their common record in JSON. Use `--allow-removals` only for intended row removal, not to bypass a truncated/malformed README. The README is not a backup of metadata it does not display.
