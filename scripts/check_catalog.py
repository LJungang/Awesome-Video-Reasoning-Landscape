#!/usr/bin/env python3
"""Offline structural and metadata checks for the survey; standard library only."""
import datetime
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
metadata = json.loads((ROOT / 'docs/bibliography.json').read_text())['papers']
counts = {'tables': 0, 'rows': 0}


def fail(path, number, message):
    errors.append(f'{path.relative_to(ROOT)}:{number}: {message}')


def cells(line):
    return [c.strip() for c in re.split(r'(?<!\\)\|', line.strip())[1:-1]]


def visible_title(cell):
    match = re.search(r'\[([^\]]+)\]\(https://arxiv\.org/', cell)
    return ' '.join(html.unescape(match[1]).split()) if match else ''


for path in [ROOT / 'README.md', ROOT / 'CONTRIBUTING.md', *sorted((ROOT / 'docs').glob('*.md'))]:
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
            date = row[date_col]
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

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f"OK: {counts['tables']} catalog tables, {counts['rows']} entries, "
      f"{len(records)} unique arXiv papers; local links, ordering, metadata, and resource columns checked.")
