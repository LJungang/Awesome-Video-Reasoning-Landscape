#!/usr/bin/env python3
"""Convert the canonical paper JSON to/from managed README tables (Python 3.10+)."""
import argparse
import copy
import datetime as dt
import html
import json
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / 'data/papers.json'
DEFAULT_README = ROOT / 'README.md'
START = '<!-- catalog:start -->'
END = '<!-- catalog:end -->'
SECTION = re.compile(r'^<!-- section:([a-z0-9-]+) -->$')
PAPER = re.compile(r'<!-- paper:([A-Za-z0-9_.:-]+) -->')
LINK = re.compile(r'(?<!!)\[([^\]]*)\]\((https?://[^\s)]+)\)')
IMAGE = re.compile(r'!\[([^\]]*)\]\((https?://[^\s)]+)\)')
HEADER = '| **Paper** | **Resources** | **Focus / scope** | **Time** | **Venue** |'
KINDS = {'code', 'data', 'project', 'weights', 'paper', 'other'}


class CatalogError(ValueError):
    pass


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CatalogError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def load(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=unique_keys)


def atomic_write(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', dir=path.parent, encoding='utf-8', delete=False) as file:
        file.write(content)
        temporary = Path(file.name)
    temporary.chmod(path.stat().st_mode & 0o777 if path.exists() else 0o644)
    temporary.replace(path)


def save(path, data):
    atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def check_url(url):
    if not isinstance(url, str) or urlsplit(url).scheme not in {'http', 'https'} or not urlsplit(url).netloc or re.search(r'[\s<>|()]', url):
        raise CatalogError(f'use an absolute HTTP(S) URL; percent-encode spaces/parentheses: {url!r}')


def check_date(date):
    if not isinstance(date, str):
        raise CatalogError('date must be an ISO month, day, or timestamp')
    try:
        if re.fullmatch(r'\d{4}-\d{2}', date):
            dt.date.fromisoformat(date + '-01')
        elif re.fullmatch(r'\d{4}-\d{2}-\d{2}', date):
            dt.date.fromisoformat(date)
        elif re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', date):
            dt.datetime.fromisoformat(date.replace('Z', '+00:00'))
        else:
            raise ValueError(date)
    except ValueError as exc:
        raise CatalogError(f'invalid ISO date: {date}') from exc
    if date[:10] > dt.date.today().isoformat():
        raise CatalogError(f'future publication date: {date}')


def validate(data):
    if data.get('schema_version') != 1:
        raise CatalogError('schema_version must be 1')
    groups, sections, papers = data['groups'], data['sections'], data['papers']
    if set(groups) & set(sections):
        raise CatalogError('group and section IDs must be distinct')
    anchors = set()
    for key, item in {**groups, **sections}.items():
        if not re.fullmatch(r'[a-z0-9-]+', key):
            raise CatalogError(f'invalid group/section ID: {key}')
        if not re.fullmatch(r'[a-z0-9-]+', item['anchor']) or item['anchor'] in anchors:
            raise CatalogError(f'invalid or duplicate anchor: {item["anchor"]}')
        anchors.add(item['anchor'])
    for key, section in sections.items():
        if section['group'] not in groups:
            raise CatalogError(f'unknown group in section {key}')
    urls = set()
    for identity, paper in papers.items():
        if not re.fullmatch(r'[A-Za-z0-9_.:-]+', identity):
            raise CatalogError(f'invalid paper ID: {identity}')
        for field in ['title', 'venue']:
            if not isinstance(paper[field], str) or not paper[field].strip() or '\n' in paper[field]:
                raise CatalogError(f'{identity}: {field} must be a nonempty single line')
        check_url(paper['url'])
        if paper['url'] in urls:
            raise CatalogError(f'duplicate primary URL: {paper["url"]}')
        urls.add(paper['url'])
        arxiv = re.search(r'arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?(?:\.pdf)?$', paper['url'])
        if arxiv and identity != arxiv[1]:
            raise CatalogError(f'{identity}: arXiv papers must use the unversioned arXiv ID')
        check_date(paper['date'])
        if paper['date_basis'] not in {'first-public', 'proceedings'}:
            raise CatalogError(f'{identity}: invalid date_basis')
        resource_keys = set()
        for resource in paper['resources']:
            check_url(resource['url'])
            key = (resource['kind'], resource['url'])
            if resource['kind'] not in KINDS or key in resource_keys:
                raise CatalogError(f'{identity}: invalid/duplicate resource {key}')
            resource_keys.add(key)
            if not resource['label'] or '\n' in resource['label']:
                raise CatalogError(f'{identity}: resource label required')
            if resource['kind'] == 'weights' and '/datasets/' in resource['url']:
                raise CatalogError(f'{identity}: dataset is not a weights resource')
            for badge in resource.get('badges', []):
                check_url(badge['url'])
        seen = set()
        if not paper['placements']:
            raise CatalogError(f'{identity}: at least one placement is required')
        for placement in paper['placements']:
            section = placement['section']
            if section not in sections or section in seen:
                raise CatalogError(f'{identity}: unknown/duplicate section {section}')
            seen.add(section)
            if not isinstance(placement.get('focus', ''), str) or '\n' in placement.get('focus', ''):
                raise CatalogError(f'{identity}: focus must be a single line')
            for badge in placement.get('badges', []):
                check_url(badge['url'])


def text_cell(value):
    text = html.escape(value, quote=False)
    for char in '|[]*_`~':
        text = text.replace(char, f'&#{ord(char)};')
    return text


def focus_cell(value):
    # Focus supports inline Markdown. Pipes are entities so table splitting is unambiguous.
    return html.escape(value, quote=False).replace('|', '&#124;')


def badge_cell(badge):
    return f'![{text_cell(badge["alt"])}]({badge["url"]})'


def resources_cell(resources):
    parts = []
    for resource in resources:
        label = f'{resource["kind"]}: {resource["label"]}'
        part = f'[{text_cell(label)}]({resource["url"]})'
        badges = ' '.join(badge_cell(badge) for badge in resource.get('badges', []))
        parts.append(part + (' ' + badges if badges else ''))
    return '<br>'.join(parts) or '`N/A`'


def row(identity, paper, placement):
    name = placement.get('name', '')
    title = (f'**{text_cell(name)}** · ' if name else '') + f'[{text_cell(paper["title"])}]({paper["url"]})'
    title += f' <!-- paper:{identity} -->'
    focus = focus_cell(placement.get('focus', ''))
    badges = ' '.join(badge_cell(badge) for badge in placement.get('badges', []))
    if badges:
        focus += ('<br>' if focus else '') + badges
    month = paper['date'][:7] + (' (proc.)' if paper['date_basis'] == 'proceedings' else '')
    return f'| {title} | {resources_cell(paper["resources"])} | {focus or "`N/A`"} | {month} | {text_cell(paper["venue"])} |'


def render_block(data):
    validate(data)
    count = sum(len(paper['placements']) for paper in data['papers'].values())
    lines = [START, '<!-- Generated from data/papers.json by scripts/catalog.py. -->', '',
             f'**{len(data["papers"]):,} papers · {count:,} catalog rows.** Cross-listed rows share one paper ID. '
             '`Time` is the first-public month; `(proc.)` marks a proceedings date with an unresolved earlier preprint. '
             '`N/A` means no recorded resource or scope detail. [Contribute via JSON](CONTRIBUTING.md).', '',
             '| Chapter | Papers |', '| :--- | ---: |']
    for section, config in data['sections'].items():
        n = sum(any(p['section'] == section for p in paper['placements']) for paper in data['papers'].values())
        lines.append(f'| [{text_cell(config["title"])}](#{config["anchor"]}) | {n} |')
    for group, info in data['groups'].items():
        lines += ['', f'<a id="{info["anchor"]}"></a>', '', f'### {info["title"]}', '']
        for section, config in data['sections'].items():
            if config['group'] != group:
                continue
            lines += [f'<a id="{config["anchor"]}"></a>', '', f'#### {config["title"]}', '', config['description'], '',
                      f'<!-- section:{section} -->', HEADER, '| :--- | :--- | :--- | :--- | :--- |']
            items = [(identity, paper, place) for identity, paper in data['papers'].items()
                     for place in paper['placements'] if place['section'] == section]
            items.sort(key=lambda item: (item[1]['date'], item[0]), reverse=True)
            lines.extend(row(*item) for item in items)
    return '\n'.join(lines) + '\n\n' + END


def split_readme(source):
    if source.count(START) != 1 or source.count(END) != 1:
        raise CatalogError('README must contain exactly one catalog:start/catalog:end marker pair')
    if source.index(END) < source.index(START):
        raise CatalogError('catalog:end must follow catalog:start')
    before, rest = source.split(START)
    block, after = rest.split(END)
    return before, START + block + END, after


def render_readme(data, source):
    before, _, after = split_readme(source)
    return before + render_block(data) + after


def parse_badges(cell):
    badges = [{'alt': html.unescape(m[1]), 'url': m[2]} for m in IMAGE.finditer(cell)]
    return badges, IMAGE.sub('', cell).strip().removesuffix('<br>').strip()


def parse_resources(cell):
    if cell == '`N/A`':
        return []
    result = []
    for part in cell.split('<br>'):
        badges, text = parse_badges(part)
        match = LINK.fullmatch(text)
        if not match or ': ' not in html.unescape(match[1]):
            raise CatalogError('resource must be [kind: label](URL), optionally followed by badges')
        kind, label = html.unescape(match[1]).split(': ', 1)
        result.append({'kind': kind, 'label': label, 'url': match[2], 'badges': badges})
    return result


def set_field(record, field, value, default=None):
    if record.get(field, default) != value:
        record[field] = value


def import_readme(source, base, allow_removals=False):
    """Import visible fields; preserve finer dates, provenance, and extra fields from base."""
    validate(base)
    _, block, _ = split_readme(source)
    found, placements, sections = {}, {}, set()
    section = None
    for line in block.splitlines():
        match = SECTION.fullmatch(line)
        if match:
            section = match[1]
            if section not in base['sections'] or section in sections:
                raise CatalogError(f'unknown/duplicate section marker: {section}')
            sections.add(section)
            continue
        if not line.startswith('|') or not section or line == HEADER or re.fullmatch(r'\|[ :|\-]+', line):
            continue
        cells = [part.strip() for part in re.split(r'(?<!\\)\|', line)[1:-1]]
        ids = PAPER.findall(line)
        if len(cells) != 5 or len(ids) != 1:
            raise CatalogError(f'{section}: expected five cells and one paper ID marker')
        identity = ids[0]
        title_cell = PAPER.sub('', cells[0]).strip()
        title = LINK.search(title_cell)
        if not title or len(LINK.findall(title_cell)) != 1:
            raise CatalogError(f'{identity}: expected one primary paper link')
        prefix = title_cell[:title.start()].strip()
        if prefix and not re.fullmatch(r'\*\*.*\*\* ·', prefix):
            raise CatalogError(f'{identity}: invalid short-name prefix')
        if title_cell[title.end():].strip():
            raise CatalogError(f'{identity}: unexpected text after paper link')
        name = html.unescape(prefix[2:-4]) if prefix else ''
        month = re.fullmatch(r'(\d{4}-\d{2})( \(proc\.\))?', cells[3])
        if not month:
            raise CatalogError(f'{identity}: Time must be YYYY-MM, optionally followed by (proc.)')
        badges, focus = parse_badges(cells[2])
        focus = '' if focus == '`N/A`' else html.unescape(focus)
        record = {'title': html.unescape(title[1]), 'url': title[2], 'date': month[1],
                  'date_basis': 'proceedings' if month[2] else 'first-public',
                  'venue': html.unescape(cells[4]), 'resources': parse_resources(cells[1])}
        if identity in found and found[identity] != record:
            raise CatalogError(f'{identity}: conflicting cross-list fields; edit JSON or all copies consistently')
        found[identity] = record
        key = (identity, section)
        if key in placements:
            raise CatalogError(f'{identity}: duplicate row in {section}')
        placements[key] = {'section': section, 'name': name, 'focus': focus, 'badges': badges}
    if sections != set(base['sections']):
        raise CatalogError('missing section markers; refusing a partial README import')
    old_keys = {(key, p['section']) for key, paper in base['papers'].items() for p in paper['placements']}
    missing = old_keys - placements.keys()
    if missing and not allow_removals:
        raise CatalogError(f'{len(missing)} catalog rows disappeared; use --allow-removals only for intentional removals')
    result = copy.deepcopy(base)
    result['papers'] = {}
    for identity in [*base['papers'], *(key for key in found if key not in base['papers'])]:
        if identity not in found:
            continue
        record = copy.deepcopy(base['papers'].get(identity, {}))
        visible = found[identity]
        for field in ['title', 'url', 'venue', 'date_basis']:
            record[field] = visible[field]
        if record.get('date', '')[:7] != visible['date'] or base['papers'].get(identity, {}).get('date_basis') != visible['date_basis']:
            record['date'] = visible['date']
        old_resources = {(r['kind'], r['url']): r for r in record.get('resources', [])}
        record['resources'] = []
        for resource in visible['resources']:
            item = copy.deepcopy(old_resources.get((resource['kind'], resource['url']), {}))
            for field, value in resource.items():
                set_field(item, field, value, [] if field == 'badges' else None)
            record['resources'].append(item)
        old_places = {p['section']: p for p in record.get('placements', [])}
        order = [*old_places, *(s for s in base['sections'] if s not in old_places)]
        record['placements'] = []
        for section in order:
            if (identity, section) not in placements:
                continue
            item = copy.deepcopy(old_places.get(section, {'section': section}))
            for field, value in placements[(identity, section)].items():
                set_field(item, field, value, [] if field == 'badges' else '')
            record['placements'].append(item)
        result['papers'][identity] = record
    validate(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['render', 'import-readme', 'check'])
    parser.add_argument('--data', type=Path, default=DEFAULT_DATA, help='canonical JSON (also metadata base for import)')
    parser.add_argument('--readme', type=Path, default=DEFAULT_README)
    parser.add_argument('--output', type=Path, help='alternate destination; defaults to README for render, JSON for import')
    parser.add_argument('--allow-removals', action='store_true', help='permit intentional row/paper removal during import')
    args = parser.parse_args()
    try:
        data = load(args.data)
        source = args.readme.read_text()
        if args.command == 'render':
            atomic_write(args.output or args.readme, render_readme(data, source))
            print(f'Rendered {len(data["papers"]):,} papers into {args.output or args.readme}.')
        elif args.command == 'import-readme':
            result = import_readme(source, data, args.allow_removals)
            save(args.output or args.data, result)
            print(f'Imported {len(result["papers"]):,} papers; retained undisplayed metadata. Run render and check next.')
        else:
            if source != render_readme(data, source):
                raise CatalogError('README is stale; run scripts/catalog.py render (or import intentional table edits first)')
            if import_readme(source, data) != data:
                raise CatalogError('JSON → README → JSON round-trip changed data')
            print(f'OK: {len(data["papers"]):,} papers; README synchronized; lossless round-trip against canonical JSON.')
    except (CatalogError, KeyError, TypeError, OSError, json.JSONDecodeError) as exc:
        parser.exit(1, f'Catalog error: {exc}\n')


if __name__ == '__main__':
    main()
