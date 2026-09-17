#!/usr/bin/env python3
"""Render the dated review index from checked metadata; no network or dependencies."""
import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'docs/review-2026'


def title_cell(title):
    return html.escape(title, quote=False).replace('|', r'\|').replace('[', '&#91;').replace(']', '&#93;')


def resources_cell(links):
    return '<br>'.join(f'[{link["label"]}]({link["url"]})' for link in links) or '`N/A`'


def render():
    manifest = json.loads((DATA / 'catalog.json').read_text())
    bibliography = json.loads((ROOT / 'docs/bibliography.json').read_text())['papers']
    outputs = {}
    for branch, config in manifest['branches'].items():
        papers = [(key, entry) for key, entry in manifest['papers'].items()
                  if entry['branch'] == branch and entry['location'] == 'review']
        papers.sort(key=lambda item: bibliography[item[0]]['first_public'], reverse=True)
        lines = [f'# {config["title"]}', '',
                 '[Review map](README.md) · [Main survey](../../README.md#paradigms)', '',
                 config['description'], '',
                 f'**{len(papers)} additions · 2025-12-18–2026-09-17.** '
                 'Dates are first-public months. `N/A` means no checked resource link is recorded. '
                 'Venue evidence and review depth are in [catalog.json](catalog.json). '
                 'See also the [proceedings supplement](proceedings.md), whose date basis differs.', '',
                 '| **Title** | **Resources** | **Focus / scope** | **Time** | **Venue** |',
                 '| :--- | :--- | :--- | :--- | :--- |']
        for key, entry in papers:
            paper = bibliography[key]
            title = title_cell(entry.get('display_title', paper['title']))
            resources = resources_cell(entry['resources'])
            lines.append(f'| [{title}](https://arxiv.org/abs/{key}) | {resources} | '
                         f'{entry["focus"]} | {paper["first_public"][:7]} | `{entry["venue"]}` |')
        outputs[DATA / f'{branch}.md'] = '\n'.join(lines) + '\n'
    supplement = json.loads((DATA / 'proceedings.json').read_text())['papers']
    lines = ['# Proceedings Supplement', '', '[Review map](README.md) · [Main survey](../../README.md#paradigms)', '',
             f'**{len(supplement)} additional papers** located in official ACL 2026 proceedings. '
             'July is the proceedings publication month; an earlier preprint date was not resolved. '
             'These entries are excluded from the first-public monthly counts. '
             'Abstracts were reviewed; results were not reproduced. '
             'Sources and inclusion decisions: [proceedings.json](proceedings.json).', '',
             '| **Title** | **Resources** | **Focus / scope** | **Publication** | **Venue** |',
             '| :--- | :--- | :--- | :--- | :--- |']
    for paper in supplement:
        focus = f'[{paper["focus"]}]({paper["branch"]}.md)'
        lines.append(f'| [{title_cell(paper["title"])}]({paper["source"]}) | '
                     f'{resources_cell(paper["resources"])} | {focus} | {paper["publication"]} | `{paper["venue"]}` |')
    outputs[DATA / 'proceedings.md'] = '\n'.join(lines) + '\n'
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='fail if generated pages are stale')
    args = parser.parse_args()
    stale = []
    for path, content in render().items():
        if args.check:
            if not path.exists() or path.read_text() != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(content)
    if stale:
        parser.exit(1, 'Stale review pages: ' + ', '.join(stale) + '\n')
    print('OK: review pages match checked metadata.' if args.check else 'Rendered review pages.')


if __name__ == '__main__':
    main()
