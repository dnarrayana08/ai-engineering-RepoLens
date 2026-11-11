# RepoLens Week 3 Source Attribution and Modifications

The prepared JSONL files contain selected text from the eight source files listed in [source_manifest.json](source_manifest.json). They are derived documentation exports, not new documentation authored by RepoLens. Every chunk carries its original repository, commit, path, source URL, license, source hash and exact text-span identity. External image files, linked pages, source-code files and RST includes are not downloaded or incorporated by this pipeline.

## Copyright and License Records

- **FastAPI**: Copyright (c) 2018 Sebastián Ramírez. Original repository documentation is covered by the [MIT license retained here](third_party/fastapi/LICENSE). Original copyright/permission notice is preserved in full.
- **Streamlit**: documentation from the Streamlit project, under [Apache License 2.0 retained here](third_party/streamlit/LICENSE). The distribution's complete [NOTICES file](third_party/streamlit/NOTICES) is retained unchanged, conservatively, even though the pipeline does not redistribute Streamlit's executable dependencies.
- **scikit-learn**: Copyright (c) 2007-2026 The scikit-learn developers. All rights reserved. The [BSD 3-Clause license and disclaimer](third_party/scikit-learn/COPYING) are retained unchanged.

The pinned license URLs/commits and fetched notice-file hashes are recorded in [week3_rights_review.json](week3_rights_review.json). Repository trees were checked for root notice files; Streamlit's `NOTICES` is included. Source-specific text is kept with its provenance rather than being relabelled as original work. These attributions do not imply upstream endorsement.

## Prominent Modification Notice

**RepoLens modified the representation on 11 November 2026:** raw Markdown/RST text was decoded as UTF-8, CRLF/CR line endings were normalised to LF, then selected by paragraph/fenced-block spans and packaged into JSONL with added provenance fields. Text spans are otherwise exact; non-whitespace source content is retained. Heading labels are derived metadata, not upstream guarantees. No external assets or linked pages are fetched. The source bytes are downloaded into an ignored local raw folder, not committed here.

Both `data/processed/prepared_text.jsonl` and `data/pipeline_v1/documents/prepared_text.jsonl` are covered by this modification notice and the upstream licenses. Keep this attribution file and all applicable notices with copies of these exports. The original pinned URLs remain available for verification. No broad permission over unrelated linked material is claimed.
