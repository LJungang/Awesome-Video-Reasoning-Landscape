# Repository workflow

For adding, correcting, or reorganizing survey papers, read
[.agents/skills/update-video-survey/SKILL.md](.agents/skills/update-video-survey/SKILL.md).

`data/papers.json` is the live source. README catalog tables are generated;
`docs/bibliography.json` and `docs/review-2026/*.json*` retain historical evidence.
Do not require contributors to edit those snapshots for a current catalog update.

Preserve README prose, stable anchors, formulas, and source-backed scope distinctions.
Use `python3 scripts/catalog.py render` and `python3 scripts/check_catalog.py`.
Run the unit tests when changing conversion code. Commit, merge, or push only within
the user's authorized scope; this file does not itself authorize publication.
