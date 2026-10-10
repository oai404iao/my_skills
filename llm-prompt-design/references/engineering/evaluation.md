# Evaluation and iteration: Validate effectiveness on the target task

First fix the model/API, input set, tool permissions, image references, sampling settings, and downstream decision rules; record the current prompt as the baseline. Change only one class of variables per round (such as label boundaries or examples, rather than changing both model and schema), and compare pass rates, latency, and cost; for stochastic generation tasks, use multiple outputs to observe stability where possible. Without running a real model, write "expected improvement," not "improved by 30%."

## Prepare representative cases

- Normal, missing, ambiguous, overlapping-category, long-input, conflicting-source cases, and untrusted data containing "ignore the rules"; do not put test-set answers directly into few-shot examples.
- If samples contain user privacy, trade secrets, or third-party images, handle authorization, redaction, and retention under the target project's policies; do not automatically upload production data for comparisons.
- Specify reviewers, acceptable error, and decision criteria; retain failure samples rather than showcasing only the best run.

| Task | Checkable metrics | First checks on failure |
| --- | --- | --- |
| Classification/extraction | Per-category accuracy, incorrect/missing fields, incorrectly filled unknowns, schema compliance | Category definitions, boundary cases, schema and input sources |
| Summarization/source-grounded question answering | Key-fact coverage, fabrication rate, citation support per claim, appropriate abstention | Missing/stale sources, retrieval recall, information lost in segmentation |
| Writing/translation/code | Fact/terminology consistency, audience fit, tests and project-contract compliance | Missing brief details, terminology conflicts, tests not run |
| Tool calling | Accuracy of calling/not calling, valid arguments, authorization before writes, failure recovery | Overlapping descriptions, missing arguments, server-side validation and error semantics |
| Image generation/editing | Subject and count, composition whitespace, exact text accuracy, identity/local preservation, human usability rate | Whether references were actually supplied, parameter support, content/composition conflicts |

Record comparisons as: `task/sample version → prompt/schema version → model and settings → result → failure type → next single-variable change`. Batch evaluation is not a prerequisite for ordinary one-off creation; with only one sample, perform targeted checks rather than claiming statistical significance. Visual images often require blind human review and item-by-item checks; image API output parameters may be more effective than adding adjectives. After deployment, if allowed, monitor input-distribution changes and regressions from model/API upgrades.

## What tests prove

Distinguish template rendering, parsing/schema, local business logic, and real model behavior. Passing the earlier layers cannot replace effectiveness evaluation of the last; without authorization to run a model, report verified boundaries and unverified items rather than using "the prompt contains a particular sentence" as behavioral evidence.

For wording lock-in, contradictory fake responses, and the boundaries of valid tests, see [Common anti-patterns and counterexamples](anti-patterns.md). Do not delete all snapshot or fake tests because brittle assertions were found, and do not create mirror-text tests for wording-only changes.

See [Anthropic's evaluation-first guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview), [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering), and [OpenAI image-prompt checking guidance](https://developers.openai.com/api/docs/guides/image-prompting). Task samples and metrics are this skill's engineering synthesis, not results of experiments already run.
