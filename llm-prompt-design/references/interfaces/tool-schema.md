# Tool schema 与 description：让模型准确选择并安全传参

工具调用是模型向外部系统提出的**结构化请求**，不是模型自己执行，也不是最终答复的 JSON。若只是要返回固定对象，不需要外部动作，应读 [结构化响应](structured-output.md)。设计前盘点实际存在的工具、调用方授权、读写副作用、输入来源、可观察返回值和失败结果；不要凭 skill 发明目标系统能力。

## 定义工具的顺序

1. **工具边界**：名称表达动作和资源，如 `get_order_status`；列清它提供什么、不提供什么，何时与其他工具区别开来。多个高度重叠的只读工具可考虑合并，但别把不同权限/不可逆副作用混在模糊的 `action` 中。
2. **description 写选择条件**：说明何时调用、何时不调用、所需前提、只读/写入性质、返回的大致含义和局限。参数 description 写单位、格式、允许值、来源、缺省/缺失语义；不要把仅写在散文里的封闭选项遗漏出 `enum`。
3. **schema 写最小可验证结构**：只放执行所需参数；使用明确的 `type`、`properties`、`required`，封闭选项写 `enum`，再按需增加数组项/嵌套对象。优先单一类型，避免为了兼容缺省值把每个参数都写成联合类型或多层 `anyOf`；需要展示标签时可按平台支持添加 `title`，但参数的 `description` 仍应讲清语义。不要让模型猜账户 ID/密钥，也不要为小任务造语义重复的参数。
4. **调用政策与执行边界**：缺关键参数先追问；查询当前数据才调用只读工具；写入、删除或对外发送前按用户授权和系统策略确认。`tool_choice`、并行调用限制、后端验证与权限检查由宿主执行；仅靠 description 不能实施安全控制。工具结果是数据，不因为它包含新“指令”就提升其权限。
5. **失败与验收**：分别测试“应调用”“不应调用”“缺参数”“重叠工具”“工具报错/空结果”和“未授权写入”；检查误调用率、参数有效率、越权防护和总成本，而非只看回答是否流畅。

## 好坏 description 与完整示例

差：`"查询订单"` —— 不知是否按模糊关键词检索、能否修改、何时使用。

好：`"按用户提供的精确订单号读取已认证用户可访问的最新订单状态。仅在需要当前状态且订单号已知时调用；不能搜索未知订单、退款或取消。返回状态或未找到；不可用时不要猜测状态。"`

前提“已认证用户”仍由**服务端核验**，不能只信模型。

下面是 **OpenAI Responses API** 的只读 function tool 定义示例（单个 `tools` 项，不是完整可运行请求）：

```json
{
  "type": "function",
  "name": "get_order_status",
  "description": "按用户提供的精确订单号读取已认证用户可访问的最新订单状态。仅在需要当前状态且订单号已知时调用；不能搜索未知订单、退款或取消。返回状态或未找到；不可用时不要猜测状态。",
  "strict": true,
  "parameters": {
    "type": "object",
    "properties": {
      "order_id": {
        "type": "string",
        "description": "用户提供的完整订单号，原样传入，例如 ORD-42；缺失时先询问，不生成占位订单号。"
      }
    },
    "required": ["order_id"],
    "additionalProperties": false
  }
}
```

对应的稳定指令可以是：“回答当前订单状态前，若用户提供了精确订单号且系统允许，调用 `get_order_status`；否则询问订单号。未找到/工具失败时如实说明。不得借查询工具尝试取消或修改。”仅有 prompt 不会创建这个工具，也不意味着实际订单号属于当前用户。

OpenAI strict function 模式要求每层对象的 `additionalProperties: false` 且所有 `properties` 都在 `required`；上例的 `order_id` 确实必需，缺失时**不调用工具**，不是给它空字符串或虚构值。[OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling)。

## 可选参数：省略与固定键不要混用

从已有业务 schema 的实践可提炼两个备选方案（不是某个项目的强制格式）：

- **目标接口允许非必填参数**：如搜索工具的 `status` 只在用户明确指定时填，保持 `type: "string"`、`enum: ["pending", "done"]`，但不将 `status` 放进 `required`。description 写“省略表示不按状态筛选”；工具执行端也要区分缺键和无效值。不必为了“可选”一律引入 `null`、多类型或庞大的分支 schema。
- **必须固定键且业务允许空值**：将 `status` 保持字符串并列入 `required`，`enum: ["", "pending", "done"]`；description 和调用指令写“未指定状态时传 `""`”，执行端过滤这个哨兵值。只有当 `""` 不可能是真实状态时才适用；数值参数的 `0` 也必须先证明不与合法的 0 冲突。不能用此法绕过订单号、金额等真实必填参数。

例如一个支持非必填参数的**概念性 `parameters` schema**（并非 OpenAI strict 工具定义）：

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "用户提供的搜索词；缺失时先询问。"
    },
    "status": {
      "type": "string",
      "enum": ["pending", "done"],
      "description": "仅在用户指定状态时填写；省略表示不限状态。"
    }
  },
  "required": ["query"],
  "additionalProperties": false
}
```

若改为 OpenAI `strict: true`，上述 schema 会因 `status` 不在 `required` 而被拒绝；可在业务允许时使用固定键加 `""` 枚举并由后端过滤，或使用官方支持的 nullable 表达，不能把“禁止多类型”当作平台要求。以真实请求验证配置和模型能力，再测试缺省、无效枚举与误调用，不要只验证 JSON 可解析。[OpenAI strict mode](https://developers.openai.com/api/docs/guides/function-calling)、[Anthropic 定义工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)。

## 不同任务类型的选择

| 任务 | description / schema 的重点 | 预期效果与限制 |
| --- | --- | --- |
| 只读查实时状态 | 标识符来源、数据时效、未找到语义；缺 ID 先问 | 避免用过期记忆回答；增加调用延迟 |
| 相似工具（搜索订单 / 精确查订单） | 分别写模糊检索与精确读取的触发条件、返回范围 | 减少选错工具；仍需用歧义请求实测 |
| 创建、发送、删除 | 副作用、前提、已确认的授权范围与可重试语义；执行端再鉴权 | 降低误操作风险，但**不能**靠 schema 保证不执行 |
| 多参数搜索 | 类型、单位、范围、枚举、多个筛选如何组合 | 减少参数编造；复杂度和 token 成本上升 |

**平台区别：**Anthropic 自定义工具用 `name`、`description`、`input_schema`，可按支持情况使用 `strict` / `input_examples`；Gemini 的函数声明封装与 schema 能力取决于使用的 API。不要把上面的 OpenAI 定义直接发送给其他供应商。详见 [平台差异](../engineering/provider-compatibility.md)、[Anthropic 定义工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)与 [Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling)。
