# RepoLens Week 3 Pipeline Decisions and Traceability

Date 11 November 2026. This records the **executed** V1 documentation-preparation workflow, rather than a proposed chatbot implementation. Local command-line/Jupyter verification and the actual Google Colab execution are identified separately. The notebook and pipeline source are the executable engineering record.

## Traceability to Topic 2

| Requirement / objective | Data preparation response | Observed evidence / limitation |
|---|---|---|
| O1 / FR2 | Use the eight previously selected documentation files, not dummy data or arbitrary repository crawling. | 8/8 expected source hashes matched; all eight appear in the prepared output. |
| FR3 / RAI5 | Retain repository, path, commit, URL, source hash, section labels and line/character spans. | 350 unique IDs and exact source spans validated; simple heading recognition is not a full structural parser. |
| NFR3 / C01 | Compare preparation choices that may later affect retrieval coverage. | Actual structural boundary results below; Recall@5 has not been measured. |
| RAI3 | Keep downloaded directives/HTML/code as inert text. | No execution or include expansion; tests protect command indentation and read-only source handling. This is not an adversarial model test. |
| O3 / later evidence | Export checks, source/output fingerprints and rerun evidence. | Two same-environment pipeline runs and fresh notebook/CLI output agreement; no downstream Q&A metrics. |

The workflow expands only S1-S3 source preparation/knowledge collection in [Week 2 architecture](week2_architecture_v1.png). It does not redesign the interface, model service or answer guardrails.

## Part B Comparison and Observed Evidence

Both configurations processed the same eight pinned sources. The fixed method cuts after 500 Python Unicode characters. The adapted paragraph-aware method merges adjacent paragraphs where they fit, preserves Markdown fenced blocks and retains overlong atomic blocks rather than truncating them. It is **not semantic chunking**, not a full recursive text splitter and not a token-aware splitter. No overlap is used.

| Observed measure | Fixed-size | Paragraph-aware |
|---|---|---|
| chunk_count | 320 | 350 |
| mid_line_boundaries | 299 | 0 |
| boundaries_inside_fences | 17 | 0 |
| oversize_chunks | 0 | 49 |
| maximum_characters | 500 | 2749 |

A boundary inside a fenced block is detected from the actual source's fence interval. A mid-line boundary falls between two non-newline characters. These are simple, inspectable structural indicators, not proofs that a chunk contains a complete explanation.

| Source | Fixed chunks | Paragraph chunks | Fixed fence cuts | Paragraph fence cuts | Largest paragraph chunk |
|---|---|---|---|---|---|
| D1 | 45 | 45 | 3 | 0 | 1569 |
| D2 | 15 | 13 | 6 | 0 | 2749 |
| D3 | 1 | 1 | 0 | 0 | 271 |
| D4 | 14 | 14 | 1 | 0 | 1936 |
| D5 | 56 | 62 | 7 | 0 | 2418 |
| D6 | 16 | 20 | 0 | 0 | 491 |
| D7 | 30 | 36 | 0 | 0 | 584 |
| D8 | 143 | 159 | 0 | 0 | 2381 |

**Selected configuration:** paragraph-aware, 500-character soft target, overlap 0, UTF-8 strict decoding, CRLF/CR to LF, indentation and markup preserved. The selection rule first minimises boundaries inside fenced blocks, then mid-line boundaries; otherwise it retains fixed splitting. The observed counts selected paragraph-aware. The report is in [chunking_comparison.json](../data/processed/chunking_comparison.json).

**Benefit:** no observed boundary cut inside a Markdown fenced block and no mid-line boundary. **Accepted limitation:** 49/350 chunks exceed the target, with a maximum of 2,749 characters. This is acceptable for a first preparation lab, but a later token-aware strategy must evaluate context-budget and retrieval trade-offs. No claim is made that this configuration meets Recall@5, correctness or latency targets.

## Important Processing Decisions

- **D1 Source format:** Read `.md`, `.rst` and `.txt` as UTF-8 text; restrict this run to the eight approved `.md`/`.rst` inputs. This is an explicit adaptation of the PDF/TXT starter in both Parts B and C; no artificial PDF conversion changes the dataset.
- **D2 Cleaning:** Normalise line endings only. Preserve commands, indentation, HTML, links, Unicode and directives as inert content. Removing all formatting would risk altering instructions. Rich markup remains a later cleanup/quality concern.
- **D3 RST correction:** Inspection/testing showed that RST tilde underline headings can look like Markdown fences. Fence handling is enabled only for Markdown; RST title/underline pairs are recognised separately. An unclosed Markdown fence produces a visible stop rather than silently exporting questionable chunks.
- **D4 Provenance:** Each D1-D8 source maps into a combined file using per-source chunk IDs and ranges. Page is null because the inputs are not paginated PDFs. Sections are best-effort metadata; exact line and character spans provide a checkable fallback.
- **D5 Data rights:** Derived text is exported only with retained licenses/notices and a prominent modification notice. Linked external assets are excluded. Raw input bytes stay ignored and are reacquired from pinned URLs. The existing source manifest is unchanged.
- **D6 Scope:** No embeddings, vector index, model training, orchestration service, deployment or multi-agent system is introduced. Preparing JSONL from document sources does not change this into Pathway D.

## ETL Versus ELT and Batch Versus Streaming

**Selected: batch ETL for the prepared-data destination.** Download and land the raw source bytes for traceability; extract readable text, transform into the chosen chunks, validate and load the prepared JSONL. The existence of a raw landing copy does not imply an in-warehouse ELT implementation. This small finite snapshot is processed as one batch; streaming, scheduled refresh and orchestration would add complexity without a Week 3 requirement.

## Stage Contracts and Failure Responses

| Stage | Contract / evidence | Failure response |
|---|---|---|
| Ingest | Exactly 8 unique approved records; supported suffix; URL/repository/commit identity; raw byte hash matches expected snapshot. | Stop on missing input, redirect, unexpected source, wrong hash or oversized download. Never silently switch to a newer branch. |
| Inspect | Strict UTF-8 decoding, non-empty text, actual previews/counts and RST/Markdown-specific handling. | Stop on decoding errors, binary/null content, empty input or unclosed Markdown fence; report the source for review. |
| Prepare | Chosen configuration equals the Part B method; exact text spans, no overlapping records and no non-whitespace source loss. | Stop on transformation/coverage failure; do not truncate overlong blocks to force a cosmetic size target. |
| Store and validate | JSONL round-trip equality; non-empty file; unique IDs; source/record metadata and content hashes verified. | Stop on missing/empty export, duplicate IDs, wrong repository or altered content. |
| Record lineage | All 8 sources map to the exact output hash and per-source record range with version/license metadata. | Stop/report a missing source/output relationship or inconsistent metadata before calling the run complete. |
| Rerun | Source fingerprints, configuration, output bytes/counts and mappings match; Part B equals Part C. | Raise a repeatability failure; investigate changed inputs/configuration/environment rather than claiming reproducibility. |

The [pipeline diagram](week3_pipeline_diagram.png) documents the actual selected stages and failure responses. Its [editable Draw.io source](week3_pipeline_diagram.drawio) is supplied as an extra artifact.

## Output Locations and Manifest Roles

| Artifact | Meaning |
|---|---|
| data/source_manifest.json | Unchanged Week 1 source-selection record; not a substitute for a Week 3 execution manifest. |
| data/processed/prepared_text.jsonl | Part B prepared dataset, 350 records from 8 sources. |
| data/processed/inspection.json | Actual source properties, previews and initial limitations. |
| data/processed/chunking_comparison.json | Observed fixed/paragraph candidate metrics and selected method. |
| data/week3_manifest.json | Part B processing lineage; each source maps to the combined export. |
| data/pipeline_v1/documents/prepared_text.jsonl | Part C integrated-pipeline output; byte-identical to Part B. |
| data/pipeline_v1/documents/pipeline_manifest.json | Part C execution record: configuration, environment, implementation hash, sources, outputs, mappings and validation. |
| data/pipeline_v1/documents/repeatability_report.json | Two-run same-environment smoke-check result. |
| data/ATTRIBUTION.md and data/third_party/ | Source attribution, representation changes, original license and notice text. |


**Actual prepared-output SHA-256:** `9a71abd2df1a530c6b58d06a41ccf329b23132310421a7766a661ad020834b66`.

The notebook uses the same embedded source implementation as `src/week3_pipeline.py`, identified by SHA-256 in each run. Source data and licenses are downloaded by fixed URL and verified; executable pipeline code is embedded, not fetched from an arbitrary branch. The saved notebook contains the actual successful Google Colab execution of all 14 code cells, including a final cell archiving runtime manifests. Independent local command-line and 13-cell Jupyter executions produced identical prepared bytes. Colab used Python 3.13.18 on Linux; local verification used Python 3.12.14 on Darwin. This observed agreement is not a guarantee for every future environment. No package installation or model keys were needed.

## Repeatability and Test Evidence

Two integrated CLI runs matched source fingerprints, prepared output fingerprint/size/count, configuration, implementation hash and mappings. Part B and Part C output bytes match. Execution timestamps may differ and are not compared. The notebook independently reruns the two-run smoke check in a fresh workspace. This does not establish cross-environment reproducibility or comprehensive data quality.

Focused tests cover fence/indentation preservation, RST underline headings, malformed Markdown fences, invalid configuration, empty/binary-like input, an unapproved source URL, changed cached bytes, a missing input, duplicate/wrong-repository records, export round-trip and the observed comparison decision. See [test report](../data/pipeline_v1/documents/test_report.json) and [test source](../tests/test_week3_pipeline.py). No model safety, retrieval or answer-quality test is reported as passed.

## Reflections and Next Review

The main engineering choice is preserving source context instead of enforcing a hard chunk-size ceiling. The comparison shows that fixed splitting is simple and bounded but can cut installation examples; keeping atomic blocks avoids those cuts while allowing long chunks. Later work should assess token budgets, richer Markdown/RST parsing, boilerplate treatment and retrieval effectiveness before changing this choice. Topic 4 should assess fitness for purpose, coverage, residual markup and responsible-data concerns more comprehensively.

Save permitted outputs and the notebook before Colab resets. Browser/portal submission and a Colab run must be confirmed by actual user-visible evidence, not inferred from a local successful run or the existence of repository files.
