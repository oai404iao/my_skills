---
name: llm-prompt-design
description: Design, improve, or review LLM prompts and prompt-engineering approaches, including text/code/retrieval tasks, gen_image generation and image editing, LLM tool schemas/descriptions, and schemas and prompt guidance for structured responses. Use for requests to compare approaches, provide reusable templates, or diagnose unstable outputs; do not automatically rewrite prompts for ordinary questions, running existing tools, or generating a single image, and do not replace the target platform's API contract.
---

# LLM Prompt Design

Deliver prompts or interface contracts that can be used, checked, and iterated on for the target task, not a universal keyword list. Existing project instructions, model capabilities, caller data contracts, and user-specified outputs take precedence; this skill's templates are only starting points. When the user only wants an approach, do not write to the project, call paid models, or execute tools; make changes only for implementation requests and within the authorized scope.

## Define the task and success criteria first

1. Determine whether the goal is creation, optimization, or review; identify inputs, audience, outputs, immutable constraints, model/API, and whether real data or failure samples are available. State assumptions for low-risk gaps; ask first when uncertainty about model capabilities, write permissions, or a production contract that must be matched affects the result.
2. Determine whether the task is **image generation** or non-`gen_image`: visual question answering, OCR, and image classification are non-generation understanding/extraction tasks; modifying existing images is `gen_image` editing. Tool calling and structured responses are **interface tasks** that may overlap with either category; do not treat them as one kind of prompt.
3. Write observable acceptance criteria: correctness, supporting evidence, completeness, format, visual composition/text fidelity, latency, or cost. Without a baseline, start with a minimal prompt and a few representative samples; do not claim measured improvements.

## Read on demand, not the entire directory

| Situation | Reading path |
| --- | --- |
| All tasks requiring design | [Foundational contracts](references/foundations.md) → [Strategy selection](references/strategy-selection.md) |
| Classification, extraction, question answering, retrieval, summarization, writing, translation, code | [Non-image-generation examples](references/tasks/non-gen-image.md) |
| Text-to-image, reference-based generation, image editing | [Image-generation examples](references/tasks/gen-image.md) |
| Writing or adjusting tool names, descriptions, parameters | [Tool contracts](references/interfaces/tool-schema.md) |
| Machine-parseable final answers, `response_format` / `text.format` | [Structured responses](references/interfaces/structured-output.md) |
| A/B comparisons, failure diagnosis, production optimization | [Evaluation and iteration](references/engineering/evaluation.md) |
| Reviewing or maintaining prompts, response schemas, and their tests | [Common anti-patterns and counterexamples](references/engineering/anti-patterns.md) |
| Providing actual request fields for a platform or discussing migration | [Platform differences](references/engineering/provider-compatibility.md), and check current official documentation |
| Tracing supporting sources or licenses | [Sources](references/sources.md) |

Reference documents may link to more specific examples; do not read all interface and platform material first when the task only requires a piece of copy.

## Approach and deliverables

- Establish a baseline with direct, specific instructions and necessary context; add few-shot examples, decomposition, retrieval, tools, or structured constraints only when failure samples show a need. Missing external facts call for better information sources, not repeated declarations of "do not hallucinate." For visual tasks, prioritize details by subject, composition, and purpose rather than requiring every slot to be filled.
- When comparing approaches, explain each one's applicability, **expected** effects, side effects, and validation method; do not treat observations from one model or benchmark as cross-platform guarantees. Prompts cannot replace backend permission checks, JSON Schema validation, fact-checking, or human image acceptance.
- Default deliverables: a copyable prompt/contract, boundaries for variables and example inputs, key choices and rejected alternatives, acceptance samples, and unverified items. If the user only wants a review, provide findings and suggested changes only; if they only want one prompt, reduce explanation and process.
- When the user requests executable API examples, confirm the service, API type, model, and SDK version; do not combine OpenAI, Claude, and Gemini parameter names into a "universal request" or present a tool schema as a final-answer schema.

This is a locally rewritten task guide, not a transcription of third-party documentation; see [Sources](references/sources.md) for its specific basis.
