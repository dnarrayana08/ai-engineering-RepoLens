# RepoLens Week 3 Verification Record

Review date 11 November 2026. **Local and Google Colab executions completed. Course portal submission remains outstanding.**

## Required Lab Deliverables

| Lab stage | Delivered evidence |
|---|---|
| Topic 2 requirements to data | FR2, FR3 and RAI5 mapped to the eight existing approved sources in the data inventory. |
| Connected coding workspace | Actual Google Colab execution saved: 14 code cells completed without errors, model keys or package installation. |
| Ingestion and inspection | All 8 pinned files acquired with expected SHA-256 matches; actual previews and source properties saved. |
| Relevant pathway only | Pathway A explicitly adapted to Markdown/RST; no unrelated data modalities or dummy dataset. |
| Part B comparison | Both fixed and paragraph-aware methods executed on the same sources; real counts and samples recorded. |
| Part B validation / storage | 350 unique, non-empty, provenance-bearing records; JSONL round-trip and exact source-span/content-coverage checks. |
| Part B lineage | data/week3_manifest.json has 8 source-to-output mappings, actual versions/rights and output hashes. |
| Part C executable V1 | src/week3_pipeline.py plus self-contained notebook, shared Part B configuration and documents output directory. |
| Repeatability | Two runs match source fingerprints, configuration, prepared bytes/counts and mappings; Part B equals Part C. |
| Pipeline diagram | Required PNG visually inspected; editable Draw.io source supplied, with failure responses and chosen operations. |
| Pipeline decisions | Comparison, benefit/limitation, chosen settings, ETL/batch rationale, stage contracts, rights/access and traceability documented. |
| Cumulative progress | README links to Week 3 artifacts, reports actual results and distinguishes remaining application work. |

## Actual Preparation Results

- Sources: 8 files across 3 repositories, exactly matching the unchanged source-selection manifest.
- Fixed method: 320 chunks, 17 boundaries inside fenced Markdown blocks, 299 mid-line boundaries, maximum 500 characters.
- Selected paragraph-aware method: 350 chunks, 0 boundaries inside fenced Markdown blocks, 0 mid-line boundaries, 49 chunks above the soft target, maximum 2,749 characters.
- Every non-whitespace source character is covered by exact source spans. Markdown indentation is preserved; RST underline headings are not treated as Markdown fences. This does not prove semantic completeness or good retrieval.
- Prepared-output SHA-256: `9a71abd2df1a530c6b58d06a41ccf329b23132310421a7766a661ad020834b66`.
- Implementation SHA-256: `5ec0c744f9c8e120c302392b08d3ecf64fe9fcc83d03940eeeacf1382f9d53d4`.

## Execution and Contract Evidence

The command-line implementation executed successfully and ran the integrated pipeline twice. A fresh real Jupyter kernel then executed all **13 code cells** in the self-contained notebook; all completed with no cell errors. Its independently acquired/prepared dataset is byte-identical to the command-line export. Its own two pipeline runs passed repeatability checks. Google Colab then completed all **14 code cells**, including the final manifest-archive cell, using Python 3.13.18 on Linux. The saved notebook outputs are this actual Colab execution; the original 13 processing/export code cells are unchanged. Its two runs at 05:05:51.388925 and 05:05:51.549487 UTC on 11 November 2026 passed, and its prepared bytes match both local executions. Canonical manifests were extracted directly from the final Colab output; the previous local manifest/report are retained in `data/pipeline_v1/documents/local_verification_report.json`. Source version, configuration, output hashes/counts and source/output mappings were compared; timestamps may differ.

The focused **11-test suite passed**, with zero errors/failures. It checks source allowlisting, tampered/missing input, empty/binary-like text, fence/indentation preservation, RST headings, invalid configuration, duplicate/wrong-repository records, full corpus round-trip/content coverage and the observed comparison choice. These are pipeline contracts, not model safety or answer-quality tests.

## Packaging and Consistency Checks

- Required notebook, inventory, diagram, decisions, exports and both distinct manifest types exist.
- Notebook schema validates, every code cell has an execution count, and no error outputs are present.
- Source IDs, version/license metadata and chunk hashes were checked; raw bytes match the expected original fingerprints.
- Both final exports match byte-for-byte; Part B and Part C manifests link all eight sources to their stable record ranges.
- Retained original licenses and Streamlit NOTICES match their review-record hashes; attribution includes a prominent representation-change notice.
- The notebook export ZIP includes the attribution, retained notices, source-selection metadata and rights-review record; raw inputs and secret files are excluded.
- Local Markdown links resolve; editable Draw.io XML parses with valid nodes/edges. The final PNG was visually inspected.
- Raw downloads, credentials, caches and later embedding/index stores are ignored. Curated Week 3 exports are deliberately tracked.
- Missing earlier observation screenshots were extracted losslessly from the existing PDF. The original Week 1 map image was extracted as PNG. The restored Week 2 editable source was accepted only after its paired original PNG matched the repository PNG byte-for-byte.
- No source-manifest refresh, model API spend, source-code execution, embeddings/index, training or chatbot implementation was introduced.

## Remaining User Evidence

The required Google Colab execution is complete and saved in GitHub. Portal submission must be completed and confirmed by the student; no portal interaction or receipt is asserted.
