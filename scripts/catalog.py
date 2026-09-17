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
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / 'data/papers.json'
DEFAULT_README = ROOT / 'README.md'
START = '<!-- catalog:start -->'
END = '<!-- catalog:end -->'
SECTION = re.compile(r'^<!-- section:([a-z0-9-]+) -->$')
PAPER = re.compile(r'<!-- paper:([A-Za-z0-9_.:-]+) -->')
LINK = re.compile(r'(?<!!)\[([^\]]*)\]\((https?://[^\s)]+)\)')
IMAGE = re.compile(r'!\[([^\]]*)\]\((https?://[^\s)]+)\)')
HEADER = '| **Paper** | **Resources** | **Input modalities** | **Time** | **Venue** |'
BENCHMARK_HEADER = '| **Name** | **Paper** | **Link** | **Task** | **Time** | **Venue** |'
BENCHMARK_TASKS = {'language': ('AEC6DF', 'Reasoning by language models, including multimodal LMs'),
                   'vision': ('C3E6CB', 'Reasoning by visual generation models')}
LINKED_IMAGE = re.compile(r'\[!\[([^\]]*)\]\((https?://[^\s)]+)\)\]\((https?://[^\s)]+)\)')
KINDS = {'code', 'data', 'project', 'weights', 'paper', 'other'}
MODALITY_IMAGE = re.compile(r'!\[([^\]]+)\]\[mod-([a-z0-9-]+)\]')
RESOURCE_LINK = re.compile(r'\[!\[([^\]]+)\]\[(res-[a-z0-9-]+)\]\]\((https?://[^\s)]+)\)')
REFERENCE = re.compile(r'^\[([^\]]+)\]: (https?://\S+)$', re.M)
# Platform and purpose are independent: a Hugging Face dataset is not a checkpoint.
RESOURCE_STYLES = {
    'github': ('181717', 'github', dict.fromkeys(sorted(KINDS), 'GitHub')),
    'hf': ('9C276A', 'huggingface', {'code': 'Code', 'weights': 'Checkpoints', 'data': 'Datasets',
                                  'project': 'Project', 'paper': 'Paper', 'other': 'Resources'}),
    'modelscope': ('624AFF', None, {'code': 'Code', 'weights': 'Checkpoints', 'data': 'Datasets',
                                  'project': 'Project', 'paper': 'Paper', 'other': 'Resources'}),
    'arxiv': ('b31b1b', 'arxiv', {'paper': 'arXiv'}),
}


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
    modalities = data['modalities']
    labels, colors = set(), set()
    tasks = {'language', 'vision', 'streaming', 'grounding', 'reasoning', 'qa', 'planning', 'generation', 'spatial'}
    for key, info in modalities.items():
        if not re.fullmatch(r'[a-z0-9-]+', key) or key in tasks or info['label'].lower() in tasks:
            raise CatalogError(f'input modality required, not a task/representation label: {key}')
        if not re.fullmatch(r'[A-Za-z0-9]+(?: [A-Za-z0-9]+)*', info['label']) or info['label'] in labels:
            raise CatalogError(f'invalid/duplicate modality label: {key}')
        if not re.fullmatch(r'[0-9A-F]{6}', info['color']) or info['color'] in colors:
            raise CatalogError(f'modality colors must be distinct uppercase hex values: {key}')
        if not isinstance(info['description'], str) or not info['description'].strip():
            raise CatalogError(f'modality description required: {key}')
        labels.add(info['label'])
        colors.add(info['color'])
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
        if section.get('table', 'papers') not in {'papers', 'benchmark'}:
            raise CatalogError(f'unknown table layout in {key}')
        if section['group'] not in groups:
            raise CatalogError(f'unknown group in section {key}')
    urls = set()
    for identity, paper in papers.items():
        if not re.fullmatch(r'[A-Za-z0-9_.:-]+', identity):
            raise CatalogError(f'invalid paper ID: {identity}')
        for field in ['title', 'venue']:
            if not isinstance(paper[field], str) or not paper[field].strip() or '\n' in paper[field]:
                raise CatalogError(f'{identity}: {field} must be a nonempty single line')
        if re.search(r'[`|<>]|&(?:#\d+|\w+);', paper['venue']):
            raise CatalogError(f'{identity}: venue must be plain text without Markdown/HTML delimiters')
        inputs = paper['input_modalities']
        if not isinstance(inputs, list) or any(not isinstance(m, str) or m not in modalities for m in inputs) or len(inputs) != len(set(inputs)):
            raise CatalogError(f'{identity}: input_modalities must contain unique registered modality IDs')
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
                if badge['url'].startswith('https://img.shields.io/github/stars/'):
                    raise CatalogError(f'{identity}: GitHub Stars are generated; omit stored star badges')
        seen = set()
        if not paper['placements']:
            raise CatalogError(f'{identity}: at least one placement is required')
        for placement in paper['placements']:
            section = placement['section']
            if section not in sections or section in seen:
                raise CatalogError(f'{identity}: unknown/duplicate section {section}')
            seen.add(section)
            if sections[section].get('table') == 'benchmark':
                tasks = placement.get('tasks')
                if not isinstance(tasks, list) or any(not isinstance(t, str) or t not in BENCHMARK_TASKS for t in tasks) or len(tasks) != len(set(tasks)):
                    raise CatalogError(f'{identity}: benchmark tasks must be unique language/vision values')
            if not isinstance(placement.get('name', ''), str) or '\n' in placement.get('name', ''):
                raise CatalogError(f'{identity}: name must be a single line')
            if not isinstance(placement.get('focus', ''), str) or '\n' in placement.get('focus', ''):
                raise CatalogError(f'{identity}: focus must be a single line')
            if 'badges' in placement:
                raise CatalogError(f'{identity}: use paper input_modalities; placement badges mix tasks with inputs')


def text_cell(value):
    text = html.escape(value, quote=False)
    for char in '|[]*_`~':
        text = text.replace(char, f'&#{ord(char)};')
    return text


def modality_cell(identity, info):
    return f'![{info["label"]}][mod-{identity}]'


def resource_style(resource):
    host = (urlsplit(resource['url']).hostname or '').removeprefix('www.')
    platform = {'github.com': 'github', 'huggingface.co': 'hf', 'hf.co': 'hf',
                'modelscope.cn': 'modelscope', 'modelscope.ai': 'modelscope', 'arxiv.org': 'arxiv'}.get(host)
    if platform and resource['kind'] in RESOURCE_STYLES[platform][2]:
        return f'res-{platform}-{resource["kind"]}'
    if resource['kind'] == 'project':
        return 'res-project'
    return None


def github_repo(url):
    parsed = urlsplit(url)
    if parsed.hostname not in {'github.com', 'www.github.com'}:
        return None
    parts = parsed.path.strip('/').split('/')
    if len(parts) < 2 or not all(re.fullmatch(r'[A-Za-z0-9_.-]+', p) for p in parts[:2]):
        return None
    return '/'.join([parts[0], parts[1].removesuffix('.git')])


def stars_cell(url):
    repo = github_repo(url)
    if not repo:
        return ''
    return (f'[![Stars](https://img.shields.io/github/stars/{repo}?style=flat-square&color=E0E0E0&label=Stars)]'
            f'(https://github.com/{repo}/stargazers)')


def badge_references(data):
    refs = {f'mod-{key}': f'https://img.shields.io/badge/{quote(info["label"], safe="")}-{info["color"]}?style=flat-square'
            for key, info in data['modalities'].items()}
    refs.update({f'task-{key}': f'https://img.shields.io/badge/{key}-{info[0]}?style=flat-square'
                 for key, info in BENCHMARK_TASKS.items()})
    refs['res-project'] = 'https://img.shields.io/badge/%F0%9F%8F%A0-Project_Page-527A9B?style=flat-square'
    for platform, (color, logo, purposes) in RESOURCE_STYLES.items():
        for kind, label in purposes.items():
            caption = f'ModelScope-{label}' if platform == 'modelscope' else label
            refs[f'res-{platform}-{kind}'] = (f'https://img.shields.io/badge/{caption}-{color}?style=flat-square'
                                            + (f'&logo={logo}' + ('&logoColor=white' if platform == 'github' else '') if logo else ''))
    return refs


def badge_cell(badge):
    return f'![{text_cell(badge["alt"])}]({badge["url"]})'


def resources_cell(resources):
    parts = []
    for resource in resources:
        label = f'{resource["kind"]}: {resource["label"]}'
        style = resource_style(resource)
        link_label = f'![resource:{resource["kind"]}][{style}]' if style else text_cell(label)
        part = f'[{link_label}]({resource["url"]})'
        stars = stars_cell(resource['url'])
        if stars:
            part += ' ' + stars
        badges = ' '.join(badge_cell(badge) for badge in resource.get('badges', []))
        parts.append(part + (' ' + badges if badges else ''))
    return '<br>'.join(parts) or '`N/A`'


def row(identity, paper, placement, modalities, benchmark=False):
    name = placement.get('name', '')
    title = (f'**{text_cell(name)}** · ' if name else '') + f'[{text_cell(paper["title"])}]({paper["url"]})'
    title += f' <!-- paper:{identity} -->'
    inputs = ' '.join(modality_cell(key, modalities[key]) for key in paper['input_modalities'])
    month = paper['date'][:7] + (' (proc.)' if paper['date_basis'] == 'proceedings' else '')
    if benchmark:
        title = f'[{text_cell(paper["title"])}]({paper["url"]}) <!-- paper:{identity} -->'
        tasks = ' '.join(f'![{t}][task-{t}]' for t in placement['tasks']) or '`N/A`'
        return f'| {text_cell(name) if name else "`N/A`"} | {title} | {resources_cell(paper["resources"])} | {tasks} | {month} | `{paper["venue"]}` |'
    return f'| {title} | {resources_cell(paper["resources"])} | {inputs or "`N/A`"} | {month} | `{paper["venue"]}` |'


def render_block(data):
    validate(data)
    lines = [START, '<!-- Generated from data/papers.json by scripts/catalog.py. -->', '',
             '`Time` is the first-public month; `(proc.)` marks a proceedings date with an unresolved earlier preprint. '
             '`N/A` means unrecorded or not applicable.', '',
             '<details open>', '<summary><strong>Input modalities & benchmark tasks</strong></summary>', '',
             'Badges describe supplied inputs, including optional conditioning. They exclude outputs, internal representations, '
             'and task names. Lists cover verified inputs and may be incomplete.', '',
             '| Modality | Input | Color |', '| :--- | :--- | :--- |']
    for key, info in data['modalities'].items():
        lines.append(f'| {modality_cell(key, info)} | {text_cell(info["description"])} | `#{info["color"]}` |')
    lines += ['', 'Benchmark **Task** identifies the evaluated model family, not its input modality. '
              'Both badges indicate evaluation of both families; `N/A` means unspecified or outside these families.', '',
              '| Task | Evaluated reasoning | Color |', '| :--- | :--- | :--- |']
    for task, (color, description) in BENCHMARK_TASKS.items():
        lines.append(f'| ![{task}][task-{task}] | {description} | `#{color}` |')
    lines += ['', '</details>', '']
    for group, info in data['groups'].items():
        lines += ['', f'<a id="{info["anchor"]}"></a>', '', f'### {info["title"]}', '']
        for section, config in data['sections'].items():
            if config['group'] != group:
                continue
            items = [(identity, paper, place) for identity, paper in data['papers'].items()
                     for place in paper['placements'] if place['section'] == section]
            benchmark = config.get('table') == 'benchmark'
            lines += ['', f'<a id="{config["anchor"]}"></a>', '', '<details open>',
                      f'<summary><strong>{html.escape(config["title"])}</strong></summary>', '',
                      config['description'], '', f'<!-- section:{section} -->', BENCHMARK_HEADER if benchmark else HEADER,
                      '| ' + ' :--- |' * (6 if benchmark else 5)]
            items.sort(key=lambda item: (item[1]['date'], item[0]), reverse=True)
            lines.extend(row(*item, data['modalities'], benchmark=benchmark) for item in items)
            lines += ['', '</details>', '']
    lines += [f'[{key}]: {url}' for key, url in badge_references(data).items()]
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


def parse_resources(cell, references, base_resources=()):
    if cell == '`N/A`':
        return []
    result = []
    for part in cell.split('<br>'):
        # Stars are derived from the repository URL, not a second resource.
        stars = LINKED_IMAGE.search(part)
        if stars:
            primary = RESOURCE_LINK.match(part) or LINK.match(part)
            primary_url = primary.groups()[-1] if primary else ''
            if stars[0] != stars_cell(primary_url):
                raise CatalogError('Stars badge must link to the resource repository stargazers')
            part = part[:stars.start()] + part[stars.end():]
        decorated = RESOURCE_LINK.match(part)
        if decorated:
            alt, style, url = decorated.groups()
            if not alt.startswith('resource:'):
                raise CatalogError('resource badge alt must be resource:kind')
            kind = alt.removeprefix('resource:')
            if style != resource_style({'kind': kind, 'url': url}) or style not in references:
                raise CatalogError('resource badge must match its platform and purpose')
            old = next((r for r in base_resources if (r['kind'], r['url']) == (kind, url)), None)
            label = old['label'] if old else ('GitHub' if github_repo(url) else kind.title())
            part = f'[{text_cell(kind + ": " + label)}]({url})' + part[decorated.end():]
        badges, text = parse_badges(part)
        match = LINK.fullmatch(text)
        if not match or ': ' not in html.unescape(match[1]):
            raise CatalogError('resource must be [kind: label](URL), optionally followed by badges')
        kind, label = html.unescape(match[1]).split(': ', 1)
        result.append({'kind': kind, 'label': label, 'url': match[2], 'badges': badges})
    return result


def parse_modalities(cell, data):
    if cell == '`N/A`':
        return []
    matches = MODALITY_IMAGE.findall(cell)
    if not matches or MODALITY_IMAGE.sub('', cell).strip():
        raise CatalogError('Input modalities accepts registered badges only; tasks belong in JSON focus')
    result = []
    for label, identity in matches:
        if identity not in data['modalities'] or label != data['modalities'][identity]['label'] or identity in result:
            raise CatalogError(f'unknown, mislabeled, or duplicate input modality: {identity}')
        result.append(identity)
    return result


def set_field(record, field, value, default=None):
    if record.get(field, default) != value:
        record[field] = value


def import_readme(source, base, allow_removals=False):
    """Import visible fields; preserve finer dates, provenance, and extra fields from base."""
    validate(base)
    _, block, _ = split_readme(source)
    definitions = REFERENCE.findall(block)
    references = dict(definitions)
    if len(references) != len(definitions) or references != badge_references(base):
        raise CatalogError('badge definitions must match the central registry; edit JSON for modality/color changes')
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
        if not line.startswith('|') or not section or line in {HEADER, BENCHMARK_HEADER} or re.fullmatch(r'\|[ :|\-]+', line):
            continue
        cells = [part.strip() for part in re.split(r'(?<!\\)\|', line)[1:-1]]
        ids = PAPER.findall(line)
        benchmark = base['sections'][section].get('table') == 'benchmark'
        if len(cells) != (6 if benchmark else 5) or len(ids) != 1:
            raise CatalogError(f'{section}: unexpected cells or missing paper ID marker')
        benchmark_name = ''
        tasks = []
        if benchmark:
            benchmark_name = html.unescape(cells.pop(0))
            benchmark_name = '' if benchmark_name == '`N/A`' else benchmark_name
            tasks = re.findall(r'!\[(language|vision)\]\[task-\1\]', cells[2])
            remaining = re.sub(r'!\[(language|vision)\]\[task-\1\]', '', cells[2]).strip()
            if (remaining and remaining != '`N/A`') or (tasks and remaining) or len(tasks) != len(set(tasks)):
                raise CatalogError('benchmark Task accepts only language/vision badges or N/A')
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
        name = benchmark_name if benchmark else (html.unescape(prefix[2:-4]) if prefix else '')
        if benchmark and prefix:
            raise CatalogError('benchmark names belong in the Name column')
        month = re.fullmatch(r'(\d{4}-\d{2})( \(proc\.\))?', cells[3])
        if not month:
            raise CatalogError(f'{identity}: Time must be YYYY-MM, optionally followed by (proc.)')
        venue = re.fullmatch(r'`([^`]+)`', cells[4])
        if not venue:
            raise CatalogError(f'{identity}: Venue must be wrapped in backticks')
        record = {'title': html.unescape(title[1]), 'url': title[2], 'date': month[1],
                  'date_basis': 'proceedings' if month[2] else 'first-public',
                  'venue': venue[1], 'resources': parse_resources(cells[1], references, base['papers'].get(identity, {}).get('resources', []))}
        if not benchmark:
            record['input_modalities'] = parse_modalities(cells[2], base)
        if identity in found and any(found[identity][k] != record[k] for k in found[identity].keys() & record.keys()):
            raise CatalogError(f'{identity}: conflicting cross-list fields; edit JSON or all copies consistently')
        found.setdefault(identity, {}).update(record)
        key = (identity, section)
        if key in placements:
            raise CatalogError(f'{identity}: duplicate row in {section}')
        placements[key] = {'section': section, 'name': name}
        if benchmark:
            placements[key]['tasks'] = tasks
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
        record['input_modalities'] = visible.get('input_modalities', record.get('input_modalities', []))
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
