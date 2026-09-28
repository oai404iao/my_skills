# 平台差异：先认清 API，再抄示例

此页是**入口索引，不是版本锁定的 SDK 教程**。用户明确需要可执行请求时，先查看项目现有 SDK/模型/API、调用方式和目标平台当前官方文档，再核对 schema 子集、工具轮次、图像能力和错误/拒答路径；不要仅凭本页字段名直接上线。名称中的 `responses_format` 不是 OpenAI Responses API 的统一字段。

| 接口 | 工具定义 | 最终结构化响应 | 核对资料 |
| --- | --- | --- | --- |
| OpenAI Responses API | `tools` 中扁平的 `type: "function"`、`name`、`description`、`parameters`；可配置 `strict` | `text.format` 内 `type: "json_schema"`、`name`、`schema`、`strict` | [function calling](https://developers.openai.com/api/docs/guides/function-calling)、[structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs) |
| OpenAI Chat Completions | `tools` 项中的 `function: {name, description, parameters, ...}` 封装 | `response_format: {type: "json_schema", json_schema: {name, schema, strict}}` | 同上；**不要**把 Chat 的 `response_format` 写到 Responses 的 `text.format` 位置 |
| Anthropic Messages API | 自定义工具有 `name`、`description`、`input_schema`；严格输入校验须核对 `strict` 支持条件 | `output_config.format` 的 `json_schema` | [define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)、[structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) |
| Gemini API | 函数声明的名称、描述和参数 schema；外层封装随 API 而异 | Interactions API 使用 `response_format` 的 JSON text 配置；`generateContent` 使用 `response_mime_type` + `response_schema` 等配置，按实际版本核对 | [function calling](https://ai.google.dev/gemini-api/docs/function-calling)、[structured output](https://ai.google.dev/gemini-api/docs/structured-output)、[迁移说明](https://ai.google.dev/gemini-api/docs/migrate-to-interactions) |

**具体差异：**OpenAI strict function 对对象设置 `additionalProperties: false` 且所有属性列入 `required`，可用 nullable 表示业务可选；其他供应商的约束不完全相同。不同服务仅支持 JSON Schema 的子集，无法把任意标准 JSON Schema 原样跨平台发送。Anthropic 工具的 `input_schema` 描述的是工具**输入**，`output_config.format` 约束的是助手**最终回答**；OpenAI 的工具参数和 `text.format` 也是两条契约。不要把“要求 JSON”当成启用严格结构化输出。[OpenAI strict mode](https://developers.openai.com/api/docs/guides/function-calling)、[Anthropic structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)、[Gemini structured output](https://ai.google.dev/gemini-api/docs/structured-output)。

对于 `gen_image`，提示词描述画面；尺寸、质量、透明度、参考图、遮罩等由实际平台和模型支持的请求参数/输入承载。画面里说“透明”不保证得到含 alpha 通道的文件，说“编辑图 A”也不等于发送了图 A。对比生成与编辑接口、参数有效范围和输出格式，见 [OpenAI 图片提示指南](https://developers.openai.com/api/docs/guides/image-prompting)、[Gemini 图片生成](https://ai.google.dev/gemini-api/docs/image-generation)。平台发生迁移时，应先更新/验证具体 API 示例，不能把旧项目悄悄切到新接口。
