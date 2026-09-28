# 来源与改写范围

本 skill 依据下列资料**独立组织规则与原创示例**；不是任何一份上游指南的拷贝或完整翻译。相同词语（zero-shot、few-shot、tool schema、JSON Schema）用于指代通用概念，不代表上游背书。外部内容若将来直接引用、复制示例或图片，应核对具体文件版本、许可证和署名，不以本页推定所有页面采用同一许可。

## 用户提供的主要资料

| 来源 | 本 skill 采用的主题 |
| --- | --- |
| [OpenAI Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) | 指令/上下文边界、few-shot、面向任务迭代 |
| [Anthropic Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)、[Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | 先定义可评估的目标、清晰指令、示例与结构化上下文 |
| [GoogleCloudPlatform/generative-ai 的 `gemini/prompts/`](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/prompts)、[入门笔记本](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/prompts/intro_prompt_design.ipynb) | 简洁、具体、按任务拆分及 zero-/few-shot 的案例组织；笔记本中的模型/SDK 代码不作为当前通用调用契约 |
| [DAIR.AI Prompt Engineering Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) | 多种技巧和应用类型的索引，不把技巧一概定为最佳实践 |

上述两个 GitHub 仓库的**仓库级**许可分别见 [GoogleCloudPlatform/generative-ai LICENSE](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/LICENSE)（Apache-2.0）与 [DAIR.AI LICENSE](https://github.com/dair-ai/Prompt-Engineering-Guide/blob/main/LICENSE.md)（MIT）。此处仅保留来源及许可信息，未引入原文示例或仓库资产；别把仓库许可擅自扩展到其他网站文档。

## 特定接口和图像资料

- [OpenAI Function calling](https://developers.openai.com/api/docs/guides/function-calling)、[Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)、[Image prompting](https://developers.openai.com/api/docs/guides/image-prompting)。
- [Anthropic Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)、[Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)。
- [Gemini Function calling](https://ai.google.dev/gemini-api/docs/function-calling)、[Structured output](https://ai.google.dev/gemini-api/docs/structured-output)、[Image generation](https://ai.google.dev/gemini-api/docs/image-generation)、[API migration](https://ai.google.dev/gemini-api/docs/migrate-to-interactions)。

其中 tool/输出的实际参数名和支持范围会变化，示例对应的 API 类型已在 [平台差异](engineering/provider-compatibility.md)标明；实际集成需再次核对官方文档。`gen_image` 七槽位公式来自本任务用户给出的示例，经本地整理为可选项；没有将它伪称为上游规范。
