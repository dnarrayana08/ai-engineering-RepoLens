# Week 1 Project Scoping Document

Status: C2 planning completed; application development and evaluation have not started. Updated 22 October 2026. Fields below follow the Part C template on pages 12-13, in order. Additional planning follows the template fields.

## Project Name

RepoLens - AI-Powered GitHub Repository Understanding Assistant

## Domain

Software Engineering / Developer Tools / Natural Language Processing

## Problem Statement

University students and beginner developers need to locate and interpret purpose, installation, prerequisite and contribution information when exploring unfamiliar public repositories. Relevant information can span README, installation and contribution files, while a beginner's wording may differ from documentation terminology. RepoLens proposes document-grounded Q&A using semantic retrieval and an LLM to explain and combine selected evidence with citations; its benefit over keyword retrieval must be tested.

## Evidence of the Problem

**Evidence 1:** A systematic review identifies documentation, finding a starting point and technical hurdles among barriers to open-source contribution. This supports a need for newcomer guidance; it does not establish RepoLens's effectiveness.

**Source / citation:** Steinmacher et al. (2015), [R1].

**Evidence 2:** CoReQA reports difficulties answering repository-level questions with evaluated retrieval-based and long-context baselines. These are broader code questions, so the finding motivates evaluation rather than predicting performance on our smaller documentation task.

**Source / citation:** Chen et al. (2025), [R2].

## Initial Related Work (at least 3)

**Study / solution 1:** GitHub Copilot Chat provides contextual coding assistance; Spaces can curate repository materials.

**Source / citation:** GitHub official application card, [R3].

**Key limitation (documented):** Spaces uses only a portion of included content; responses require review. RepoLens therefore needs explicit retrieval and citation evaluation. We do not claim curated repository Q&A is novel.

**Study / solution 2:** Sourcegraph Cody retrieves relevant code context for an LLM.

**Source / citation:** Sourcegraph official FAQ, [R4].

**Key limitation (documented):** Cody depends on Sourcegraph; Free, Pro and Enterprise Starter plans were sunset on 23 July 2025, while Enterprise continues. This limits its suitability as a directly reproducible student baseline. The FAQ says Enterprise retrieval uses Sourcegraph Search rather than embeddings.

**Study / solution 3:** RepoQA evaluates long-context code understanding through natural-language function search.

**Source / citation:** Liu et al. (2024), [R5].

**Key limitation (task mismatch, our assessment):** Function search does not directly measure beginner installation explanations, contribution guidance or citation-grounded documentation answers. It informs evaluation design but is not our benchmark.

## Engineering Gap / Limitation

**Gap / Limitation:** This project needs a small, reproducible documentation assistant that keeps repositories and versions separate, explains instructions for beginners, cites the supporting document sections and declines unsupported questions. Existing products and research provide relevant capabilities, but do not establish performance on this project's fixed eight-document beginner benchmark. This is our proposed engineering and evaluation gap, not a claim that all existing assistants lack these features or that RAG is novel.

## Initial Project Objectives (2-3)

- **O1:** To design a bounded documentation dataset and processing specification covering exactly three repositories and eight selected files, with source URLs, commit IDs, licenses and section-level provenance recorded for every file.
- **O2:** To develop, during the semester, a simple web RAG prototype supporting repository selection, natural-language Q&A, two-repository installation comparison, source references and explicit abstention when evidence is insufficient; demonstrate each function with at least one acceptance case.
- **O3:** To evaluate the prototype against a BM25 keyword retrieval baseline on a frozen 30-question test set, targeting Recall@5 >= 0.85, fully correct answers >= 80%, citation accuracy and groundedness >= 90%, and p95 response latency <= 15 seconds under the protocol in the evaluation plan. These are preliminary targets, not achieved results.

## Target Users

Primary users are university computing students and beginner developers exploring FastAPI, Streamlit and scikit-learn for coursework or an initial open-source contribution. Initial support is English-language documentation and questions. The system explains selected documentation; it does not infer undocumented implementation details.

## Data Sources (at least 2)

**Source 1:** FastAPI - D1-D3: README, tutorial entry page with installation guidance, and contribution entry page.
**Source 2:** Streamlit - D4-D5: README (including installation and running) and contribution guide.
**Source 3:** scikit-learn - D6-D8: README, installation guide and contribution guide.

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

All eight selected files were retrieved successfully (HTTP 200) on 22 October 2026. URLs are pinned to observed commit IDs, so later branch changes will not silently alter the planned collection. This is an initial source selection, not a completed ingestion pipeline. See [source manifest](../data/source_manifest.json) for hashes and exact metadata.

- **fastapi/fastapi: MIT** - [verified repository license](https://raw.githubusercontent.com/fastapi/fastapi/4bdfbe4513084b19e22421ce1f916d8c1ac462a0/LICENSE).
- **streamlit/streamlit: Apache-2.0** - [verified repository license](https://raw.githubusercontent.com/streamlit/streamlit/f478c9783be8099f1d394d02dea77bd0697d93ea/LICENSE).
- **scikit-learn/scikit-learn: BSD-3-Clause** - [verified repository license](https://raw.githubusercontent.com/scikit-learn/scikit-learn/718eedb7af8678255de080d4748d9f67e321ba41/COPYING).

Week 1 commits only source metadata and original planning text, not copies of upstream documents. Repository licenses were inspected; before any later redistribution, preserve applicable copyright and permission notices for MIT, BSD conditions/disclaimer for BSD-3-Clause, and Apache license, applicable notices and change notices for Apache-2.0. Check file-specific exceptions and any applicable NOTICE material; do not assume a linked external website has the repository's license. If uncertain, retain the URL only. External images, linked pages, code files and included snippets in other files are not automatically collected.

FastAPI D3 delegates detailed development instructions to an external guide; answers must acknowledge that boundary. Streamlit D4 records a pause on external pull requests; answers must reflect the pinned policy instead of giving generic contribution advice. No third-party document has been added to this repository.

## Similar to EduAdvisor

Both are bounded, document-grounded assistants for students. Both propose loading, cleaning, chunking, embedding, retrieval, an LLM, source references, input/output checks and objective evaluation. GitHub will record requirements, data provenance, architecture decisions, prompts, evaluation evidence and subsequent changes across the semester.

## Different from EduAdvisor

RepoLens uses public software documentation instead of university course and graduation PDFs. Questions concern repository purpose, technologies, prerequisites, installation and contributions; comparisons may require evidence from two selected repositories. Main risks include incorrect technical instructions, mixed repository versions and malicious text inside retrieved documentation. It does not provide academic enrolment decisions or reproduce the EduAdvisor example's observations or measured results.

## Responsible AI Risks (at least 2)

| Risk | Potential harm and affected users | Planned mitigation and verification |
|---|---|---|
| 1. Hallucinated or outdated instructions | Beginners may waste time, install incompatible packages or follow incorrect commands. | Ground factual claims in retrieved sections; display commit/version and citations; preserve command syntax; abstain on missing evidence; manually check installation cases and unsupported questions. No commands run automatically. |
| 2. Prompt injection in public documentation | Malicious retrieved text could redirect the model, solicit secrets or suggest harmful actions. | Treat documents as untrusted evidence rather than instructions; use an allowlist, separate system instructions from retrieved text, disable execution/tools and test adversarial snippets. |
| 3. Repository confusion and uneven coverage | Advice for one project may be applied to another; longer guides may dominate retrieval. | Filter by repository, label both sides of comparisons, evaluate per repository and topic, and state when a selected file lacks details. |
| 4. Privacy and source rights | Questions might contain credentials; excessive excerpts or copied assets may violate source conditions. | Warn against entering secrets; keep keys outside Git and browser code; avoid raw query logging by default; record provenance and licenses; use concise sourced paraphrases and exclude unreviewed third-party content. |

## Additional Planning: Semester Scope

**In scope:** exactly the eight allowlisted public Markdown/reStructuredText files; text extraction, cleaning and heading-aware chunking; embeddings and semantic retrieval; plain-language answers and repository/document/section citations; a simple web interface; comparisons between two supported repositories; answer-quality, retrieval, abstention and latency evaluation.

**Out of scope:** full-codebase analysis, arbitrary crawling, private repositories, executing downloaded code, automatically installing dependencies, autonomous repository modification, pull requests and complex multi-agent workflows. A feature-documentation question is answered only if its evidence appears in the selected files; otherwise provide a source entry point and explain the evidence gap. Linked content and referenced include files are not implicitly in scope.

**Proposed approach:** selected files -> parse Markdown/RST -> clean while retaining commands/headings -> chunk -> embed/index with repository, path, commit, heading and source URL -> repository-filtered retrieval -> context-grounded LLM -> citation/scope checks -> simple web UI. A comparison retrieves separately for each requested repository before synthesis. Model, embedding provider, chunk size and vector store are provisional; select them after a small development experiment and budget check. There is no running application in Week 1.

**Why AI:** paraphrased questions may not match exact words; semantic retrieval can find related passages, while generation can combine multiple documents and explain technical steps. BM25 keyword retrieval remains a necessary baseline. Measure rather than assume improvements; use simple retrieval alone if generation adds no reliable value.

**Semester sequence:** Week 1 framing and repository preparation; next refine requirements and freeze benchmark sources; then parsing/retrieval, grounded generation, interface/guardrails, and final evaluation/documentation. Adjust dates to the course schedule. Prioritise one vertical slice before adding comparisons.

## Additional Planning: Initial Evaluation

See [evaluation plan](../evaluation/plan.md) for a 36-question development/test design, reference-answer and passage annotation, metric definitions, preliminary targets and repeatable timing protocol. No benchmark results are claimed.

## References

- **[R1]** Steinmacher, I., Graciotto Silva, M. A., Gerosa, M. A., & Redmiles, D. F. (2015). *A systematic literature review on the barriers faced by newcomers to open source software projects*. Information and Software Technology, 59, 67-85. [DOI](https://doi.org/10.1016/j.infsof.2014.11.001); [accessible university abstract and bibliographic record](https://experts.nau.edu/en/publications/a-systematic-literature-review-on-the-barriers-faced-by-newcomers/).
- **[R2]** Chen, J., Zhao, K., Liu, J., Peng, C., Liu, J., Zhu, H., Gao, P., Yang, P., & Deng, S. (2025). *CoReQA: Uncovering Potentials of Language Models in Code Repository Question Answering*. arXiv preprint 2501.03447. [Paper and abstract](https://arxiv.org/abs/2501.03447).
- **[R3]** GitHub. (n.d.). *Application card: GitHub Copilot Chat*. [Official documentation](https://docs.github.com/en/copilot/responsible-use/chat). Accessed 22 October 2026.
- **[R4]** Sourcegraph. (n.d.). *Cody FAQs*. [Official documentation](https://sourcegraph.com/docs/cody/faq). Accessed 22 October 2026.
- **[R5]** Liu, J., Tian, J. L., Daita, V., Wei, Y., Ding, Y., Wang, Y. K., Yang, J., & Zhang, L. (2024). *RepoQA: Evaluating Long Context Code Understanding*. arXiv preprint 2406.06025. [Paper and abstract](https://arxiv.org/abs/2406.06025).

