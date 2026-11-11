# Running and Submitting the RepoLens Week 3 Lab

The repository contains the notebook, required planning/evidence files, prepared exports and manifests for Topic 3. The saved notebook outputs were produced by a **real local Jupyter kernel**, not by Google Colab. The command-line pipeline and notebook independently produced byte-identical exports; 11 data-contract tests passed.

## Run in Google Colab

1. [Open the notebook in Google Colab](https://colab.research.google.com/github/dnarrayana08/ai-engineering-RepoLens/blob/main/notebooks/week3_pipeline.ipynb).
2. Sign in with your own Google account if asked. Save a copy if Colab opens the GitHub notebook read-only.
3. Select **Runtime > Run all**. Read the first environment output: a Colab execution must say Google Colab. No model key, paid model service or package installation is required by this notebook.
4. Inspect the representative D1/D4 text, chunk comparison, validation and two-run PASS output. Do not assume successful execution merely from old saved outputs. If a download fails, check network access; never substitute a moving branch or ignore a hash mismatch.
5. Use File > Download > Download .ipynb to save the **actually executed** notebook. The last code cell produces `week3_data_exports.zip`; uncomment its two download lines and run that cell, or download the ZIP through Colab's Files panel.
6. The ZIP includes prepared data, both manifest types, original source-selection metadata, rights review, attribution and retained upstream license/notice files. It excludes raw data. Keep attribution/notices with derived text.
7. If replacing the local-run notebook/evidence in GitHub with your Colab run, preserve the source code and selected configuration, inspect the diff, and label the new execution honestly. Do not manually edit local outputs to say Colab.

Files in `/content` are temporary. Save the notebook and exports before disconnecting or resetting the runtime. If a reset occurs, run all cells again in order rather than running a late cell with missing variables.

## Required Week 3 Files

| Artifact | Repository location |
|---|---|
| Runnable notebook | [notebooks/week3_pipeline.ipynb](../notebooks/week3_pipeline.ipynb) |
| Data inventory | [docs/week3_data_inventory.md](week3_data_inventory.md) |
| Pipeline diagram | [docs/week3_pipeline_diagram.png](week3_pipeline_diagram.png) |
| Pipeline decisions | [docs/week3_pipeline_decisions.md](week3_pipeline_decisions.md) |
| Part B export | [data/processed/prepared_text.jsonl](../data/processed/prepared_text.jsonl) |
| Part B lineage | [data/week3_manifest.json](../data/week3_manifest.json) |
| Part C outputs / run manifest | [data/pipeline_v1/documents/](../data/pipeline_v1/documents/) |
| Progress | [README.md](../README.md) |

The editable [Draw.io pipeline source](week3_pipeline_diagram.drawio), [test report](../data/pipeline_v1/documents/test_report.json) and [verification record](week3_verification.md) are additional supporting artifacts.

## Optional Local Verification

The student workflow uses Colab. If you also have Python 3.10+ locally, the pipeline itself has no external dependencies:

```bash
python src/week3_pipeline.py
python -m unittest discover -s tests -v
```

The first command downloads only approved pinned sources, validates them, prepares Part B, runs Part C twice and compares outputs. `--offline` is available once the eight raw inputs have been acquired. The unit tests require those raw inputs; run the pipeline first. Notebook authoring/execution tools used to verify the delivered notebook locally are not required to run the notebook in Colab.

## Final GitHub and Portal Check

Verify the required notebook, docs, manifests, prepared exports and licenses are visible in the same GitHub repository used in Weeks 1-2. Open the notebook and diagram, not just their folder listing. The code prepares 350 chunks from 8 documents; it does not build embeddings, train a model or demonstrate chatbot accuracy.

Submit the real repository URL through the Topic 3 course-portal submission if required by your lecturer:

https://github.com/dnarrayana08/ai-engineering-RepoLens

Portal submission and the lecturer's acceptance of any locally executed evidence cannot be inferred from a GitHub push. Complete the Colab run required by the lab and keep the portal confirmation yourself; neither account login nor portal submission is claimed in this delivery.
