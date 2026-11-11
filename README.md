# RepoLens - AI-Powered GitHub Repository Understanding Assistant

> Helps university students and beginner developers understand selected public GitHub repositories through document-grounded answers with source references.

**Current status (11 November 2026):** Week 1/2 materials and the Topic 3 documentation-preparation pipeline are available. The pipeline processed all eight pinned sources into **350 traceable chunks**; two-run repeatability, export validation and 11 data-contract tests passed locally. The self-contained notebook was executed with a real local Jupyter kernel; Google Colab execution is not claimed. The RepoLens chatbot, embeddings, retrieval benchmark and answer-quality evaluation remain future work.

## Project Documents

| Topic | Document |
|---|---|
| Week 1 | [Project scope](docs/week1_project_scope.md) |
| Week 1 | [Observation sheet - Markdown](docs/week1_observation_sheet.md) and [PDF with evidence screenshots](docs/week1_observation_sheet.pdf) |
| Week 1 | [Conceptual system map and reflection - PDF](docs/week1_system_map.pdf) |
| Week 2 | [Requirements specification](docs/week2_requirements.md) |
| Week 2 | [Evaluation criteria](docs/week2_evaluation_criteria.md) |
| Week 2 | [V1 architecture diagram](docs/week2_architecture_v1.png) |
| Week 2 | [Architecture decisions and traceability](docs/week2_architecture_decisions.md) |
| Week 3 | [Runnable pipeline notebook](notebooks/week3_pipeline.ipynb) and [Colab/run guide](docs/week3_run_guide.md) |
| Week 3 | [Data inventory](docs/week3_data_inventory.md) and [pipeline decisions](docs/week3_pipeline_decisions.md) |
| Week 3 | [Pipeline diagram](docs/week3_pipeline_diagram.png) and [editable Draw.io source](docs/week3_pipeline_diagram.drawio) |
| Week 3 | [Part B export](data/processed/prepared_text.jsonl), [lineage](data/week3_manifest.json) and [Part C evidence](data/pipeline_v1/documents/) |
| Data and evaluation | [Source manifest](data/source_manifest.json) and [initial evaluation plan](evaluation/plan.md) |

The Week 1 observation sheet and system map examine **Claude**, the system analysed in Parts A/B. The Week 2 architecture describes the proposed **RepoLens** application. Observations about Claude are not RepoLens test results.

## Problem Statement

Students and beginner developers must find and interpret purpose, installation, prerequisite and contribution information across unfamiliar repository documentation. RepoLens proposes semantic retrieval and an LLM to answer paraphrased questions, combine selected passages and explain instructions with citations. Its value over keyword retrieval will be evaluated rather than assumed.

## Evidence of the Problem

- **Evidence 1:** Open-source newcomer research identifies documentation, finding a starting point and technical hurdles as contribution barriers (Steinmacher et al., 2015, [R1]). It motivates guidance without proving our solution works.
- **Evidence 2:** CoReQA finds difficulties in repository-level QA for evaluated retrieval and long-context baselines (Chen et al., 2025, [R2]). Its broader code task motivates evaluation but does not predict results for our documentation dataset.

## Initial Related Work / Existing Approaches

- **GitHub Copilot Chat / Spaces [R3]:** contextual coding Q&A with curated repository materials. **Documented limitation:** only part of included context is used, and answers require review. Curated repository Q&A is an existing capability.
- **Sourcegraph Cody [R4]:** retrieves code context for an LLM. **Documented limitation:** depends on Sourcegraph; Free, Pro and Enterprise Starter plans were sunset on 23 July 2025, with Enterprise continuing. The current FAQ describes Search-based Enterprise retrieval, not embeddings.
- **RepoQA [R5]:** evaluates natural-language function search in long code contexts. **Our task-mismatch assessment:** it does not directly evaluate beginner documentation explanations, installation comparisons or answer citation quality.

## Engineering Gap / Limitation

**Gap / Limitation:** This project needs a small, reproducible documentation assistant that keeps repositories and versions separate, explains instructions for beginners, cites the supporting document sections and declines unsupported questions. Existing products and research provide relevant capabilities, but do not establish performance on this project's fixed eight-document beginner benchmark. This is our proposed engineering and evaluation gap, not a claim that all existing assistants lack these features or that RAG is novel.

## Project Objectives

- **O1:** To design a bounded documentation dataset and processing specification covering exactly three repositories and eight selected files, with source URLs, commit IDs, licenses and section-level provenance recorded for every file.
- **O2:** To develop, during the semester, a simple web RAG prototype supporting repository selection, natural-language Q&A, two-repository installation comparison, source references and explicit abstention when evidence is insufficient; demonstrate each function with at least one acceptance case.
- **O3:** To evaluate the prototype against a BM25 keyword retrieval baseline on a frozen 30-question test set, targeting Recall@5 >= 0.85, fully correct answers >= 80%, citation accuracy and groundedness >= 90%, and p95 response latency <= 15 seconds under the protocol in the evaluation plan. These are preliminary targets, not achieved results.

## Target Users

University computing students and beginner developers exploring FastAPI, Streamlit and scikit-learn. Initial support covers English-language documentation and questions.

## Data Sources

Fixed initial collection: **three repositories and eight documents**. Streamlit's README supplies installation and running instructions; a separate installation file is not required for that repository.

| ID | Repository | Selected public document (fixed commit URL) | Relevance |
|---|---|---|---|
| D1 | fastapi/fastapi | [README.md](https://raw.githubusercontent.com/fastapi/fastapi/4bdfbe4513084b19e22421ce1f916d8c1ac462a0/README.md) | Purpose, technologies, installation and running examples |
| D2 | fastapi/fastapi | [docs/en/docs/tutorial/index.md](https://raw.githubusercontent.com/fastapi/fastapi/4bdfbe4513084b19e22421ce1f916d8c1ac462a0/docs/en/docs/tutorial/index.md) | Installation and tutorial entry point |
| D3 | fastapi/fastapi | [docs/en/docs/contributing.md](https://raw.githubusercontent.com/fastapi/fastapi/4bdfbe4513084b19e22421ce1f916d8c1ac462a0/docs/en/docs/contributing.md) | Contribution entry point; external development guide is not ingested |
| D4 | streamlit/streamlit | [README.md](https://raw.githubusercontent.com/streamlit/streamlit/f478c9783be8099f1d394d02dea77bd0697d93ea/README.md) | Purpose, installation, running and contribution policy |
| D5 | streamlit/streamlit | [CONTRIBUTING.md](https://raw.githubusercontent.com/streamlit/streamlit/f478c9783be8099f1d394d02dea77bd0697d93ea/CONTRIBUTING.md) | Contribution guidance and policy |
| D6 | scikit-learn/scikit-learn | [README.rst](https://raw.githubusercontent.com/scikit-learn/scikit-learn/718eedb7af8678255de080d4748d9f67e321ba41/README.rst) | Purpose and project overview |
| D7 | scikit-learn/scikit-learn | [doc/install.rst](https://raw.githubusercontent.com/scikit-learn/scikit-learn/718eedb7af8678255de080d4748d9f67e321ba41/doc/install.rst) | Installation options and requirements |
| D8 | scikit-learn/scikit-learn | [doc/developers/contributing.rst](https://raw.githubusercontent.com/scikit-learn/scikit-learn/718eedb7af8678255de080d4748d9f67e321ba41/doc/developers/contributing.rst) | Contribution guidance |

Verified by successful HTTP retrieval on 22 October 2026. [Machine-readable manifest](data/source_manifest.json) records commit IDs, content hashes and license URLs.

- **fastapi/fastapi: MIT** - [verified repository license](https://raw.githubusercontent.com/fastapi/fastapi/4bdfbe4513084b19e22421ce1f916d8c1ac462a0/LICENSE).
- **streamlit/streamlit: Apache-2.0** - [verified repository license](https://raw.githubusercontent.com/streamlit/streamlit/f478c9783be8099f1d394d02dea77bd0697d93ea/LICENSE).
- **scikit-learn/scikit-learn: BSD-3-Clause** - [verified repository license](https://raw.githubusercontent.com/scikit-learn/scikit-learn/718eedb7af8678255de080d4748d9f67e321ba41/COPYING).

Week 3 now includes derived text chunks from the eight selected documents. Original raw downloads remain ignored and can be reacquired from the fixed URLs. The [attribution and modification notice](data/ATTRIBUTION.md), [source-rights review](data/week3_rights_review.json) and retained licenses/Streamlit NOTICES accompany those exports. External linked assets and documents are not downloaded. See the [project scope](docs/week1_project_scope.md) for the original collection boundary.

## Weekly Progress

| Week | Focus | Deliverable | Status |
|---|---|---|---|
| W1 | Project scoping | README, project scope, source manifest and initial evaluation plan | Available in GitHub |
| W1 | Analyse an existing AI system | Observation sheet in Markdown and PDF | Uploaded; Markdown evidence screenshots restored from the supplied PDF |
| W1 | Conceptual system map | System map and reflection in PDF | PDF and PNG available; PNG extracted from the supplied map |
| W1 | Repository setup | Public GitHub repository and planning files | Repository, planned folders and .gitignore available |
| W1 | Course portal submission | Repository URL | Not verified in this repository |
| W2 | Requirements and application scope | Section 0 framing, 7 FRs, 5 NFRs and 5 Responsible AI requirements | Planning document available in GitHub |
| W2 | Evaluation criteria | 12 criteria, proposed metrics/thresholds and evaluation protocol | Planning document available in GitHub; tests not run |
| W2 | V1 architecture and justification | Architecture PNG, 6 decisions and 12 traceability rows | Required files and matching editable Draw.io source available |
| W3 | Data engineering | Notebook, inventory, decisions, diagram, prepared exports and manifests | Implemented and verified locally; Colab run pending |
| W3 | Preparation comparison | Fixed-size versus paragraph-aware splitting across 8 sources | 320 versus 350 chunks; fenced-block cuts 17 versus 0; 49 selected chunks exceed the soft size target |
| W3 | Validation and repeatability | Same-environment reruns, CLI/notebook agreement and focused tests | PASS; 11 tests; no downstream answer/retrieval result claimed |
| Later topics | Retrieval, grounded answers and interface | Embeddings/index, application and benchmark evaluation | Planned |

## Proposed AI Approach and Scope

Allowlisted Markdown/RST documentation -> cleaning and chunking -> embeddings and repository-filtered semantic retrieval -> LLM answer -> citation/scope checks -> simple web interface. Cross-repository installation comparisons retrieve evidence for each repository separately. Answers show repository, document, section and fixed source URL; missing evidence triggers explicit abstention. All technology choices remain provisional.

In scope: selected public documentation, natural-language Q&A, citations, a simple web UI and objective evaluation. Out of scope: entire-codebase analysis, arbitrary crawling, execution, automatic dependency installation, private repositories, autonomous modifications, pull requests and complex multi-agent workflows. FastAPI's contribution entry page links externally; detailed uncollected instructions are unsupported. Streamlit's pinned contribution policy must be respected.

## Week 3 Pipeline

[Open in Google Colab](https://colab.research.google.com/github/dnarrayana08/ai-engineering-RepoLens/blob/main/notebooks/week3_pipeline.ipynb) and select **Runtime > Run all**. Save the actual executed notebook and the export ZIP before the runtime resets. No model API key or package installation is required.

The selected workflow is batch ETL: fixed documentation sources -> verified ingestion -> text inspection -> compared/chosen preparation -> validated JSONL -> source/output lineage -> repeatability check. Markdown/RST are read directly, preserving indentation and treating embedded instructions as inert text. The same configuration is used in Parts B and C.

The measured structural comparison selected paragraph-aware splitting: it avoids observed fenced-block and mid-line cuts, but permits atomic blocks above the 500-character target (49 chunks; maximum 2,749 characters). This is preparation evidence, not proof of better retrieval or answers. See [decisions](docs/week3_pipeline_decisions.md) and [verification](docs/week3_verification.md).

## Repository Structure

```text
ai-engineering-RepoLens/
├── README.md
├── .gitignore
├── src/
│   └── week3_pipeline.py
├── notebooks/
│   └── week3_pipeline.ipynb
├── tests/
│   └── test_week3_pipeline.py
├── prompts/
│   └── .gitkeep
├── docs/
│   ├── week1_observation_sheet.md / .pdf
│   ├── week1_observation_assets/
│   ├── week1_project_scope.md
│   ├── week1_system_map.pdf / .png
│   ├── week2_requirements.md
│   ├── week2_evaluation_criteria.md
│   ├── week2_architecture_v1.png / .drawio
│   ├── week2_architecture_decisions.md
│   ├── week3_data_inventory.md
│   ├── week3_pipeline_decisions.md
│   ├── week3_pipeline_diagram.png / .drawio
│   ├── week3_run_guide.md
│   └── week3_verification.md
├── data/
│   ├── source_manifest.json
│   ├── ATTRIBUTION.md
│   ├── third_party/
│   ├── week3_rights_review.json
│   ├── week3_manifest.json
│   ├── processed/
│   │   ├── prepared_text.jsonl
│   │   ├── inspection.json
│   │   └── chunking_comparison.json
│   └── pipeline_v1/documents/
│       ├── prepared_text.jsonl
│       ├── pipeline_manifest.json
│       ├── repeatability_report.json
│       └── test_report.json
└── evaluation/
    └── plan.md
```

`data/raw/` is created during execution and ignored in Git. The grouped `.md / .pdf` and `.png / .drawio` entries above represent separate files.

### Repository and Submission Checklist

- [x] Week 1 observation screenshots restored from the uploaded PDF.
- [x] Week 1 map PNG extracted from the uploaded map PDF; original PDF/reflection retained.
- [x] Matching Week 2 editable Draw.io source restored.
- [x] Required working folders and credential/cache exclusions added.
- [x] Topic 3 notebook, inventory, diagram, decisions, Part B/Part C outputs and manifests prepared and verified locally.
- [x] Source licenses/notices and representation-change attribution retained with derived exports.
- [ ] Run the notebook in Google Colab and save that actual execution evidence for the lab. Local execution has already been verified; it must not be relabelled as Colab.
- [ ] Confirm actual course portal submissions. Repository file presence does not establish portal submission.

## Planned Evaluation

Prepare 6 development questions and freeze 30 test questions (24 answerable, 6 unsupported). Annotate reference answers and required source passages. Compare semantic retrieval against BM25 on the same sources/chunks; compare RAG explanations against the same generator with BM25 context. Measure Recall@5, full answer correctness, citation accuracy, groundedness, abstention and end-to-end latency. The [initial evaluation plan](evaluation/plan.md) records the Week 1 design. The [Week 2 evaluation criteria](docs/week2_evaluation_criteria.md) refine the acceptance rules, repeat-run scoring, privacy/safety checks, failure handling and proposed cost cap; use those criteria for the later evaluation. No application-level retrieval or answer-quality results have been measured; Week 3 reports only data-preparation and validation evidence.

## References

- **[R1]** Steinmacher, I., Graciotto Silva, M. A., Gerosa, M. A., & Redmiles, D. F. (2015). *A systematic literature review on the barriers faced by newcomers to open source software projects*. Information and Software Technology, 59, 67-85. [DOI](https://doi.org/10.1016/j.infsof.2014.11.001); [accessible university abstract and bibliographic record](https://experts.nau.edu/en/publications/a-systematic-literature-review-on-the-barriers-faced-by-newcomers/).
- **[R2]** Chen, J., Zhao, K., Liu, J., Peng, C., Liu, J., Zhu, H., Gao, P., Yang, P., & Deng, S. (2025). *CoReQA: Uncovering Potentials of Language Models in Code Repository Question Answering*. arXiv preprint 2501.03447. [Paper and abstract](https://arxiv.org/abs/2501.03447).
- **[R3]** GitHub. (n.d.). *Application card: GitHub Copilot Chat*. [Official documentation](https://docs.github.com/en/copilot/responsible-use/chat). Accessed 22 October 2026.
- **[R4]** Sourcegraph. (n.d.). *Cody FAQs*. [Official documentation](https://sourcegraph.com/docs/cody/faq). Accessed 22 October 2026.
- **[R5]** Liu, J., Tian, J. L., Daita, V., Wei, Y., Ding, Y., Wang, Y. K., Yang, J., & Zhang, L. (2024). *RepoQA: Evaluating Long Context Code Understanding*. arXiv preprint 2406.06025. [Paper and abstract](https://arxiv.org/abs/2406.06025).

