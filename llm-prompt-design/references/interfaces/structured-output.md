# 结构化最终响应：schema 负责形状，prompt 负责含义

当下游需要稳定字段时，优先用目标 API 支持的结构化输出，而非从自由文本中截取 JSON。要**调用外部工具**则使用 [tool schema](tool-schema.md)；二者可共存，但调用参数与最终用户响应有不同契约。[OpenAI 对两种用途的区分](https://developers.openai.com/api/docs/guides/structured-outputs)。

## 从使用场景反推 schema

1. 确认消费者真正需要的字段，按任务拆小 schema，而不是把分类、抽取、写入各分支堆在同一个深层对象或复杂 `anyOf` 中。先用单一 `type`、少量属性和必要的数组项；只有业务确实需要时才增加嵌套、联合类型或严格格式约束。
2. 给整体一个清楚的 `title`（平台支持时），给易混淆字段写 `description`：含义、来源、单位/格式、缺失语义。`title` 是标签，不能替代字段说明。封闭选项用 `enum`（包括确有约定的兜底值），不要只在 prompt 中列举合法值。
3. 分清**省略字段**与**字段值为空**：若目标 API 允许非必填字段，保持原类型，把可省略字段留在 `properties`、不放入 `required`；未知时省略，而不是一律改成 `["string", "null"]`。若必须输出固定键且业务允许，可用明确约定的 `""`、`[]` 或不与有效值冲突的 `0`，并让程序过滤/转换；不能把合法的 0、空文本或空列表误当缺失，也不能靠 `default` 假定模型会自行补值。若调用方明确需要区分“未知”与这些值，且平台支持，才考虑 `null` 或独立状态字段。
4. 为目标 API 校验 schema 子集、`required` 和嵌套对象约束。**OpenAI strict 结构化输出要求所有属性必填并设置 `additionalProperties: false`**，不能简单从 `required` 删字段；要么采用固定键+约定空值，要么按能力选 nullable 表达或非 strict 模式。其他平台各自核对，不能把“禁止联合类型”当 JSON Schema 标准。
5. 配套 prompt 说明取值、证据、缺失与空值规则，与 schema 的类型和枚举一致，不重复堆砌 schema。服务端仍须严格解析、校验字段间关系及业务语义，处理拒答/输出截断/工具失败；schema 通过不代表结果真实。

`description` 是模型可见的生成指导，不是开发说明栏。保留字段语义、来源、缺失规则及必要的篇幅建议；“该长度仅为生成提示，不作为校验条件”等实现说明放在开发文档，实际约束由 schema 关键字和本地校验决定。不要用测试强制这些解释句出现。相关反例与合同冲突排查见 [通用反模式](../engineering/anti-patterns.md)。

以上取舍来自对一个实际服务的路由与草稿 schema、配套 prompt 和 schema 兼容性检查的归纳：路由可以只要求判定枚举，条件字段未提供时省略；固定字段的草稿则要求每个字段单一类型、为空时用约定值，并在业务处理前检查。这里提炼的是**可选设计**，不把那个服务的私有业务字段搬到本 skill。模式效果应使用真实模型样本比较结构合格率和字段误填率。

## 完整示例：工单抽取与分类

需求：从工单正文取一个主类别及**原文明确出现**的订单号，并给一段原文证据。下面是 **OpenAI Responses API** 请求中的 `text.format` 对象示例，不是完整请求；Chat Completions 的字段不同：

```json
{
  "type": "json_schema",
  "name": "ticket_triage",
  "strict": true,
  "schema": {
    "type": "object",
    "title": "TicketTriage",
    "properties": {
      "category": {
        "type": "string",
        "enum": ["billing", "technical", "other"],
        "description": "主要诉求：billing 为扣费/发票/退款，technical 为功能故障；其余或主诉求不明为 other。"
      },
      "order_id": {
        "type": "string",
        "description": "原文明确给出的订单号；未提供时为空字符串。"
      },
      "evidence": {
        "type": "string",
        "description": "支持分类的原文短语；无可靠依据时为空字符串。"
      }
    },
    "required": ["category", "order_id", "evidence"],
    "additionalProperties": false
  }
}
```

配套指令（按平台放到合适的指令位置）：

```text
只根据 <ticket> 分类和抽取。
billing=扣费/发票/退款，technical=功能故障，其余或主诉求不明=other。
订单号须原样出现；没有就填 ""。evidence 引用支持主类别的原文短语；
无法找到依据时填 ""。这两个空字符串表示“未提供/无可靠依据”，
不得当作实际订单号或证据。不要从其他工单或常识补全。
<ticket>{{本次工单正文}}</ticket>
```

示意输入：“订单 A123 被重复扣费。”对应有效结果：

```json
{"category":"billing","order_id":"A123","evidence":"重复扣费"}
```

输入“被重复扣费，订单号忘了”时仍须输出 `order_id: ""`；下游应将 `""` 过滤或转为自己的缺失表示，不能拿它查订单。这里选空字符串是因为订单号和证据的有效值都应非空；如果空串本身是有效业务值，就不能沿用这项约定。输入即使显得可疑，也不能生成不存在的订单号。这个 schema **约束形状，不验证**订单是否真实、证据是否支持类别；必要时后端按业务规则再校验。提示词与 schema 应共同覆盖缺失、混合诉求、输入包含伪指令等失败样本。

**另一种方案：允许省略。**若目标接口支持非必填字段，可把 `order_id` 保持为 `{"type":"string"}`，但从 `required` 删去 `order_id`；没有订单号时输出的对象不包含这个键。同理，只有确有依据才输出 `evidence`。条件字段也可以用同一方式设计，例如 `approved=false` 时不输出正整数 `candidate_id`，由后端校验“通过则必填、拒绝则不得出现”。这个方案**不适用上面 OpenAI `strict: true` 的 schema**；切换前须确认目标 API 支持并对缺键、错误类型和额外字段执行本地校验。`0` 只有在业务 ID 不可能为 0 且调用方同意过滤时才能代替省略；不能把它当作真实候选 ID。

## 按任务选择，不把所有回答 JSON 化

| 任务 | 建模建议 | 预期作用 / 代价 |
| --- | --- | --- |
| 分类与路由 | 明确枚举及兜底；需要解释时用短证据字段 | 易解析；类别含义需业务定义 |
| 表单/发票抽取 | 原文值、来源位置与未知值分开 | 降低臆造；字段多时 schema 变复杂 |
| 汇总用于 UI | 只包含界面用得上的列表/状态字段 | 渲染稳定；可能不适合自由叙事 |
| 普通聊天、创意文案、生图输出 | 通常不为“整齐”强制 JSON | 保留自然表达；如图片工具需要参数，按图像接口单独建模 |

各平台的响应配置参见 [平台差异](../engineering/provider-compatibility.md)。不要混淆 **JSON mode**（通常只约束 JSON 有效）与按 schema 约束的结构化输出；即使后者成功，也要处理拒答、截断和事实错误。[OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)、[Anthropic structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)。
