# Non-`gen_image`: Reusable examples by task

The examples on this page are original **illustrative inputs**, not prompts measured to be optimal. For image OCR/visual question answering without image generation, also use extraction/question-answering approaches with the image as input. Read [Strategy selection](../strategy-selection.md) first; for machine-readable output, read [Structured responses](../interfaces/structured-output.md); for calling business tools, read [Tool contracts](../interfaces/tool-schema.md).

## 1. Classification: From vague intent to explicit decisions

The baseline "determine this ticket's type" lacks category boundaries. A **zero-shot approach** suits tickets with clearly defined categories:

```text
Choose one primary category for the ticket: billing (charges, invoices, refunds),
technical (feature errors, inability to use a feature), other (anything else or indeterminate).
If multiple requests occur without a primary request, choose other.
Decide only from <ticket>; do not infer account history.
<ticket>{{ticket_body}}</ticket>
```

The illustrative input "I was charged twice. How do I get a refund?" should yield `billing`. If "the page crashes when I request a refund" is often confused, a **few-shot approach** can add project-reviewed examples before the current input: `"The invoice name is wrong" → billing`, `"The page failed to load" → technical`, and a mixed case with no clear primary request labeled `other`. Examples must match category definitions, not just include easily distinguished positive cases.

**Choice and effects:** Start zero-shot; add few-shot examples only when many boundary cases fail. Expect fewer errors between similar categories, at the cost of more tokens and possible overfitting to examples. For acceptance, compare confusion matrices on held-out samples from each category and mixed cases; use a [Response schema](../interfaces/structured-output.md) when downstream code parses labels rather than relying only on "output one word."

## 2. Extraction: Make missing information explicit rather than inventing it

The baseline "organize this ticket for me" can generate names and identifiers that never appeared. Replace it with:

```text
Extract the explicitly stated order number and the original problem phrase from <ticket>.
If there is no order number, mark it unknown; do not guess from context or invent one.
<ticket>{{ticket_body}}</ticket>
```

For "Order A123 was charged twice," expect order number `A123` and problem evidence "charged twice"; "charged twice but no order number provided" should keep the order number unknown. Database writes require explicit `string | null` fields and validation; see the [Complete schema example](../interfaces/structured-output.md). **Effects and costs:** Constraining information sources helps reduce invented fields; it cannot automatically resolve ambiguous source text. Assess field accuracy, incorrect filling of missing values, and inducement by irrelevant text.

## 3. Source-grounded question answering: Query evidence instead of reciting general knowledge

The baseline "how many days does delivery to remote areas take?" invites guessed numbers when information is missing. Illustrative material (fictional, only demonstrating citations):

```text
Answer <question> using only <sources>. Give the corresponding source id for each fact.
If specific information is absent, say "The sources do not specify"; do not fill in days using general knowledge.
<sources>
  <source id="S1">Standard delivery usually takes 3–5 days.</source>
  <source id="S2">Estimated delivery times for remote areas are those shown at checkout.</source>
</sources>
<question>How many days does delivery to remote areas take?</question>
```

Expected: "The sources do not specify the number of days for remote areas; check the estimated time at checkout [S2]." **Choice and effects:** When sources are in context, directly limit the answer to them; when absent or time-sensitive, use authorized retrieval/read-only tools instead of adding more "be accurate" instructions. Source IDs aid checking, but a citation does not mean its source supports the conclusion; check support sentence by sentence and the rate of unsupported answers.

## 4. Summarization: Distinguish decisions, action items, and unresolved matters

The baseline "summarize the meeting" can turn proposals into approved actions. Replace it with:

```text
Using only <notes>, output three sections: Decisions, Action items, Unresolved.
Only explicitly agreed items belong in Decisions; mark missing action owners/deadlines as "Unspecified";
proposals under discussion belong in Unresolved. Preserve disputed points; do not invent commitments.
<notes>{{meeting_notes}}</notes>
```

Illustrative notes: "A proposed launching Friday; B said testing was needed first; nobody set a release date." Expect "Unresolved: launch date and testing plan," not "Decision: launch Friday." **Choice and effects:** Sections and decision rules reduce confusion about identities/statuses; long notes or cross-references among multiple speakers still require checking the original for omissions and considering boundary information lost in segmented summarization.

## 5. Writing, rewriting, translation: Control goals without fixing wording

```text
Write two canvas bag product descriptions for commuters, each 40–60 characters, in a plain tone.
Known facts: foldable, side pocket fits a water bottle. Do not add unprovided environmental certifications or weight-capacity figures.
Version A emphasizes storage; version B emphasizes easy access.
```

**Choice and effects:** Constrain creation with audience, purpose, facts, and dimensions to vary, with the expectation of more context-appropriate copy; add few-shot examples only when brand tone is hard to describe and approved samples exist. Compare product-fact errors, audience mismatch, and A/B differences. Translation is similar: specify the audience, glossary, and proper names not to translate; do not let "fluency" override numbers and names that must be preserved. When writing does not require machine parsing, do not force JSON merely for neatness.

## 6. Code and complex analysis: Turn acceptance into checkable items

```text
Implement function {{function_name}} according to the following interface contract; use the target repository's language and existing error conventions.
Inputs, return values, and boundaries: {{confirmed_contract}}.
Provide necessary tests for empty, normal, and invalid inputs.
If critical behavior is undefined, identify the gap; do not invent compatibility-breaking defaults;
do not claim tests passed when they were not run.
```

**Choice and effects:** Inspect actual repository contracts first, then cover boundaries with verifiable tests. Decompose only when the task has independently checkable extraction, generation, and validation stages and direct generation frequently fails; decomposition helps locate failures but adds invocation rounds and does not replace running tests. When external facts or repository contents are unknown, read/retrieve them rather than adding role titles to the model.

Measure the expected effects of these cases using [Evaluation and iteration](../engineering/evaluation.md); technique categories draw on [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering), the [Google prompt design notebook](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/prompts/intro_prompt_design.ipynb), and the [DAIR.AI guide](https://github.com/dair-ai/Prompt-Engineering-Guide). All ticket, delivery, and product content above is locally created illustrative material.
