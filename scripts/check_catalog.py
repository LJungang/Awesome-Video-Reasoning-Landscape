#!/usr/bin/env python3
"""Offline structural and metadata checks for the survey; standard library only."""
import datetime
from collections import Counter, defaultdict
import html
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAPER = re.compile(r'https://arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?')
LINK = re.compile(r'(?<!!)\[[^\]\n]+\]\(([^\s)]+)\)')
DATE = re.compile(r'^\d{4}-(0[1-9]|1[0-2])$')
errors = []
records = {}
locations = defaultdict(list)
from catalog import load, render_readme, import_readme, CatalogError
live = load(ROOT / 'data/papers.json')
metadata = {key: {'first_public': paper['date']} for key, paper in live['papers'].items()}
counts = {'tables': 0, 'rows': 0}


def fail(path, number, message):
    errors.append(f'{path.relative_to(ROOT)}:{number}: {message}')


def cells(line):
    return [c.strip() for c in re.split(r'(?<!\\)\|', line.strip())[1:-1]]


def visible_title(cell):
    match = re.search(r'\[([^\]]+)\]\(https://arxiv\.org/', cell)
    return ' '.join(html.unescape(match[1]).split()) if match else ''


for path in [ROOT / 'README.md', ROOT / 'CONTRIBUTING.md', ROOT / 'AGENTS.md',
             *sorted((ROOT / '.agents').rglob('*.md')), *sorted((ROOT / 'docs').rglob('*.md'))]:
    source = path.read_text()
    # GitHub's math-renderer macro restrictions, checked 2026-09-17.
    # Parse math before removing fenced examples from the Markdown checks below.
    forbidden = {
        'DeclareMathOperator', 'DeclarePairedDelimiters', 'renewtagform',
        'newtagform', 'colorbox', 'fcolorbox', 'hphantom', 'vphantom',
        'phantom', 'operatorname', 'Newextarrow', 'definecolor',
        'mathchoice', 'unicode', 'mmlToken',
    }
    expressions = list(re.finditer(r'^```math\n(.*?)^```', source, re.S | re.M))
    expressions += list(re.finditer(r'\$`([^`\n]+)`\$', source))
    for expression in expressions:
        macros = set(re.findall(r'\\([A-Za-z]+)', expression[1]))
        blocked = sorted(macros & forbidden)
        if blocked:
            fail(path, source[:expression.start()].count('\n') + 1,
                 f'GitHub blocks these math macros: {", ".join(blocked)}')
    if any(ord(c) < 32 and c not in '\n\t' for c in source):
        fail(path, 1, 'unexpected control character (possibly an escaped TeX command)')
    # Ignore comments and fenced examples; neither is rendered catalog content.
    source = re.sub(r'<!--.*?-->', lambda m: '\n' * m[0].count('\n'), source, flags=re.S)
    source = re.sub(r'^```.*?^```[^\n]*', lambda m: '\n' * m[0].count('\n'), source, flags=re.S | re.M)
    ids = re.findall(r'<a id="([^"]+)"', source)
    if len(ids) != len(set(ids)):
        fail(path, 1, 'duplicate explicit anchor')
    lines = source.splitlines()
    for number, line in enumerate(lines, 1):
        for target in LINK.findall(line):
            url = urlsplit(html.unescape(target))
            if url.scheme or url.netloc:
                continue
            dest = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not dest.is_file():
                fail(path, number, f'missing local file: {target}')
            elif url.fragment:
                # Repository-authored local fragment links use explicit stable anchors.
                anchors = re.findall(r'<a id="([^"]+)"', dest.read_text())
                if unquote(url.fragment) not in anchors:
                    fail(path, number, f'missing explicit anchor: {target}')
        if line.startswith('|') and ('`<br>`' in line or 'github.comLJungang' in line):
            fail(path, number, 'malformed HTML or URL')
    i = 0
    while i < len(lines):
        if not lines[i].startswith('|'):
            i += 1
            continue
        start = i
        while i < len(lines) and lines[i].startswith('|'):
            i += 1
        if i < len(lines) and lines[i].strip():
            fail(path, i + 1, 'blank line required after table; GitHub can consume the next anchor as a row')
        table = [cells(line) for line in lines[start:i]]
        width = len(table[0])
        for offset, row in enumerate(table):
            if len(row) != width:
                fail(path, start + offset + 1, f'expected {width} table cells, got {len(row)}')
        if len(table) < 2 or not all(re.fullmatch(r':?-+:?', c) for c in table[1]):
            fail(path, start + 1, 'missing table separator')
        if '**Time**' not in table[0]:
            continue
        counts['tables'] += 1
        date_col = table[0].index('**Time**')
        venue_col = table[0].index('**Venue**')
        ckpt_col = table[0].index('**Checkpoint**') if '**Checkpoint**' in table[0] else None
        previous = '9999-12'
        seen = set()
        for offset, row in enumerate(table[2:], 2):
            number = start + offset + 1
            counts['rows'] += 1
            if len(row) != width:
                continue
            date = row[date_col].removesuffix(' (proc.)')
            if not DATE.fullmatch(date):
                fail(path, number, f'invalid month: {date}')
            elif date > datetime.date.today().strftime('%Y-%m'):
                fail(path, number, f'future first-public month: {date}')
            if date > previous:
                fail(path, number, f'out of date order: {date} after {previous}')
            previous = date
            if ckpt_col is not None and ('/datasets/' in row[ckpt_col] or '[Project' in row[ckpt_col]):
                fail(path, number, 'dataset/project in checkpoint column')
            paper = PAPER.search(' | '.join(row))
            if not paper:
                continue
            identity = paper[1]
            if identity in seen:
                fail(path, number, f'duplicate paper within table: {identity}')
            seen.add(identity)
            if identity in metadata and date != metadata[identity]['first_public'][:7]:
                fail(path, number, f'date disagrees with checked primary metadata: {identity}')
            record = (visible_title(' | '.join(row)), date, row[venue_col])
            if identity in records and records[identity] != record:
                fail(path, number, f'inconsistent cross-list title/date/venue: {identity}')
            records[identity] = record
            locations[identity].append(path)

# The dated expansion must be traceable to its primary metadata and screening log.
review = ROOT / 'docs/review-2026'
manifest_path = review / 'catalog.json'
manifest = json.loads(manifest_path.read_text())
catalog = manifest['papers']
snapshot_metadata = json.loads((ROOT / 'docs/bibliography.json').read_text())['papers']
coverage = json.loads((review / 'coverage.json').read_text())
screened_rows = [json.loads(line) for line in (review / 'screening.jsonl').read_text().splitlines()]
screened = {row['id']: row for row in screened_rows}
resources = json.loads((review / 'resource-checks.json').read_text())
supplement = json.loads((review / 'proceedings.json').read_text())['papers']
months = defaultdict(lambda: {'existing': 0, 'added': 0})


def review_fail(message):
    fail(manifest_path, 1, message)


if len(screened) != len(screened_rows):
    review_fail('duplicate screening identity')
if {key for key, row in screened.items() if row['decision'] == 'included'} != set(catalog):
    review_fail('screening inclusion set disagrees with catalog')
for identity, entry in catalog.items():
    if identity not in snapshot_metadata:
        review_fail(f'missing archived primary metadata: {identity}')
        continue
    paper = snapshot_metadata[identity]
    date = paper['first_public'][:10]
    if not manifest['window']['start'] <= date <= manifest['window']['end']:
        review_fail(f'outside archived review window: {identity}')
    location, branch = entry['location'], entry['branch']
    if location not in {'README', 'review'} or (branch not in manifest['branches'] and not (location == 'README' and branch == 'existing')):
        review_fail(f'invalid archived chapter or location: {identity}')
        continue
    row = screened.get(identity, {})
    if any(row.get(field) != value for field, value in {
        'title': paper['title'], 'first_public': date, 'branch': branch,
        'location': location, 'review_level': entry['review_level'],
    }.items()):
        review_fail(f'screening metadata differs: {identity}')
    if entry['review_level'] not in {'abstract', 'abstract-excerpt', 'previous-review'}:
        review_fail(f'unreviewed catalog entry: {identity}')
    if not entry['focus'].strip():
        review_fail(f'missing contribution/scope: {identity}')
    for link in entry['resources']:
        if resources.get(link['url'], {}).get('status') != 200:
            review_fail(f'resource lacks a successful recorded check: {identity}: {link["url"]}')
    months[date[:7]]['existing' if location == 'README' else 'added'] += 1

branch_counts = dict(Counter(entry['branch'] for entry in catalog.values() if entry['location'] == 'review'))
expected_counts = {
    'window': manifest['window'], 'window_records': len(catalog),
    'existing_window_records': sum(entry['location'] == 'README' for entry in catalog.values()),
    'new_arxiv_records': sum(branch_counts.values()), 'branches': branch_counts,
    'months': dict(months), 'primary_metadata_records': len(screened),
    'screening': dict(Counter(row['decision'] for row in screened_rows)),
    'proceedings_supplement': len(supplement),
}
for field, value in expected_counts.items():
    if coverage.get(field) != value:
        review_fail(f'stale coverage field: {field}')
sources = [paper['source'] for paper in supplement]
if len(sources) != len(set(sources)):
    review_fail('duplicate proceedings supplement source')
for paper in supplement:
    if paper['branch'] not in manifest['branches'] or paper['review_level'] != 'abstract':
        review_fail(f'invalid proceedings placement/review: {paper["title"]}')
    if not DATE.fullmatch(paper['publication']) or not paper['date_basis'].startswith('first located proceedings'):
        review_fail(f'proceedings date basis missing: {paper["title"]}')

# Exhausted pagination is a checkable property, not an inferred coverage claim.
searches = json.loads((review / 'searches.json').read_text())
query_pages = defaultdict(list)
for page in searches['arxiv_pages']:
    query_pages[page['query']].append(page)
for query, pages in query_pages.items():
    cursor = 0
    for page in sorted(pages, key=lambda page: page['start']):
        if page['start'] != cursor or page['total'] != pages[0]['total']:
            review_fail(f'incomplete/inconsistent pagination: {query}')
        cursor += page['returned']
    if cursor != pages[0]['total']:
        review_fail(f'unexhausted query: {query}')
if coverage['primary_query_unique'] != sum(bool(set(row['queries']) & set(query_pages)) for row in screened_rows):
    review_fail('stale unique query count')

try:
    readme = (ROOT / 'README.md').read_text()
    if readme != render_readme(live, readme):
        fail(ROOT / 'README.md', 1, 'catalog is stale; run scripts/catalog.py render')
    if import_readme(readme, live) != live:
        fail(ROOT / 'data/papers.json', 1, 'JSON/README round-trip changed data')
except (CatalogError, KeyError, TypeError) as exc:
    fail(ROOT / 'data/papers.json', 1, str(exc))

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f"OK: {counts['tables']} catalog tables, {counts['rows']} entries, "
      f"{len(records)} unique arXiv papers; canonical JSON, round-trip, local links, math macros, and archived evidence checked.")
