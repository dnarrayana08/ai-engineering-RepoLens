# RepoLens Week 3 Data Inventory

Date 11 November 2026. **Actual project data, not synthetic practice data.** All eight sources were fetched from the pre-existing fixed commits and passed the expected SHA-256 checks. The executed notebook uses Pathway A adapted for Markdown and RST. No PDF conversion is necessary and no unrelated modality is processed.

## Requirements to Data Needs

| Requirement ID | Needed information / feature | Candidate source | Why usable / constraint |
|---|---|---|---|
| FR2 | Repository purpose, installation, prerequisites and contributions | D1-D8 documentation files below | Public project-maintained documentation with selected-topic coverage; excludes uncollected code and linked pages. |
| FR3 | Verifiable document/section references | Source URLs, paths, derived headings and line spans from D1-D8 | Every chunk retains source and commit identity; heading recognition is simple rather than a full parser. |
| RAI5 | Repository/version identity and source rights | Existing source manifest and pinned license/notice files | Fixed commits, expected hashes and retained notices; source review does not make untrusted text executable instructions. |

## Source Inventory and Observed Inspection

All source URLs below are version-specific; full 40-character commits, source SHA-256 values and owners remain in the unchanged [Week 1 source manifest](../data/source_manifest.json). The owners are the named upstream projects, not RepoLens. Collection/run date is recorded separately from source version: a commit snapshot is not a claim that it is the latest release.

| Source ID | Filename / URL | Type | Purpose | Version / owner | Access / rights | Inspection evidence |
|---|---|---|---|---|---|---|
| D1 | [fastapi/fastapi / README.md](https://raw.githubusercontent.com/fastapi/fastapi/4bdfbe4513084b19e22421ce1f916d8c1ac462a0/README.md) | Markdown | Purpose, technologies, installation and running examples | 4bdfbe451308 / fastapi/fastapi | MIT | 22228 bytes; 22011 characters; 533 lines; 29 headings; 45 chunks |
| D2 | [fastapi/fastapi / docs/en/docs/tutorial/index.md](https://raw.githubusercontent.com/fastapi/fastapi/4bdfbe4513084b19e22421ce1f916d8c1ac462a0/docs/en/docs/tutorial/index.md) | Markdown | Installation and tutorial entry point | 4bdfbe451308 / fastapi/fastapi | MIT | 7464 bytes; 7458 characters; 141 lines; 5 headings; 13 chunks |
| D3 | [fastapi/fastapi / docs/en/docs/contributing.md](https://raw.githubusercontent.com/fastapi/fastapi/4bdfbe4513084b19e22421ce1f916d8c1ac462a0/docs/en/docs/contributing.md) | Markdown | Contribution entry point; external development guide is not ingested | 4bdfbe451308 / fastapi/fastapi | MIT | 271 bytes; 271 characters; 7 lines; 2 headings; 1 chunks |
| D4 | [streamlit/streamlit / README.md](https://raw.githubusercontent.com/streamlit/streamlit/f478c9783be8099f1d394d02dea77bd0697d93ea/README.md) | Markdown | Purpose, installation, running and contribution policy | f478c9783be8 / streamlit/streamlit | Apache-2.0 | 7008 bytes; 6965 characters; 150 lines; 12 headings; 14 chunks |
| D5 | [streamlit/streamlit / CONTRIBUTING.md](https://raw.githubusercontent.com/streamlit/streamlit/f478c9783be8099f1d394d02dea77bd0697d93ea/CONTRIBUTING.md) | Markdown | Contribution guidance and policy | f478c9783be8 / streamlit/streamlit | Apache-2.0 | 27548 bytes; 27536 characters; 594 lines; 54 headings; 62 chunks |
| D6 | [scikit-learn/scikit-learn / README.rst](https://raw.githubusercontent.com/scikit-learn/scikit-learn/718eedb7af8678255de080d4748d9f67e321ba41/README.rst) | RST | Purpose and project overview | 718eedb7af86 / scikit-learn/scikit-learn | BSD-3-Clause | 7676 bytes; 7676 characters; 217 lines; 19 headings; 20 chunks |
| D7 | [scikit-learn/scikit-learn / doc/install.rst](https://raw.githubusercontent.com/scikit-learn/scikit-learn/718eedb7af8678255de080d4748d9f67e321ba41/doc/install.rst) | RST | Installation options and requirements | 718eedb7af86 / scikit-learn/scikit-learn | BSD-3-Clause | 14525 bytes; 14505 characters; 426 lines; 15 headings; 36 chunks |
| D8 | [scikit-learn/scikit-learn / doc/developers/contributing.rst](https://raw.githubusercontent.com/scikit-learn/scikit-learn/718eedb7af8678255de080d4748d9f67e321ba41/doc/developers/contributing.rst) | RST | Contribution guidance | 718eedb7af86 / scikit-learn/scikit-learn | BSD-3-Clause | 71320 bytes; 71305 characters; 1665 lines; 30 headings; 159 chunks |

Detailed machine-readable inspection is in [inspection.json](../data/processed/inspection.json). It contains actual content previews and heading lists for each source. The notebook also displays representative D1 and D4 content, exceeding the two-file inspection checkpoint.

## Inspection Findings and Preparation Implications

1. The README filename repeats across projects. Preserve repository subdirectories and stable D1-D8 IDs to avoid overwriting or source confusion.
2. Markdown files contain links, HTML and fenced command/code blocks. Keep indentation and fenced blocks intact; do not apply blanket whitespace collapse or render embedded HTML.
3. RST uses underline headings, including tildes. Those must not be mistaken for Markdown fences. RST directives remain inert text; the pipeline does not resolve include files or execute extensions.
4. FastAPI D3 is a short contribution entry point that delegates detailed instructions externally. Preserve the entry-point link without pretending to have ingested the destination.
5. Streamlit's pinned contribution-policy wording must survive preparation. A snapshot documents its captured state, not a guarantee about the current policy.
6. All sources decoded as UTF-8 and were non-empty. Text and code remain source data even if they contain instructions addressed to AI tools. None of those instructions is acted on.

## Raw Versus Prepared Storage

| Location | Role | Sharing decision |
|---|---|---|
| data/raw/<owner>/<repository>/<original path> | Unmodified pinned download bytes; reacquired from source URLs for each fresh notebook run. | Ignored in Git; not needed for redistribution because URLs/hashes allow reacquisition. |
| data/processed/prepared_text.jsonl | Part B combined export; 350 records across 8 sources. | Committed with upstream licenses, complete Streamlit NOTICES and the prominent modification notice. |
| data/week3_manifest.json | Part B source-to-prepared-output provenance with per-source record ranges. | Committed; contains project-source metadata, not secrets. |
| data/pipeline_v1/documents/ | Part C prepared export, execution manifest and two-run repeatability report. | Committed; actual Colab run records and separately identified local verification. |
| data/third_party/ and data/ATTRIBUTION.md | Retained licenses/notices, owners and representation changes. | Keep with exported derived text. |

## Source Rights and Provenance Review

The pinned repository licenses and root notice files were retrieved and inspected. FastAPI uses MIT, Streamlit Apache-2.0, and scikit-learn BSD-3-Clause. Streamlit's complete root NOTICES is retained; the source manifest was not silently updated. See [attribution and modification notice](../data/ATTRIBUTION.md) and [rights-review record](../data/week3_rights_review.json). Do not assume the license covers every linked image, website or external document; none is fetched here.

SHA-256 proves that downloaded bytes match the chosen snapshot; it is not proof of permission or fitness for purpose. Derived headings/line metadata and record boundaries need later quality review. Colab files are temporary; save notebook/exports before resetting the runtime.

## Execution and Quality Status

The command-line pipeline, a fresh local Jupyter-kernel execution, and Google Colab independently produced byte-identical prepared exports. All 14 Colab code cells completed on 11 November 2026 (Python 3.13.18, Linux). Actual Colab manifests are archived in the final notebook output and committed under the canonical manifest paths; local evidence is preserved separately. No model keys or package installation were needed.

Basic checks passed for all 350 records: non-empty text, unique record IDs, exact source spans, all 8 source identities, source hashes, export round-trip and preservation of non-whitespace content. This is not a Topic 4 comprehensive quality assessment, a retrieval benchmark or an answer-accuracy result.
