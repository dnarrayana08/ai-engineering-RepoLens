# RepoLens Week 2 Requirements Specification

Version 1.0 | Planning date 26 October 2026 | Status: proposed specification; not implemented or validated.

This specification refines the Week 1 RepoLens scope into observable behaviour and measurable acceptance criteria. RepoLens is a semester engineering project for documentation-grounded assistance; comparable general assistants already exist. Its practical value must be established with evidence, not inferred from adding an AI interface.

## Section 0 Project Framing and Application Scope Checkpoint

| Framing element | RepoLens specification |
|---|---|
| Problem Evidence | Students and beginner developers need help locating and interpreting unfamiliar repository documentation. Newcomer research identifies documentation and starting-point barriers [R1]; CoReQA reports repository-QA difficulties for the evaluated baselines [R2]. These motivate a bounded test, not a claim that RepoLens will solve onboarding. |
| Existing Approaches | GitHub Copilot Chat/Spaces provides contextual coding assistance and curated materials [R3]. Cody retrieves relevant code context through Sourcegraph [R4]. RepoQA evaluates natural-language function search [R5]. A general assistant supplied with the same documents is also a legitimate alternative. No novelty claim is made. |
| Project / Engineering Gap | The practical gap is a reproducible beginner workflow with an explicit source snapshot, repository-specific evidence, inspectable citations and an evaluated abstention policy. Existing capabilities do not establish whether our implementation meets these requirements. Product usefulness and improvement over simpler search remain hypotheses. |
| Objective O1 | To design a bounded documentation dataset and processing specification covering exactly three repositories and eight selected files, with source URLs, commit IDs, licenses and section-level provenance recorded for every file. |
| Objective O2 | To develop, during the semester, a simple web RAG prototype supporting repository selection, natural-language Q&A, two-repository installation comparison, source references and explicit abstention when evidence is insufficient; demonstrate each function with at least one acceptance case. |
| Objective O3 | To evaluate the prototype against a BM25 keyword retrieval baseline on a frozen 30-question test set, targeting Recall@5 >= 0.85, fully correct answers >= 80%, citation accuracy and groundedness >= 90%, and p95 response latency <= 15 seconds under the protocol in the evaluation plan. These are preliminary targets, not achieved results. |
| Intended Users | University computing students and beginner developers exploring FastAPI, Streamlit and scikit-learn. English questions and documents in V1. |
| Supported Tasks | Ask about purpose, technologies, installation/running, prerequisites, contribution guidance and documentation locations; request a two-repository installation comparison; inspect sources; receive a bounded explanation or an explicit limitation. |
| Information / Knowledge Domain | Exactly eight pinned Markdown/RST documents across three public software repositories. Source links are below and full metadata remains in data/source_manifest.json. Linked pages, included files and code are not automatically admitted. |
| Operating Context | A small single-user web prototype used for coursework or exploration, with a prepared read-only documentation collection. Initial evaluation uses one concurrent request, fixed model configuration and a warmed knowledge store. Network access may be needed for a model service; no SLA or production deployment is assumed. |
| Important Constraints | One-semester individual project; preserve the eight-file source boundary; no paid resources provisioned now; proposed variable inference cap US$1/100 queries; protect keys outside browser/Git; comply with source conditions before copying. Technologies remain provisional. All acceptance thresholds are design targets. |
| Explicit Out-of-Scope Tasks | Whole-codebase analysis; arbitrary crawling; private repositories; executing downloaded code; automatic installation; autonomous edits/PRs; multi-agent workflows; undocumented algorithm explanations; decisions requiring guarantees that the system cannot support. |
| Evaluation Focus | Can this bounded assistant provide correct, understandable, traceable answers with appropriate abstention at acceptable latency and cost? Does semantic knowledge access improve evidence recall on paraphrases over BM25, and does generation add useful explanation? Compare fairly; do not assume it beats general assistants or search. |

### Source collection

| Source ID | Repository | Pinned document URL |
|---|---|---|
| D1 | fastapi/fastapi | [README.md](https://raw.githubusercontent.com/fastapi/fastapi/4bdfbe4513084b19e22421ce1f916d8c1ac462a0/README.md) |
| D2 | fastapi/fastapi | [docs/en/docs/tutorial/index.md](https://raw.githubusercontent.com/fastapi/fastapi/4bdfbe4513084b19e22421ce1f916d8c1ac462a0/docs/en/docs/tutorial/index.md) |
| D3 | fastapi/fastapi | [docs/en/docs/contributing.md](https://raw.githubusercontent.com/fastapi/fastapi/4bdfbe4513084b19e22421ce1f916d8c1ac462a0/docs/en/docs/contributing.md) |
| D4 | streamlit/streamlit | [README.md](https://raw.githubusercontent.com/streamlit/streamlit/f478c9783be8099f1d394d02dea77bd0697d93ea/README.md) |
| D5 | streamlit/streamlit | [CONTRIBUTING.md](https://raw.githubusercontent.com/streamlit/streamlit/f478c9783be8099f1d394d02dea77bd0697d93ea/CONTRIBUTING.md) |
| D6 | scikit-learn/scikit-learn | [README.rst](https://raw.githubusercontent.com/scikit-learn/scikit-learn/718eedb7af8678255de080d4748d9f67e321ba41/README.rst) |
| D7 | scikit-learn/scikit-learn | [doc/install.rst](https://raw.githubusercontent.com/scikit-learn/scikit-learn/718eedb7af8678255de080d4748d9f67e321ba41/doc/install.rst) |
| D8 | scikit-learn/scikit-learn | [doc/developers/contributing.rst](https://raw.githubusercontent.com/scikit-learn/scikit-learn/718eedb7af8678255de080d4748d9f67e321ba41/doc/developers/contributing.rst) |

The collection and repository licenses were checked on 22 October 2026; those source snapshots are retained rather than silently refreshed. The eight source documents are not copied into this Week 2 package. FastAPI's selected contribution entry point delegates detailed development guidance to an external page; that page is not in scope. Preserve Streamlit's contribution-policy restriction as recorded in the pinned README. Repository licenses and source hashes remain in the Week 1 manifest. References below were rechecked on 26 October 2026.

### Objective traceability checkpoint

- O1 leads to FR2/FR3/FR7, NFR3 and RAI1/RAI5, evaluated through C01/C03/C12.
- O2 leads to FR1-FR6 and RAI2-RAI4, evaluated through the feature, clarity, boundary, injection and privacy checks.
- O3 leads to NFR1-NFR5 and the evaluation protocol; all reported outcomes must distinguish measured results from the present targets.

## Section 1 Functional Requirements

| ID | Objective | Requirement | Scope Boundary |
|---|---|---|---|
| FR1 | O2 | The system shall let the user select one supported repository for a question or two supported repositories for an installation comparison. | Only FastAPI, Streamlit and scikit-learn; no arbitrary URL or private-repository access. |
| FR2 | O1, O2 | The system shall answer English questions about repository purpose, documented technologies, installation/running, prerequisites, contributions and documentation locations using the selected documents. | State when a detail is absent; do not infer implementation behaviour from unexamined code. |
| FR3 | O1, O2 | The system shall attach verifiable references to material factual claims, identifying repository, document, section and fixed commit URL. | Do not fabricate source paths or treat a link to an uncollected page as evidence for its unseen contents. |
| FR4 | O2 | The system shall compare documented installation/prerequisite information for two selected repositories and label the evidence for each separately. | If one side lacks evidence, explain the partial answer rather than inventing a complete comparison. |
| FR5 | O2 | The system shall explain when a question lacks sufficient evidence or falls outside scope, and provide a relevant selected-source entry point when available. | Decline execution, dependency installation, private access, repository edits and pull-request creation; ask a short clarifying question when repository or intent is ambiguous. |
| FR6 | O2 | The system shall present beginner-readable explanations, expand unfamiliar technical terms when needed and preserve the syntax of any quoted commands. | Display commands as documentation guidance only; never execute them or claim they were tested. |
| FR7 | O1 | The system shall let the user inspect the supported source list, repository commit, collection date and documented coverage limits. | A snapshot is not a promise of the latest upstream instructions; display when a detailed guide is outside the collection. |

FRs specify visible outcomes rather than a particular model, database or interface framework. The evaluation document supplies acceptance scenarios for FR1-FR7.

## Section 2 Non Functional Requirements

| ID | Objective | Quality Attribute | Requirement | Measurement Method | Metric | Threshold |
|---|---|---|---|---|---|---|
| NFR1 | O3 | Performance | The system shall complete interactive answers within the proposed latency budget. | Time 30 test questions three times after one excluded warm-up, one concurrent request, no answer cache; include query processing, knowledge access, model generation and output checks. | p50 and p95 end-to-end completion latency; report failures separately and as failed trials. | p50 <= 8 s and p95 <= 15 s; deadline 30 s per trial. |
| NFR2 | O3 | Correctness | The system shall answer supported questions consistently with their annotated source evidence. | Human-grade the 24 answerable test questions using the 0/1/2 correctness rubric. Use the median score across three runs per question; publish all run scores. | Fully correct question rate (median score 2). | >= 80% = at least 20/24; report repository/topic breakdowns. |
| NFR3 | O1, O3 | Retrieval quality | The system shall expose enough supporting evidence to answer supported questions. | Annotate required evidence units independently of chunking, then inspect top 5 evidence passages for each of 24 answerable questions; accept declared equivalent passages. | Macro-average Recall@5 across questions. | >= 0.85; compare with BM25 under the same retrieval budget. |
| NFR4 | O3 | Cost | The system shall keep variable inference expenditure within a student-scale evaluation budget. | Record billable model/embedding usage for the 90 test trials, price it at the actual provider rates recorded on the run date, divide by attempted trials and multiply by 100. Include retries; record initial indexing separately. | Variable API cost per 100 attempted queries in USD. | <= US$1.00 per 100 queries; proposed budget cap, not a statement of current provider pricing. |
| NFR5 | O2, O3 | Reliability | The system shall return a clear controlled message on unavailable knowledge, a failed model call or a timeout, without claiming a successful answer. | Inject 10 failures: 3 unavailable knowledge cases, 3 model errors, 4 timeouts; inspect UI and diagnostic output. | Controlled-error response rate and maximum time to a terminal status. | 10/10 controlled responses, each within 30 s; 0 false success messages. |

**Threshold rationale:** Twenty-four answerable questions are manageable for manual review; 20 correct answers is an initial semester prototype target and does not imply suitability for consequential automated decisions. A 15-second p95 target allows source retrieval and a short explanation; a 30-second deadline prevents indefinite waiting. The cost cap is a proposed project constraint that will be revisited if model selection cannot meet it. Targets may be revised using development evidence before the held-out set is opened; record any change and reason.

## Section 3 Responsible AI Requirements

| ID | Objective | Responsible AI Risk | Requirement | Measurement Method | Metric | Threshold |
|---|---|---|---|---|---|---|
| RAI1 | O1, O2, O3 | Misinformation and misleading citations | The system shall support factual claims with correct source passages and disclose insufficient evidence. | Human-check all claim-citation pairs and all material claims across the 72 generated answers to answerable questions; validate source IDs and commits. | Citation accuracy; groundedness/citation coverage; source-ID/commit validity. | Accuracy >= 90%; groundedness >= 90%; source-ID/commit validity 100%. Abstentions do not earn a perfect groundedness score. |
| RAI2 | O2, O3 | Scope and capability misunderstanding | The system shall decline unsupported or prohibited requests and explain the relevant limit without pretending to act. | Run 6 held-out unsupported cases (4 evidence gaps, 2 prohibited-action/private-access cases); inspect 24 answerable cases for false abstention. | Appropriate abstention/refusal rate; action-case refusal; false abstention rate. | At least 5/6 appropriate outcomes; both prohibited-action cases refused in every run; false abstention <= 2/24 by majority outcome. |
| RAI3 | O2, O3 | Prompt injection and unsafe actions | The system shall treat retrieved documents as evidence rather than instructions and provide no execution or repository-write capability. | Use 20 separate synthetic injection cases in retrieved text, including override, credential request, fake citation and command execution attempts; inspect outputs and available tool permissions. | Attack success count; enabled execution/write tools. | 0/20 attacks succeed in the defined set; 0 execution/write tools. This is bounded test evidence, not proof against every attack. |
| RAI4 | O2, O3 | Privacy and secret exposure | The system shall block detected credential-like input before any external model call and keep raw user questions out of persistent logs by default. | Use 20 synthetic credential cases and inspect captured outgoing payloads/logs; include a case that evades the chosen detector and record it as a failure rather than claiming universal protection. | Synthetic secret transmissions; persistent raw question records; controlled warning responses. | 0 transmissions and 0 raw question records for the 20 cases; 20/20 controlled warnings. Detector limits must be documented. |
| RAI5 | O1, O2 | Source rights and repository/version confusion | The system shall admit only the eight reviewed documents with provenance metadata and preserve repository/version identity through answers. | Audit source manifest and admitted collection; test 6 comparisons for source attribution and use 4 unallowlisted-source attempts. Review notices before copying any upstream content. | Complete source records; rejected unapproved additions; correct repository/version labels. | 8/8 records complete; 4/4 unapproved additions rejected; 6/6 comparisons labelled correctly in every run; no unreviewed redistribution. |

**Bounded assurance:** Source links do not by themselves prove semantic support, secret detectors are incomplete, and prompt-injection tests cannot prove universal resistance. Keep human review, visible limitations and disabled execution as independent controls. Evaluate answer quality by repository and topic to expose uneven coverage; do not infer demographic fairness from a three-repository benchmark.

## Part A Reflection

RAI3, resistance to prompt injection, is the most difficult control to enforce reliably because useful documentation and malicious instructions are both natural-language text in the same retrieved context. A finite test set cannot cover all attack variations, and a model may follow an indirect instruction despite a system prompt. The design therefore combines source allowlisting, clear separation of evidence from system instructions, output checks and absence of execution/write tools. Report the observed attack success count and failures rather than claiming complete safety.

## Links to Other Deliverables

- [Evaluation criteria and protocol](week2_evaluation_criteria.md)
- [Architecture decisions and traceability](week2_architecture_decisions.md)
- [V1 architecture diagram](week2_architecture_v1.png)
- [Editable architecture source](week2_architecture_v1.drawio)

## References

- **[R1]** Steinmacher, I., Graciotto Silva, M. A., Gerosa, M. A., & Redmiles, D. F. (2015). *A systematic literature review on the barriers faced by newcomers to open source software projects*. Information and Software Technology, 59, 67-85. [DOI](https://doi.org/10.1016/j.infsof.2014.11.001); [accessible university abstract and bibliographic record](https://experts.nau.edu/en/publications/a-systematic-literature-review-on-the-barriers-faced-by-newcomers/).
- **[R2]** Chen, J., Zhao, K., Liu, J., Peng, C., Liu, J., Zhu, H., Gao, P., Yang, P., & Deng, S. (2025). *CoReQA: Uncovering Potentials of Language Models in Code Repository Question Answering*. arXiv preprint 2501.03447. [Paper and abstract](https://arxiv.org/abs/2501.03447).
- **[R3]** GitHub. (n.d.). *Application card: GitHub Copilot Chat*. [Official documentation](https://docs.github.com/en/copilot/responsible-use/chat). Accessed 26 October 2026.
- **[R4]** Sourcegraph. (n.d.). *Cody FAQs*. [Official documentation](https://sourcegraph.com/docs/cody/faq). Accessed 26 October 2026.
- **[R5]** Liu, J., Tian, J. L., Daita, V., Wei, Y., Ding, Y., Wang, Y. K., Yang, J., & Zhang, L. (2024). *RepoQA: Evaluating Long Context Code Understanding*. arXiv preprint 2406.06025. [Paper and abstract](https://arxiv.org/abs/2406.06025).

