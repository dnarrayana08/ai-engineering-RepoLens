# RepoLens - AI-Powered GitHub Repository Understanding Assistant

> Helps university students and beginner developers understand selected public GitHub repositories through document-grounded answers with source references.

**Current status (27 October 2026):** Week 1 materials and all four required Week 2 planning deliverables are available in this repository. The application, final benchmark and evaluation results are planned; there is no runnable RepoLens application yet. Some repository-format and supporting-file items remain open in the checklist below.

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

The upstream documentation dataset is represented by URLs and metadata; its document copies have not been committed. Before later redistribution, check file-level exceptions and preserve the applicable license, copyright, disclaimer and attribution/change notices. External links and assets are not included automatically; record a URL if permission is uncertain. See the [project scope](docs/week1_project_scope.md) for collection limits.

## Weekly Progress

| Week | Focus | Deliverable | Status |
|---|---|---|---|
| W1 | Project scoping | README, project scope, source manifest and initial evaluation plan | Available in GitHub |
| W1 | Analyse an existing AI system | Observation sheet in Markdown and PDF | Uploaded; PDF includes evidence screenshots; Markdown image assets still need uploading |
| W1 | Conceptual system map | System map and reflection in PDF | Uploaded; required PNG export still pending |
| W1 | Repository setup | Public GitHub repository and planning files | Repository exists; missing folders and .gitignore listed below |
| W1 | Course portal submission | Repository URL | Not verified in this repository |
| W2 | Requirements and application scope | Section 0 framing, 7 FRs, 5 NFRs and 5 Responsible AI requirements | Planning document available in GitHub |
| W2 | Evaluation criteria | 12 criteria, proposed metrics/thresholds and evaluation protocol | Planning document available in GitHub; tests not run |
| W2 | V1 architecture and justification | Architecture PNG, 6 decisions and 12 traceability rows | Required files available in GitHub; linked editable Draw.io source still missing |
| W3 onward | Implementation and evaluation | Data processing, retrieval, grounded answers, interface and measured evidence | Planned |

## Proposed AI Approach and Scope

Allowlisted Markdown/RST documentation -> cleaning and chunking -> embeddings and repository-filtered semantic retrieval -> LLM answer -> citation/scope checks -> simple web interface. Cross-repository installation comparisons retrieve evidence for each repository separately. Answers show repository, document, section and fixed source URL; missing evidence triggers explicit abstention. All technology choices remain provisional.

In scope: selected public documentation, natural-language Q&A, citations, a simple web UI and objective evaluation. Out of scope: entire-codebase analysis, arbitrary crawling, execution, automatic dependency installation, private repositories, autonomous modifications, pull requests and complex multi-agent workflows. FastAPI's contribution entry page links externally; detailed uncollected instructions are unsupported. Streamlit's pinned contribution policy must be respected.

## Repository Structure

Current tracked files:

```text
ai-engineering-RepoLens/
├── README.md
├── data/
│   └── source_manifest.json
├── docs/
│   ├── week1_observation_sheet.md
│   ├── week1_observation_sheet.pdf
│   ├── week1_project_scope.md
│   ├── week1_system_map.pdf
│   ├── week2_requirements.md
│   ├── week2_evaluation_criteria.md
│   ├── week2_architecture_v1.png
│   └── week2_architecture_decisions.md
└── evaluation/
    └── plan.md
```

### Remaining Repository and Submission Items

- [ ] Export the existing Week 1 system map as `docs/week1_system_map.png`, as required by the lab. The PDF is already available above.
- [ ] Add `docs/week1_observation_assets/evidence_1.jpg`, `evidence_2.jpg` and `evidence_3.jpg` to restore the observation Markdown's embedded screenshots. The observation PDF currently preserves them.
- [ ] Upload `docs/week2_architecture_v1.drawio` so the editable-source links in the Week 2 documents resolve. The required architecture PNG is already present.
- [ ] Add the planned `src/`, `notebooks/` and `prompts/` directories, using `.gitkeep` files while empty.
- [ ] Add `.gitignore` rules for credentials, `.env` files, virtual environments, caches, raw document copies and generated indices/logs before implementation.
- [ ] Confirm the actual course portal submission. File presence in GitHub does not establish that submission occurred.

## Planned Evaluation

Prepare 6 development questions and freeze 30 test questions (24 answerable, 6 unsupported). Annotate reference answers and required source passages. Compare semantic retrieval against BM25 on the same sources/chunks; compare RAG explanations against the same generator with BM25 context. Measure Recall@5, full answer correctness, citation accuracy, groundedness, abstention and end-to-end latency. The [initial evaluation plan](evaluation/plan.md) records the Week 1 design. The [Week 2 evaluation criteria](docs/week2_evaluation_criteria.md) refine the acceptance rules, repeat-run scoring, privacy/safety checks, failure handling and proposed cost cap; use those criteria for the later evaluation. There are no measured results yet.

## References

- **[R1]** Steinmacher, I., Graciotto Silva, M. A., Gerosa, M. A., & Redmiles, D. F. (2015). *A systematic literature review on the barriers faced by newcomers to open source software projects*. Information and Software Technology, 59, 67-85. [DOI](https://doi.org/10.1016/j.infsof.2014.11.001); [accessible university abstract and bibliographic record](https://experts.nau.edu/en/publications/a-systematic-literature-review-on-the-barriers-faced-by-newcomers/).
- **[R2]** Chen, J., Zhao, K., Liu, J., Peng, C., Liu, J., Zhu, H., Gao, P., Yang, P., & Deng, S. (2025). *CoReQA: Uncovering Potentials of Language Models in Code Repository Question Answering*. arXiv preprint 2501.03447. [Paper and abstract](https://arxiv.org/abs/2501.03447).
- **[R3]** GitHub. (n.d.). *Application card: GitHub Copilot Chat*. [Official documentation](https://docs.github.com/en/copilot/responsible-use/chat). Accessed 22 October 2026.
- **[R4]** Sourcegraph. (n.d.). *Cody FAQs*. [Official documentation](https://sourcegraph.com/docs/cody/faq). Accessed 22 October 2026.
- **[R5]** Liu, J., Tian, J. L., Daita, V., Wei, Y., Ding, Y., Wang, Y. K., Yang, J., & Zhang, L. (2024). *RepoQA: Evaluating Long Context Code Understanding*. arXiv preprint 2406.06025. [Paper and abstract](https://arxiv.org/abs/2406.06025).

