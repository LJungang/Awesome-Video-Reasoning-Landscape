"""Behavioral checks for conversion and contributor updates; no network calls."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import catalog


def fixture():
    return {
        'schema_version': 1,
        'groups': {'engines': {'title': 'Engines', 'anchor': 'engines'}},
        'sections': {
            'language': {'group': 'engines', 'title': 'Language', 'anchor': 'language', 'description': 'Words.'},
            'visual': {'group': 'engines', 'title': 'Visual', 'anchor': 'visual', 'description': 'Frames.'},
        },
        'papers': {'2601.00001': {
            'title': 'A [test] | B & C_*', 'url': 'https://arxiv.org/abs/2601.00001',
            'date': '2026-01-02T12:34:56Z', 'date_basis': 'first-public', 'venue': 'arXiv',
            'resources': [{'kind': 'code', 'label': 'Code [A] | B', 'url': 'https://example.org/code?a=1&b=2',
                           'badges': [{'alt': 'Stars', 'url': 'https://example.org/badge.svg'}],
                           'evidence': {'checked_on': '2026-01-03', 'source': 'author'}}],
            'placements': [{'section': 'language', 'focus': '**Grounding** | visual evidence', 'name': 'A [bench]',
                            'badges': [{'alt': 'Video', 'url': 'https://example.org/video.svg'}]},
                           {'section': 'visual', 'focus': 'Visual bridge'}],
            'provenance': {'bibtex': '@article{x, title={A {Protected} Title}}', 'private_note': {'depth': 'abstract'}},
        }},
    }


def readme(data):
    shell = '# Survey\n\n```math\na=b\n```\n\n' + catalog.START + '\n' + catalog.END + '\n\nHuman-written notes.\n'
    return catalog.render_readme(data, shell)


class CatalogTests(unittest.TestCase):
    def test_round_trip_preserves_precision_provenance_badges_and_special_text(self):
        data = fixture()
        self.assertEqual(catalog.import_readme(readme(data), data), data)

    def test_new_json_paper_updates_tables_without_changing_narrative(self):
        data = fixture()
        before = readme(data)
        new = copy.deepcopy(data['papers']['2601.00001'])
        new.update(title='A newer paper', url='https://arxiv.org/abs/2602.00002', date='2026-02-01',
                   placements=[{'section': 'visual', 'focus': 'New work'}])
        data['papers']['2602.00002'] = new
        after = catalog.render_readme(data, before)
        self.assertEqual(catalog.split_readme(before)[::2], catalog.split_readme(after)[::2])
        self.assertIn('2 papers · 3 catalog rows', after)
        visual = after.split('<!-- section:visual -->')[1]
        self.assertLess(visual.index('paper:2602.00002'), visual.index('paper:2601.00001'))
        self.assertEqual(catalog.import_readme(after, data), data)

    def test_section_anchors_cannot_be_consumed_as_gfm_table_rows(self):
        data = fixture()
        source = readme(data)
        for section in data['sections'].values():
            before, _ = source.split(f'<a id="{section["anchor"]}"></a>')
            self.assertTrue(before.endswith('\n\n'), 'GFM needs a blank line between a table and the next anchor')

    def test_readme_edits_update_shared_fields_and_preserve_evidence(self):
        data = fixture()
        source = readme(data).replace(catalog.text_cell(data['papers']['2601.00001']['title']), 'New title')
        source = source.replace('**Grounding** &#124; visual evidence', 'Updated scope')
        result = catalog.import_readme(source, data)
        paper = result['papers']['2601.00001']
        self.assertEqual(paper['title'], 'New title')
        self.assertEqual(paper['placements'][0]['focus'], 'Updated scope')
        self.assertEqual(paper['provenance'], data['papers']['2601.00001']['provenance'])
        self.assertEqual(paper['date'], '2026-01-02T12:34:56Z')
        self.assertEqual(paper['resources'], data['papers']['2601.00001']['resources'])

    def test_conflicting_cross_list_rejected(self):
        data = fixture()
        source = readme(data).replace(catalog.text_cell(data['papers']['2601.00001']['title']), 'Only one copy changed', 1)
        with self.assertRaisesRegex(catalog.CatalogError, 'conflicting cross-list'):
            catalog.import_readme(source, data)

    def test_truncation_and_unexpected_removal_rejected(self):
        data = fixture()
        source = readme(data)
        with self.assertRaises(catalog.CatalogError):
            catalog.import_readme(source.split(catalog.END)[0], data)
        removed = '\n'.join(line for line in source.splitlines() if 'paper:2601.00001' not in line)
        with self.assertRaisesRegex(catalog.CatalogError, 'disappeared'):
            catalog.import_readme(removed, data)
        result = catalog.import_readme(removed, data, allow_removals=True)
        self.assertEqual(result['papers'], {})

    def test_date_edits_do_not_invent_day_or_mislabel_proceedings(self):
        data = fixture()
        result = catalog.import_readme(readme(data).replace('| 2026-01 |', '| 2026-02 (proc.) |'), data)
        paper = result['papers']['2601.00001']
        self.assertEqual((paper['date'], paper['date_basis']), ('2026-02', 'proceedings'))

    def test_new_readme_row_imported(self):
        base = fixture()
        expanded = copy.deepcopy(base)
        new = copy.deepcopy(base['papers']['2601.00001'])
        new.update(title='New source', url='https://example.org/new-paper', date='2026-02', date_basis='proceedings')
        new['placements'] = [{'section': 'language', 'focus': 'Proceedings source'}]
        expanded['papers']['paper:new'] = new
        result = catalog.import_readme(readme(expanded), base)
        self.assertEqual(result['papers']['paper:new']['title'], 'New source')
        self.assertEqual(result['papers']['paper:new']['date_basis'], 'proceedings')
        self.assertNotIn('provenance', result['papers']['paper:new'])

    def test_duplicate_json_keys_and_dataset_weights_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'duplicate.json'
            path.write_text('{"papers": {}, "papers": {}}')
            with self.assertRaisesRegex(catalog.CatalogError, 'duplicate JSON key'):
                catalog.load(path)
        data = fixture()
        data['papers']['2601.00001']['resources'] = [
            {'kind': 'weights', 'label': 'Wrong', 'url': 'https://huggingface.co/datasets/example/data'}]
        with self.assertRaisesRegex(catalog.CatalogError, 'dataset'):
            catalog.validate(data)

    def test_failed_cli_import_does_not_overwrite_destination(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            catalog.save(root / 'papers.json', fixture())
            (root / 'README.md').write_text('# Truncated\n')
            target = root / 'output.json'
            target.write_text('preserve me')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/catalog.py'), 'import-readme',
                                     '--data', str(root / 'papers.json'), '--readme', str(root / 'README.md'),
                                     '--output', str(target)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(target.read_text(), 'preserve me')

    def test_entire_repository_catalog_round_trips(self):
        data = catalog.load(ROOT / 'data/papers.json')
        source = (ROOT / 'README.md').read_text()
        self.assertGreater(len(data['papers']), 1300)
        self.assertEqual(catalog.render_readme(data, source), source)
        self.assertEqual(catalog.import_readme(source, data), data)
        row_ids = catalog.PAPER.findall(catalog.split_readme(source)[1])
        self.assertEqual(set(row_ids), set(data['papers']))
        self.assertEqual(len(row_ids), sum(len(p['placements']) for p in data['papers'].values()))


if __name__ == '__main__':
    unittest.main()
