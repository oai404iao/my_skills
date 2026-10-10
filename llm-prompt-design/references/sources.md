# Sources and scope of rewriting

This skill **independently organizes rules and original examples** based on the sources below; it is not a copy or complete translation of any upstream guide. Shared terms (zero-shot, few-shot, tool schema, JSON Schema) refer to common concepts, not upstream endorsement. If external text, examples, or images are directly quoted or copied in the future, check the specific file version, license, and attribution; do not infer from this page that every page uses the same license.

## Main sources supplied by the user

| Source | Topics adopted by this skill |
| --- | --- |
| [OpenAI Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) | Instruction/context boundaries, few-shot examples, task-oriented iteration |
| [Anthropic Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview), [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | Define evaluable goals first, clear instructions, examples, and structured context |
| [GoogleCloudPlatform/generative-ai `gemini/prompts/`](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/prompts), [Introductory notebook](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/prompts/intro_prompt_design.ipynb) | Concise, specific, task-based organization and zero-/few-shot examples; model/SDK code in notebooks is not treated as a current universal invocation contract |
| [DAIR.AI Prompt Engineering Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) | An index of techniques and application types, without treating all techniques as best practices |

The **repository-level** licenses of the two GitHub repositories above are [GoogleCloudPlatform/generative-ai LICENSE](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/LICENSE) (Apache-2.0) and [DAIR.AI LICENSE](https://github.com/dair-ai/Prompt-Engineering-Guide/blob/main/LICENSE.md) (MIT), respectively. Only source and license information is retained here; no original examples or repository assets have been imported. Do not extend repository licenses to documentation on other websites without authorization.

## Specific interface and image sources

- [OpenAI Function calling](https://developers.openai.com/api/docs/guides/function-calling), [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [Image prompting](https://developers.openai.com/api/docs/guides/image-prompting).
- [Anthropic Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools), [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs).
- [Gemini Function calling](https://ai.google.dev/gemini-api/docs/function-calling), [Structured output](https://ai.google.dev/gemini-api/docs/structured-output), [Image generation](https://ai.google.dev/gemini-api/docs/image-generation), [API migration](https://ai.google.dev/gemini-api/docs/migrate-to-interactions).

Actual parameter names and support for tools/outputs change; the API types used in examples are identified in [Platform differences](engineering/provider-compatibility.md). Check official documentation again for actual integrations. The seven-slot `gen_image` formula comes from an example supplied by the user for this task, locally organized into optional items; it is not misrepresented as an upstream specification.
