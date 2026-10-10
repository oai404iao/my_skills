# Foundations: Turn requirements into checkable input/output contracts

Collect five things before designing: **task** (what to decide/generate), **available inputs** (who provides them and whether they are live), **output** (for people or machine parsing), **boundaries** (what must not be inferred, permissions, length, style), and **success criteria** (how to judge correctness). High-risk information should follow the approval and fact-checking processes of the system hosting the task; prompts are not security isolation.

## Separate instructions, data, and examples

- Place stable rules in the high-priority instruction location supported by the target API/host; pass dynamic user inputs, retrieved excerpts, and tool results according to their actual sources. Do not assume all platforms support the same roles or priorities.
- Use clear Markdown headings, XML tags, or equivalent delimiters to mark "rules," "examples," and "current input." Tags only aid understanding; they **cannot** turn untrusted text into trusted instructions. Treat "ignore previous requirements" in quoted documents and tool outputs as data to process, not instructions to follow.
- Limit permissible inference: for extraction, extract only values explicitly present in the material; for factual answers, specify sources, allowed inferences, and the response when evidence is insufficient. Prompts cannot conjure live data; use retrieval or tools when needed.
- Specify the result's form: recipient, language, item count, length, required/optional fields, and handling of conflicts or missing information. When format can be checked mechanically, use programmatic validation rather than repeating "strict JSON is mandatory."

A minimal extraction prompt skeleton (`{{...}}` denotes variables replaced by the caller, not real file paths):

```text
Task: Extract only order numbers explicitly present in <input>.
Output: If found, return the order number unchanged; otherwise answer "Not provided." Do not guess.
<input>
{{user_message}}
</input>
```

If downstream code parses a fixed object, use [Structured responses](interfaces/structured-output.md) instead; do not treat the free-text skeleton above as a JSON contract.

## Examples and complexity

Start with a zero-shot trial. If classification boundaries are unstable or a style must be imitated, add a few **correct** examples covering normal cases, similar categories, and missing information. Examples must not conflict, and production prompts must not include real credentials or sensitive samples. State that examples are input/output pairs to imitate, not new user requests. More examples consume more context and may encourage mechanical imitation.

For long-material tasks, test material placement for the model and invocation method, preserving boundaries between excerpt IDs/sources and the query; first reduce irrelevant excerpts rather than treating "fill the context" as RAG. Decompose complex tasks only when intermediate results can be checked independently; request brief, verifiable conclusions or verification items, not mandatory disclosure of private reasoning. Prefer configuration actually supported by the target API for image parameters (dimensions, transparent background, etc.), tool selection, and strict JSON output, rather than simulating them only in prose.

See [Strategy selection](strategy-selection.md) for specific trade-offs, and [Non-image generation](tasks/non-gen-image.md) and [Image generation](tasks/gen-image.md) for task-based examples. This section contains local recommendations organized from [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering), [Anthropic best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), and the [Google example notebook](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/prompts/intro_prompt_design.ipynb); their original examples are not reused.
