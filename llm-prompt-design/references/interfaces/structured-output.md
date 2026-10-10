# Structured final responses: Schemas define shape, prompts define meaning

When downstream consumers need stable fields, prefer structured output supported by the target API over extracting JSON from free text. To **call external tools**, use [Tool schemas](tool-schema.md); both can coexist, but call parameters and final user responses have different contracts. [OpenAI's distinction between these uses](https://developers.openai.com/api/docs/guides/structured-outputs).

## Derive the schema from its use case

1. Confirm the fields consumers actually need, and split schemas by task rather than piling classification, extraction, and write branches into one deep object or complex `anyOf`. Start with a single `type`, few properties, and necessary array items; add nesting, union types, or strict format constraints only when the business truly requires them.
2. Give the whole schema a clear `title` (where supported), and write `description` for easily confused fields: meaning, source, units/format, and missing-value semantics. `title` is a label, not a replacement for field descriptions. Use `enum` for closed sets (including genuinely agreed fallback values), not only lists of legal values in the prompt.
3. Distinguish **omitting a field** from **an empty field value**: if the target API allows non-required fields, keep their original types, leave omittable fields in `properties` but outside `required`, and omit them when unknown rather than always changing them to `["string", "null"]`. If fixed keys are required and business rules allow it, use explicitly agreed `""`, `[]`, or `0` that does not conflict with valid values, then filter/convert programmatically. Do not mistake valid 0, empty text, or empty lists for missing data, or assume `default` makes the model fill values automatically. Consider `null` or a separate status field only if the caller explicitly needs to distinguish "unknown" from these values and the platform supports it.
4. Validate the schema subset, `required`, and nested-object constraints for the target API. **OpenAI strict structured output requires all properties to be required and `additionalProperties: false`**; simply deleting fields from `required` is not allowed. Use fixed keys + agreed empty values, or choose nullable representations or non-strict mode according to capabilities. Check other platforms individually; do not treat "no union types" as the JSON Schema standard.
5. Accompany the schema with prompt rules for values, evidence, missing data, and empty values, consistent with schema types and enums, without repetitively restating the schema. The server still must parse strictly, validate inter-field relationships and business semantics, and handle refusals/truncation/tool failures; schema compliance does not make results truthful.

`description` is model-visible generation guidance, not a developer-notes field. Retain field semantics, sources, missing-value rules, and necessary length suggestions; implementation notes such as "this length is only generation guidance, not a validation condition" belong in developer documentation, while actual constraints come from schema keywords and local validation. Do not force these explanatory sentences to appear through tests. See [Common anti-patterns](../engineering/anti-patterns.md) for related counterexamples and contract-conflict diagnosis.

These trade-offs summarize routing and draft schemas, accompanying prompts, and schema-compatibility checks from an actual service: routing can require only a decision enum and omit unprovided conditional fields; fixed-field drafts require a single type per field, agreed values for empty fields, and checks before business processing. These are **optional designs**, not imports of that service's private business fields into this skill. Compare structural compliance and incorrectly filled fields on real model samples to evaluate the patterns.

## Complete example: Ticket extraction and classification

Requirement: Extract one primary category, an order number **explicitly present in the original text**, and a passage of original evidence from a ticket body. Below is an example `text.format` object in an **OpenAI Responses API** request, not a complete request; Chat Completions uses different fields:

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
        "description": "Primary request: billing covers charges/invoices/refunds, technical covers feature failures; anything else or an unclear primary request is other."
      },
      "order_id": {
        "type": "string",
        "description": "Order number explicitly provided in the original text; an empty string if not provided."
      },
      "evidence": {
        "type": "string",
        "description": "An original phrase supporting the classification; an empty string if there is no reliable evidence."
      }
    },
    "required": ["category", "order_id", "evidence"],
    "additionalProperties": false
  }
}
```

Accompanying instructions (placed in the appropriate instruction location for the platform):

```text
Classify and extract using only <ticket>.
billing=charges/invoices/refunds, technical=feature failures, anything else or unclear primary request=other.
The order number must appear unchanged in the original; use "" if absent. evidence quotes an original phrase supporting the primary category;
use "" if no evidence can be found. These two empty strings mean "not provided/no reliable evidence,"
not actual order numbers or evidence. Do not fill gaps from other tickets or general knowledge.
<ticket>{{current_ticket_body}}</ticket>
```

Illustrative input: "Order A123 was charged twice." Corresponding valid result:

```json
{"category":"billing","order_id":"A123","evidence":"charged twice"}
```

For "I was charged twice but forgot the order number," output `order_id: ""` nonetheless; downstream code should filter `""` or convert it to its own missing-value representation, not use it to query orders. Empty strings are chosen because valid order numbers and evidence should both be nonempty; do not reuse this convention if empty strings are valid business values. Even suspicious-looking input must not cause nonexistent order numbers to be generated. This schema **constrains shape, not the validity** of orders or whether evidence supports the category; apply further backend business validation where necessary. Prompts and schemas together should cover failure samples such as missing information, mixed requests, and input containing pseudo-instructions.

**Alternative: Allow omission.** If the target interface supports non-required fields, retain `order_id` as `{"type":"string"}` but remove it from `required`; the output object omits that key when no order number is present. Likewise, output `evidence` only when there is genuine support. Conditional fields can follow this design too: for example, omit the positive integer `candidate_id` when `approved=false`, with backend validation that "approval requires it; rejection forbids it." This approach **does not apply to the OpenAI `strict: true` schema above**; confirm target API support and locally validate missing keys, incorrect types, and extra fields before switching. `0` can replace omission only when business IDs cannot be 0 and the caller agrees to filter it; do not treat it as a real candidate ID.

## Choose by task; do not turn every answer into JSON

| Task | Modeling recommendation | Expected effects / costs |
| --- | --- | --- |
| Classification and routing | Explicit enums and fallback; short evidence field when explanation is needed | Easy parsing; category meanings require business definitions |
| Form/invoice extraction | Separate original values, source locations, and unknowns | Reduce invention; schemas grow complex with many fields |
| Summaries for UI | Include only list/status fields used by the interface | Stable rendering; may not suit free-form narrative |
| Ordinary chat, creative copy, image-generation output | Usually do not force JSON for "neatness" | Preserve natural expression; model image-tool parameters separately according to the image interface |

See [Platform differences](../engineering/provider-compatibility.md) for response configuration. Do not confuse **JSON mode** (usually constraining only JSON validity) with schema-constrained structured output; even if the latter succeeds, handle refusals, truncation, and factual errors. [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [Anthropic structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs).
