# RepoLens - AI-Powered GitHub Repository Understanding Assistant

> Helps university students and beginner developers understand selected public GitHub repositories through document-grounded answers with source references.

**Week 1 status:** project scope, README, source selection, evaluation plan and local folder structure prepared. Parts A/B files and authenticated GitHub publication remain pending. This repository contains planning only; the application has not been implemented and no evaluation results have been achieved.

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

Only URLs and metadata are committed in Week 1. Before later redistribution, check file-level exceptions and preserve the applicable license, copyright, disclaimer and attribution/change notices. External links and assets are not included automatically; record a URL if permission is uncertain. See the [project scope](docs/week1_project_scope.md) for collection limits.

## Weekly Progress

| Week | Focus | Deliverable | Status |
|---|---|---|---|
| W1 | Project scoping (C1/C2 preparation) | README, scope, source manifest, evaluation plan | Complete locally |
| W1 | Repository setup (C3) | Required folders and .gitignore | Prepared locally; remote check/create/push pending authentication |
| W1 | Observation sheet and conceptual system map (Parts A/B) | docs/week1_observation_sheet.md; docs/week1_system_map.png | Pending: actual group files not provided |
| W1 | Final Week 1 submission | Verify public GitHub contents and submit repository URL | Pending |
| W2 onward | Requirements, design, implementation and evaluation | To be refined against course schedule | Planned |

**Week 1 overall is not complete.** The absent Part A/B files have not been replaced with fabricated content.

## Proposed AI Approach and Scope

Allowlisted Markdown/RST documentation -> cleaning and chunking -> embeddings and repository-filtered semantic retrieval -> LLM answer -> citation/scope checks -> simple web interface. Cross-repository installation comparisons retrieve evidence for each repository separately. Answers show repository, document, section and fixed source URL; missing evidence triggers explicit abstention. All technology choices remain provisional.

In scope: selected public documentation, natural-language Q&A, citations, a simple web UI and objective evaluation. Out of scope: entire-codebase analysis, arbitrary crawling, execution, automatic dependency installation, private repositories, autonomous modifications, pull requests and complex multi-agent workflows. FastAPI's contribution entry page links externally; detailed uncollected instructions are unsupported. Streamlit's pinned contribution policy must be respected.

## Repository Structure

```text
ai-engineering-repolens/
├── README.md
├── .gitignore
├── docs/
│   └── week1_project_scope.md
├── data/
│   ├── .gitkeep
│   └── source_manifest.json
├── src/.gitkeep
├── notebooks/.gitkeep
├── evaluation/
│   └── plan.md
└── prompts/.gitkeep
```

Required but **absent until supplied**: `docs/week1_observation_sheet.md` and `docs/week1_system_map.png`. These must come from the actual Parts A/B work, not a RepoLens architecture invented for this task.

## Planned Evaluation

Prepare 6 development questions and freeze 30 test questions (24 answerable, 6 unsupported). Annotate reference answers and required source passages. Compare semantic retrieval against BM25 on the same sources/chunks; compare RAG explanations against the same generator with BM25 context. Measure Recall@5, full answer correctness, citation accuracy, groundedness, abstention and end-to-end latency. Preliminary targets and the full protocol are in [evaluation/plan.md](evaluation/plan.md). There are no measured results yet.

## References

- **[R1]** Steinmacher, I., Graciotto Silva, M. A., Gerosa, M. A., & Redmiles, D. F. (2015). *A systematic literature review on the barriers faced by newcomers to open source software projects*. Information and Software Technology, 59, 67-85. [DOI](https://doi.org/10.1016/j.infsof.2014.11.001); [accessible university abstract and bibliographic record](https://experts.nau.edu/en/publications/a-systematic-literature-review-on-the-barriers-faced-by-newcomers/).
- **[R2]** Chen, J., Zhao, K., Liu, J., Peng, C., Liu, J., Zhu, H., Gao, P., Yang, P., & Deng, S. (2025). *CoReQA: Uncovering Potentials of Language Models in Code Repository Question Answering*. arXiv preprint 2501.03447. [Paper and abstract](https://arxiv.org/abs/2501.03447).
- **[R3]** GitHub. (n.d.). *Application card: GitHub Copilot Chat*. [Official documentation](https://docs.github.com/en/copilot/responsible-use/chat). Accessed 22 October 2026.
- **[R4]** Sourcegraph. (n.d.). *Cody FAQs*. [Official documentation](https://sourcegraph.com/docs/cody/faq). Accessed 22 October 2026.
- **[R5]** Liu, J., Tian, J. L., Daita, V., Wei, Y., Ding, Y., Wang, Y. K., Yang, J., & Zhang, L. (2024). *RepoQA: Evaluating Long Context Code Understanding*. arXiv preprint 2406.06025. [Paper and abstract](https://arxiv.org/abs/2406.06025).

