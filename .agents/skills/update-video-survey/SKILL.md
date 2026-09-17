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
- Read at least the abstract to establish scope. Choose an existing `placements[].section`; add a concise `focus` when it clarifies mechanism or scope. Cross-list only for distinct contributions. Preserve existing placement-specific names, badges, resources, and provenance when updating a record.
- Keep supplied state/rules, inferred dynamics, simulation, and learned rendering distinct. Label visual bridges and planning foundations. Do not present a framework proposal as an evaluated capability.

## Update and verify

1. Edit **only `data/papers.json`** for paper data. Each paper owns shared citation/resources and a list of placements. Read the schema reference for optional fields or a new section. Older bibliography/review JSON files are frozen evidence, not sources to synchronize by hand.
2. Verify resource purpose before assigning `kind`; datasets are not weights. Store venue/source evidence, review depth, aliases, and unresolved details in `provenance`. Report uncertainty rather than guessing; keep unsupported venue claims `arXiv`/`Unverified` as appropriate.
3. Run:

   ```sh
   python3 scripts/catalog.py render
   python3 scripts/check_catalog.py
   git diff --check
   ```

4. Review the diff for retained citations, correct placements, dates, and untouched narrative/formulas. If conversion code changed, run `python3 -m unittest discover -s tests -v`. Formula or diagram edits additionally need MathJax/Mermaid and published-output checks where available.
5. Report additions/corrections, validation, and unresolved sources. Commit/merge/push only when the user has authorized those actions in the active task; the skill itself grants no publishing permission.

## Intentional README edits

JSON editing is the normal path. To import an edited README, retain `catalog`, `section`, and `paper` comments, then use:

```sh
python3 scripts/catalog.py import-readme --output /tmp/papers-import.json
```

Inspect the candidate before replacing `data/papers.json`, then render/check. Import preserves undisplayed metadata using the existing JSON. Conflicting cross-lists are errors; fix their common record in JSON. Use `--allow-removals` only for intended row removal, not to bypass a truncated/malformed README. The README is not a backup of metadata it does not display.
