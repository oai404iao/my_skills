# Common anti-patterns in prompts, schemas, and tests

The following are illustrative counterexamples distilled from code-review issues, not measured model results. They distinguish generation guidance, interface contracts, and effectiveness validation without categorically condemning wording or testing tools. Review tasks only report issues; changes must stay within the authorized scope, especially without unilaterally changing business inference rules.

## 1. Addressing the wrong audience: Developer notes written to the model

**Counterexample**

```json
{
  "type": "string",
  "description": "Suggested length: 60–180 characters; this length is only generation guidance, not a validation condition."
}
```

**Problem:** The second half explains server-side validation rather than helping the model complete the task; the first half specifies length alone, not what the field should convey. Model-visible schemas should not serve as maintenance notes.

**Fix:** For example, change it to "Summarize the most important known facts and limitations of the assessment; state that information is insufficient when there is no evidence. Suggested length: 60–180 characters." Put validation policy in developer documentation, and express hard limits through schema keywords supported by the target platform and local validation. Necessary task boundaries (such as generating text only, not HTML) remain valid instructions, not developer notes to remove.

**Verification:** Check schema keywords and actual acceptance/rejection of boundary inputs against the design, rather than requiring descriptions to contain "suggested" or "not a validation condition."

## 2. Wording mistaken for semantics: Proving behavior by the presence of a sentence

**Counterexample**

```python
assert "Do not invent dates" in prompt
assert "reduce the font size" in prompt
```

Then name the tests "the model will not invent dates" or "the poster meets readability requirements."

**Problem:** Opposite instructions can contain the same words: both "Do not reduce the font size" and "Please reduce the font size" pass the second assertion; equivalent rewordings may fail. These tests constrain the author's wording without validating model behavior.

**Fix:** Template tests check interpolation and message roles; semantic requirements need evaluation on representative inputs/outputs. For example, when no date is provided, check whether the model keeps it unknown; poster readability requires checking actual generated results. Without running a model, explicitly state that semantic effects are unverified rather than substituting keyword assertions.

**Boundary:** `Contains` is not inherently wrong. Checking that known variables were inserted or sensitive fields were not sent can be a reasonable deterministic test; the problem is substituting the presence of natural-language fragments for semantic compliance.

## 3. Exceeding test capabilities: Treating structural and workflow passes as effectiveness guarantees

**Counterexamples**

- The prompt has `<input>` and `</input>`, so claim "prompt injection has been prevented."
- Schema validation passes, so claim "facts are correct."
- The prompt says "check yourself before output," so claim "reliable quality validation exists."
- A fake LLM returns the correct category, so claim "the prompt classifies accurately."

**Problem:** At most, these prove tags exist, structure is valid, an instruction exists, or the program can handle the given category—not the claimed behavior. Internal self-checking can be generation guidance but is not an observable validator.

**Fix:** Specify each test's inputs, components actually executed, and observable assertions. Use deterministic tests for programmatic safeguards and independent evaluations for model behavior; security guarantees also require code boundaries such as permission controls. Do not inflate evidence through test names, documentation, or completion reports.

## 4. Contradictory fixtures: Injecting affirmative answers into no-data scenarios

**Counterexample**

```text
Input facts: The device list is empty; service records are empty.
Fake LLM: Two offline devices were found; three services were completed this period.
Test: Checks only that the page contains "No records"; passes.
```

**Problem:** The page may display both an empty-data notice and fabricated conclusions. Contradictory test data hides defects; one shared "successful answer" does not suit every scenario.

**Fix:** Ordinary workflow tests use scenario-consistent fakes and check the factual data sent to the model and actual rendered results. If deliberately injecting an incorrect model answer, make it a negative case and explain whether it tests rejection, fallback, or a currently unprotected boundary—not a normal success path. Fakes can prove orchestration behavior, not that real models remain factually consistent.

## 5. Contracts maintained in multiple places: Conflicting rules, examples, schemas, and validators

**Counterexample**

```text
Prompt: Do not output reason.
Schema: reason is a required string.
Example: Includes reason.
Local validation: reason is optional.
```

Another common example: rules require omitting missing fields, but examples output empty objects.

**Problem:** There is no single executable output contract. Adding more "strictly comply" instructions only amplifies conflicts; examples also steer the model away from written rules.

**Fix:** First establish business semantics and a contract expressible by the target platform, then align requiredness, types, empty values, enums, conditional relationships, and examples. Schemas govern shape, prompts govern semantics, and local validation handles necessary business relationships; avoid maintaining unnecessary details redundantly.

**Verification:** Run positive and negative cases through the actual schema and local validation, checking expectations agree; manually review prompt/example semantics. Do not prove contract consistency with matching keywords again. See [Structured responses](../interfaces/structured-output.md).

## 6. Unsupported completion: Encouraging guesses for specificity, completeness, or quotas

**Counterexamples**

- "If the user did not provide a deadline, add one based on urgency."
- "Regardless of how much material exists, always provide five issues and five recommendations."
- "You must mention a particular risk category and give a handling frequency."

**Problem:** The model may state guesses as facts, manufacture issues to meet quotas, or offer inapplicable recommendations. "Specific" is not factual evidence, and stronger wording cannot supply missing information.

**Fix:** Extraction tasks preserve unknowns; recommendation tasks first confirm whether the business authorizes inference and clearly distinguish known facts from suggested values. Allow fewer items when supported and empty arrays when no additional recommendations exist; necessary fixed output sizes require a defined way to express insufficient evidence, not invented filler.

**Verification:** Cover missing, ambiguous, inapplicable, and conflicting-source cases; ask business stakeholders first when inference permissions require a decision. Do not categorically remove approved recommendation features merely because "inference" appears.

## 7. Constraints without consumers: Turning format preferences into mandatory contracts

**Counterexample**

```text
Output must be single-line compact JSON, with keys strictly ordered A, B, C.
```

Yet the actual consumer is an ordinary JSON parser that ignores whitespace and key order, and tests lock in whether the prompt contains "single-line" and "in order."

**Problem:** Requirements irrelevant to task correctness add maintenance burden; "JSON only" does not additionally require a single line or fixed key order.

**Fix:** Ask of each constraint, "Who consumes it, and what breaks if it is unmet?" Remove unsupported constraints; if a streaming protocol, display order, signature, or legacy compatibility contract genuinely depends on it, retain it and test actual consumption behavior, not merely instruction wording.

## Retain useful tests; do not replace judgment with another slogan

| Test | What it can prove | What it cannot justify claiming |
| --- | --- | --- |
| Interpolation, message roles, field projection | Data enters intended locations without mixing other roles or fields | The model necessarily resists injection |
| Prompt SHA matches file | Audit references accurately track actual bytes | The prompt is more effective |
| Golden snapshot | Displays and constrains explicitly accepted rendering/byte changes | Copy is semantically correct and needs no review |
| Parsing and positive/negative schema cases | Types, fields, formats, and actual constraints work as expected | Content is true or reasonable |
| Fake LLM and side-effect tests | Error handling, mapping, and writes for a given response | The model can derive that response |
| Real-model held-out-sample evaluation | Observations for specified models, settings, and samples | Results hold for all inputs and future models |

Report reviews as "counterexample → actual impact → responsible layer → verification," distinguishing definite defects, coverage gaps, and business trade-offs. Do not delete all string assertions or snapshots, or create mirror-text tests for wording-only changes. See [Evaluation and iteration](evaluation.md) for recording effectiveness evaluations and unverified items.
