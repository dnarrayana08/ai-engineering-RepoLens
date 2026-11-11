"""RepoLens Topic 3: a read-only, standard-library documentation pipeline.

Public source text is untrusted data. No source directives, code blocks, links or
repository instructions are executed. This prepares data, not embeddings or Q&A.
"""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse
import argparse
import bisect
import hashlib
import json
import platform
import re
import statistics
import urllib.request

PIPELINE_VERSION = 'repolens-week3-v1'
SUPPORTED = {'.md', '.rst', '.txt'}
CONFIG = {'target_characters': 500, 'overlap': 0,
          'cleaning': 'UTF-8 strict; normalize CRLF/CR to LF; preserve indentation, links and directives as inert text',
          'paragraph_policy': 'Do not split atomic paragraphs or fenced blocks; 500 characters is a soft target'}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def sha256_file(path):
    return sha256_bytes(Path(path).read_bytes())


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf-8')


def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding='utf-8').splitlines() if line.strip()]


def validate_manifest(manifest):
    sources = manifest.get('documents', [])
    if len(sources) != 8 or len({s['id'] for s in sources}) != 8:
        raise ValueError('Expected exactly eight unique approved source records')
    repositories = {r['repository']: r for r in manifest['repositories']}
    if set(repositories) != {'fastapi/fastapi', 'streamlit/streamlit', 'scikit-learn/scikit-learn'}:
        raise ValueError('Unexpected repository allowlist')
    for source in sources:
        repo = source['repository']
        if repo not in repositories or not re.fullmatch(r'[0-9a-f]{40}', source['commit']):
            raise ValueError('Unapproved repository or unpinned commit')
        relative = Path(source['path'])
        if relative.is_absolute() or '..' in relative.parts or relative.suffix.lower() not in SUPPORTED:
            raise ValueError('Unsupported or unsafe source path')
        expected = f"https://raw.githubusercontent.com/{repo}/{source['commit']}/{source['path']}"
        if source['url'] != expected or urlparse(expected).hostname != 'raw.githubusercontent.com':
            raise ValueError('Source URL does not match approved identity')
        if not re.fullmatch(r'[0-9a-f]{64}', source['sha256_utf8']):
            raise ValueError('Missing expected source fingerprint')
        if source['commit'] != repositories[repo]['commit'] or source['license'] != repositories[repo]['license']:
            raise ValueError('Inconsistent source commit or license metadata')
    return sorted(sources, key=lambda s: int(s['id'][1:]))


def raw_path(base, source):
    return Path(base) / 'data' / 'raw' / source['repository'] / source['path']


def download_sources(base, manifest, offline=False):
    """Fetch only the eight allowlisted pinned files; verify before accepting."""
    sources = validate_manifest(manifest)
    report = []
    for source in sources:
        path = raw_path(base, source)
        if not path.exists():
            if offline:
                raise FileNotFoundError(f'Missing source: {path}')
            request = urllib.request.Request(source['url'], headers={'User-Agent': 'RepoLens-Topic3/1.0'})
            with urllib.request.urlopen(request, timeout=45) as response:
                if response.geturl() != source['url']:
                    raise ValueError('Unexpected source redirect; review before admitting')
                payload = response.read(5_000_001)
            if len(payload) > 5_000_000:
                raise ValueError('Source exceeds the V1 download limit')
            if sha256_bytes(payload) != source['sha256_utf8']:
                raise ValueError(f"Pinned source fingerprint mismatch: {source['id']}")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        if sha256_file(path) != source['sha256_utf8']:
            raise ValueError(f"Cached source fingerprint mismatch: {source['id']}")
        report.append({'id': source['id'], 'path': str(path.relative_to(base)),
                       'bytes': path.stat().st_size, 'sha256': sha256_file(path)})
    return report


def load_text(path):
    path = Path(path)
    if path.suffix.lower() not in SUPPORTED:
        raise ValueError(f'Unsupported input type: {path.suffix}')
    text = path.read_bytes().decode('utf-8', errors='strict')
    if '\x00' in text or not text.strip():
        raise ValueError(f'Empty or binary-like document: {path}')
    # Do not flatten whitespace: indentation matters in commands, lists and RST.
    return text.replace('\r\n', '\n').replace('\r', '\n')


def headings(text, suffix):
    lines = text.splitlines(keepends=True)
    found = []
    offset = 0
    fenced = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if suffix == '.md' and re.match(r'^(`{3,}|~{3,})', stripped):
            fenced = not fenced
        if not fenced:
            md = re.match(r'^#{1,6}\s+(.+?)\s*#*\s*$', stripped)
            if suffix == '.md' and md:
                found.append((offset, md.group(1)))
            elif suffix == '.rst' and i + 1 < len(lines) and stripped:
                underline = lines[i + 1].strip()
                if len(underline) >= len(stripped) and re.fullmatch(r'([=~^"`:+#*_-])\1{2,}', underline):
                    found.append((offset, stripped))
        offset += len(line)
    return found


def atomic_blocks(text, markdown_fences=True):
    """Return exact text spans; blank lines inside Markdown fences stay intact.

    RST is treated as inert text. Paragraphs/indented blocks are kept whole;
    this is not a full Markdown/RST parser or a semantic splitter.
    """
    lines = text.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    blocks = []
    start = None
    fence = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        marker = re.match(r'^(`{3,}|~{3,})', stripped) if markdown_fences else None
        if start is None and stripped:
            start = offsets[i]
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1]:
                fence = None
        if not stripped and fence is None and start is not None:
            end = offsets[i]
            if text[start:end].strip():
                blocks.append((start, end))
            start = None
    if fence is not None:
        raise ValueError('Unclosed Markdown fence; review extraction before preparing')
    if start is not None and text[start:].strip():
        blocks.append((start, len(text)))
    return blocks


def chunk_spans(text, method, size=500, markdown_fences=True):
    if size <= 0:
        raise ValueError('Chunk size must be positive')
    if method == 'fixed':
        return [(start, min(start + size, len(text))) for start in range(0, len(text), size)
                if text[start:start + size].strip()]
    if method != 'paragraph-aware':
        raise ValueError('Unknown chunk method')
    blocks = atomic_blocks(text, markdown_fences=markdown_fences)
    chunks = []
    current = None
    for start, end in blocks:
        if current is None:
            current = [start, end]
        elif end - current[0] <= size:
            current[1] = end
        else:
            chunks.append(tuple(current))
            current = [start, end]
    if current:
        chunks.append(tuple(current))
    return chunks


def fence_intervals(text, markdown_fences=True):
    if not markdown_fences:
        return []
    intervals = []
    start = None
    fence = None
    offset = 0
    for line in text.splitlines(keepends=True):
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            token = marker.group(1)
            if fence is None:
                start, fence = offset, (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1]:
                intervals.append((start, offset + len(line)))
                fence = None
        offset += len(line)
    return intervals


def source_inspection(base, manifest):
    reports = []
    for source in validate_manifest(manifest):
        path = raw_path(base, source)
        text = load_text(path)
        hs = headings(text, path.suffix.lower())
        reports.append({'id': source['id'], 'repository': source['repository'],
                        'relative_path': str(path.relative_to(base)), 'bytes': path.stat().st_size,
                        'characters': len(text), 'lines': len(text.splitlines()), 'heading_count': len(hs),
                        'fenced_blocks': len(fence_intervals(text, path.suffix.lower() == '.md')), 'non_ascii_characters': sum(ord(c) > 127 for c in text),
                        'source_sha256': sha256_file(path), 'preview': text[:420],
                        'headings_preview': [h[1] for h in hs[:6]],
                        'limitations': 'Source markup retained; linked assets/includes not fetched; RST directives never executed.'})
    return reports


def compare_methods(base, manifest, size=500):
    rows = []
    for source in validate_manifest(manifest):
        text = load_text(raw_path(base, source))
        fences = fence_intervals(text, Path(source['path']).suffix.lower() == '.md')
        for method in ['fixed', 'paragraph-aware']:
            spans = chunk_spans(text, method, size, markdown_fences=Path(source['path']).suffix.lower() == '.md')
            lengths = [end - start for start, end in spans]
            boundaries = [end for _, end in spans[:-1]]
            rows.append({'source_id': source['id'], 'method': method, 'chunk_count': len(spans),
                         'minimum_characters': min(lengths), 'maximum_characters': max(lengths),
                         'median_characters': statistics.median(lengths),
                         'oversize_chunks': sum(n > size for n in lengths),
                         'mid_line_boundaries': sum(0 < end < len(text) and text[end - 1] != '\n' and text[end] != '\n' for end in boundaries),
                         'boundaries_inside_fences': sum(any(a < end < b for a, b in fences) for end in boundaries),
                         'preview': text[spans[0][0]:spans[0][1]][:420]})
    totals = {}
    for method in ['fixed', 'paragraph-aware']:
        subset = [r for r in rows if r['method'] == method]
        totals[method] = {key: sum(r[key] for r in subset) for key in
                          ['chunk_count', 'oversize_chunks', 'mid_line_boundaries', 'boundaries_inside_fences']}
        totals[method]['maximum_characters'] = max(r['maximum_characters'] for r in subset)
    fixed, para = totals['fixed'], totals['paragraph-aware']
    selected = ('paragraph-aware' if (para['boundaries_inside_fences'], para['mid_line_boundaries']) <
                (fixed['boundaries_inside_fences'], fixed['mid_line_boundaries']) else 'fixed')
    return {'configuration': CONFIG, 'per_source': rows, 'totals': totals, 'selected_method': selected,
            'decision_rule': 'Prefer fewer boundaries inside fenced blocks, then fewer mid-line boundaries; otherwise retain simple fixed splitting.',
            'scope_of_result': 'Observable chunk-boundary comparison, not retrieval or answer-quality evaluation.'}


def make_records(base, manifest, method, size=500):
    records = []
    for source in validate_manifest(manifest):
        text = load_text(raw_path(base, source))
        spans = chunk_spans(text, method, size, markdown_fences=Path(source['path']).suffix.lower() == '.md')
        line_offsets = [0] + [m.end() for m in re.finditer('\n', text)]
        hs = headings(text, Path(source['path']).suffix.lower())
        for n, (start, end) in enumerate(spans, 1):
            active = [title for offset, title in hs if offset <= start]
            sections = ([active[-1]] if active else ['Document introduction']) + [title for offset, title in hs if start < offset < end]
            sections = list(dict.fromkeys(sections))
            content = text[start:end]
            records.append({'record_id': f"{source['id']}-{n:04d}", 'source_id': source['id'],
                            'text': content, 'repository': source['repository'], 'document_path': source['path'],
                            'commit': source['commit'], 'source_url': source['url'], 'browser_url': source['browser_url'],
                            'source_sha256': sha256_file(raw_path(base, source)), 'license': source['license'],
                            'sections': sections, 'line_start': bisect.bisect_right(line_offsets, start),
                            'line_end': bisect.bisect_right(line_offsets, max(start, end - 1)),
                            'char_start': start, 'char_end': end, 'page': None,
                            'processing': {'method': method, 'target_characters': size, 'overlap': 0,
                                           'atomic_block_soft_limit': method == 'paragraph-aware'},
                            'text_sha256': sha256_bytes(content.encode('utf-8'))})
    return records


def validate_records(records, base, manifest):
    if not records:
        raise ValueError('No prepared records')
    sources = {s['id']: s for s in validate_manifest(manifest)}
    ids = set()
    by_source = {id: [] for id in sources}
    texts = {id: load_text(raw_path(base, s)) for id, s in sources.items()}
    for record in records:
        id = record['source_id']
        if id not in sources or record['record_id'] in ids or not record['text'].strip():
            raise ValueError('Invalid identity, duplicate ID or empty text')
        ids.add(record['record_id'])
        source = sources[id]
        for key in ['repository', 'commit', 'license']:
            if record[key] != source[key]:
                raise ValueError(f'Wrong {key} for {id}')
        if record['document_path'] != source['path'] or record['source_url'] != source['url'] or record['source_sha256'] != source['sha256_utf8']:
            raise ValueError('Invalid source provenance')
        if record['text'] != texts[id][record['char_start']:record['char_end']]:
            raise ValueError('Prepared text is not an exact source span')
        if record['text_sha256'] != sha256_bytes(record['text'].encode('utf-8')):
            raise ValueError('Prepared text hash mismatch')
        if not record['sections'] or record['line_start'] < 1 or record['line_end'] < record['line_start']:
            raise ValueError('Missing section/line provenance')
        by_source[id].append(record)
    # Every non-whitespace source character must survive. Whitespace-only gaps are allowed.
    for id, rows in by_source.items():
        if not rows:
            raise ValueError(f'No records for {id}')
        rows.sort(key=lambda x: x['char_start'])
        previous = 0
        for row in rows:
            if row['char_start'] < previous or texts[id][previous:row['char_start']].strip():
                raise ValueError('Overlapping chunks or non-whitespace data loss')
            previous = row['char_end']
        if texts[id][previous:].strip():
            raise ValueError('Source tail lost')
    return {'status': 'PASS', 'record_count': len(records), 'source_count': len(by_source),
            'unique_record_ids': len(ids), 'non_whitespace_content_preserved': True,
            'exact_source_spans': True, 'provenance_verified': True}


def export_records(path, records):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + '\n')
    exported = read_jsonl(path)
    if exported != records or not path.stat().st_size:
        raise ValueError('Export round-trip failed')


def lineage_records(base, manifest, records, output, method):
    rows = []
    for source in validate_manifest(manifest):
        selected = [r['record_id'] for r in records if r['source_id'] == source['id']]
        rows.append({'source_id': source['id'], 'source_filename': str(raw_path(base, source).relative_to(base)),
                     'source_url': source['url'], 'source_sha256': sha256_file(raw_path(base, source)),
                     'source_version': source['commit'], 'repository': source['repository'],
                     'access_rights': source['license'] + '; retained notices in data/third_party; linked assets excluded',
                     'prepared_output': str(Path(output).relative_to(base)), 'prepared_sha256': sha256_file(output),
                     'record_count': len(selected), 'first_record_id': selected[0], 'last_record_id': selected[-1],
                     'processing_note': method + '; ' + CONFIG['cleaning'],
                     'known_limitations': 'Simple text/heading handling; no execution, include expansion, semantic retrieval or answer evaluation.'})
    return rows


def run_part_b(base, manifest):
    base = Path(base)
    comparison = compare_methods(base, manifest)
    selected = comparison['selected_method']
    records = make_records(base, manifest, selected)
    validation = validate_records(records, base, manifest)
    output = base / 'data/processed/prepared_text.jsonl'
    export_records(output, records)
    write_json(base / 'data/processed/chunking_comparison.json', comparison)
    write_json(base / 'data/processed/inspection.json', source_inspection(base, manifest))
    write_json(base / 'data/week3_manifest.json', {
        'pipeline_version': PIPELINE_VERSION, 'generated_at_utc': utc_now(),
        'purpose': 'Part B preparation lineage; all eight sources map into one combined JSONL with stable source IDs',
        'configuration': {**CONFIG, 'method': selected},
        'records': lineage_records(base, manifest, records, output, selected), 'validation': validation})
    print(f'PART B PASS | sources={validation["source_count"]} | chunks={len(records)} | method={selected}')
    return comparison, validation


def execute_pipeline(base, manifest, configuration, implementation_sha256):
    base = Path(base)
    if not re.fullmatch('[0-9a-f]{64}', implementation_sha256):
        raise ValueError('Record the actual implementation SHA-256')
    # Recheck raw bytes at ingestion, including offline reruns; never silently refresh.
    ingestion = download_sources(base, manifest, offline=True)
    inspection = source_inspection(base, manifest)
    records = make_records(base, manifest, configuration['method'], configuration['target_characters'])
    validation = validate_records(records, base, manifest)
    output = base / 'data/pipeline_v1/documents/prepared_text.jsonl'
    export_records(output, records)
    validation.update({'output_count': 1, 'output_bytes': output.stat().st_size,
                       'output_sha256': sha256_file(output)})
    run = {'pipeline_version': PIPELINE_VERSION, 'generated_at_utc': utc_now(),
           'execution_environment': {'python': platform.python_version(), 'system': platform.system(),
                                     'colab': 'google.colab' in __import__('sys').modules},
           'implementation_sha256': implementation_sha256, 'data_type': 'documents',
           'configuration': configuration, 'sources': ingestion, 'inspection': inspection,
           'outputs': [str(output.relative_to(base))],
           'source_output_mapping': lineage_records(base, manifest, records, output, configuration['method']),
           'validation': validation}
    write_json(output.parent / 'pipeline_manifest.json', run)
    print(f'SUCCESS: documents | Inputs: {len(ingestion)} | Records: {len(records)} | Outputs: 1')
    return run


def repeatability_check(base, manifest, configuration, implementation_sha256):
    first = execute_pipeline(base, manifest, configuration, implementation_sha256)
    second = execute_pipeline(base, manifest, configuration, implementation_sha256)
    keys = ['sources', 'configuration', 'validation', 'source_output_mapping', 'implementation_sha256']
    for key in keys:
        if first[key] != second[key]:
            raise AssertionError(f'Repeatability failure: {key}')
    part_b = Path(base) / 'data/processed/prepared_text.jsonl'
    part_c = Path(base) / second['outputs'][0]
    if part_b.read_bytes() != part_c.read_bytes():
        raise AssertionError('Part B and C outputs differ')
    report = {'status': 'PASS', 'checks': keys, 'run_count': 2,
              'first_generated_at_utc': first['generated_at_utc'], 'second_generated_at_utc': second['generated_at_utc'],
              'part_b_matches_part_c': True, 'prepared_sha256': sha256_file(part_c),
              'sources': len(second['sources']), 'records': second['validation']['record_count'],
              'environment': second['execution_environment'],
              'limitation': 'Same-environment repeatability smoke check; not cross-environment reproducibility or answer-quality proof.'}
    write_json(part_c.parent / 'repeatability_report.json', report)
    print('PASS: source fingerprints, prepared bytes, counts, mappings and configuration match; Part B equals Part C.')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--offline', action='store_true')
    args = parser.parse_args()
    base = args.base.resolve()
    manifest = json.loads((base / 'data/source_manifest.json').read_text(encoding='utf-8'))
    download_sources(base, manifest, offline=args.offline)
    comparison, _ = run_part_b(base, manifest)
    repeatability_check(base, manifest, {**CONFIG, 'method': comparison['selected_method']}, sha256_file(__file__))


if __name__ == '__main__':
    main()
