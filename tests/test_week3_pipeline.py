"""Focused contracts for data loss, source confusion and repeatable exports."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import week3_pipeline as p


class TextPreparationTests(unittest.TestCase):
    def test_fenced_commands_are_not_split_or_reindented(self):
        text = '# Installation\n\n```python\ndef example():\n    return 42\n```\n\nNext paragraph.\n'
        spans = p.chunk_spans(text, 'paragraph-aware', 20)
        chunks = [text[a:b] for a, b in spans]
        self.assertTrue(any('def example():\n    return 42\n```' in c for c in chunks))
        self.assertEqual(0, sum(a < boundary < b for _, boundary in spans[:-1] for a, b in p.fence_intervals(text)))

    def test_rst_heading_underlines_are_not_markdown_fences(self):
        text = 'Title\n~~~~~\n\nDescription\n\nAnother heading\n~~~~~~~~~~~~~~~\n\nMore content\n'
        self.assertTrue(p.chunk_spans(text, 'paragraph-aware', 20, markdown_fences=False))
        self.assertEqual(['Title', 'Another heading'], [title for _, title in p.headings(text, '.rst')])

    def test_unclosed_markdown_fence_is_a_visible_failure(self):
        with self.assertRaisesRegex(ValueError, 'Unclosed'):
            p.atomic_blocks('```bash\npip install example\n')

    def test_unknown_method_or_nonpositive_size_stops(self):
        with self.assertRaises(ValueError):
            p.chunk_spans('text', 'semantic-magic')
        with self.assertRaises(ValueError):
            p.chunk_spans('text', 'fixed', 0)

    def test_whitespace_only_or_binary_input_stops(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'empty.md'
            for content in [' \n\t', 'abc\x00def']:
                target.write_text(content)
                with self.assertRaises(ValueError):
                    p.load_text(target)


class CorpusContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / 'data/source_manifest.json').read_text())

    def test_source_url_cannot_escape_the_fixed_allowlist(self):
        bad = copy.deepcopy(self.manifest)
        bad['documents'][0]['url'] = 'https://example.com/unreviewed.md'
        with self.assertRaisesRegex(ValueError, 'URL'):
            p.validate_manifest(bad)

    def test_cached_content_changes_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            target = p.raw_path(Path(directory), self.manifest['documents'][0])
            target.parent.mkdir(parents=True)
            target.write_text('tampered')
            with self.assertRaisesRegex(ValueError, 'fingerprint mismatch'):
                p.download_sources(Path(directory), self.manifest, offline=True)

    def test_missing_raw_input_stops_instead_of_exporting_partial_data(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                p.download_sources(Path(directory), self.manifest, offline=True)

    def test_duplicate_or_wrong_repository_record_fails(self):
        records = p.make_records(ROOT, self.manifest, 'paragraph-aware')
        bad = copy.deepcopy(records)
        bad.append(copy.deepcopy(bad[0]))
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            p.validate_records(bad, ROOT, self.manifest)
        records[0]['repository'] = 'other/project'
        with self.assertRaisesRegex(ValueError, 'repository'):
            p.validate_records(records, ROOT, self.manifest)

    def test_all_eight_sources_round_trip_without_content_loss(self):
        for method in ['fixed', 'paragraph-aware']:
            records = p.make_records(ROOT, self.manifest, method)
            result = p.validate_records(records, ROOT, self.manifest)
            self.assertEqual(8, result['source_count'])
            with tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / 'prepared.jsonl'
                p.export_records(output, records)
                first_hash = p.sha256_file(output)
                p.export_records(output, records)
                self.assertEqual(first_hash, p.sha256_file(output))
                self.assertEqual(records, p.read_jsonl(output))

    def test_selection_is_based_on_observed_boundaries(self):
        comparison = p.compare_methods(ROOT, self.manifest)
        self.assertEqual('paragraph-aware', comparison['selected_method'])
        self.assertEqual(0, comparison['totals']['paragraph-aware']['boundaries_inside_fences'])
        self.assertGreater(comparison['totals']['fixed']['boundaries_inside_fences'], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
