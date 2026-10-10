# Sources and Design Basis

Last verified: **2026-10-10**. This skill is independently written guidance, not a transcription of provider prompts or a third-party skill. Official docs establish format/host/model facts; repository snapshots illustrate organizational choices; inclusion criteria and review scenarios are local synthesis.

## Official Format and Skill Structure

| Source | Use |
| --- | --- |
| [AGENTS.md official site](https://agents.md/) — stewarded by the Agentic AI Foundation | Plain Markdown, no required headings, project-specific context, and nested guidance as a format convention. Its “closest wins” description is not a universal loader specification; host docs take precedence for actual discovery details. |
| [Agent Skills Quickstart](https://agentskills.io/skill-creation/quickstart.md) | Skill entry/frontmatter and progressive disclosure. Tutorial-specific VS Code paths are not this repository's installation policy. |

## OpenAI

| Source | Use |
| --- | --- |
| [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Codex startup discovery, per-directory selection, layering, and discovery checks. The earlier developers.openai.com/codex/guides/agents-md URL redirects here. |
| [Advanced configuration](https://learn.chatgpt.com/docs/config-file/config-advanced#project-instructions-discovery), [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) | Host configuration keys; not settings to modify automatically. |
| [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) | Clear separation of instructions, examples, and context, without treating API message roles as repository-file roles. |
| [GPT-6 Astra model](https://developers.openai.com/api/docs/models/gpt-6-astra), [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices) | Verified `gpt-6-astra` identity; instruction sensitivity, clarification, completion, and verification calibration. |
| [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) — Eric Provencher, 2026-09-11 | Narrow activation descriptions, reference routing, and task-conditional reading rather than elaborate universal recipes. |

The Codex guide describes a combined byte limit while the advanced page uses per-file wording. [The inspected loader source](https://github.com/openai/codex/blob/c3d3b142d10f4316b46e35aad7e5317e7e506cb7/codex-rs/core/src/agents_md.rs) corroborates a shared remaining project-document budget. This is source inspection, not an installed-host experiment; refresh before making size-dependent promises.

## Anthropic

| Source | Use |
| --- | --- |
| [How Claude remembers your project](https://code.claude.com/docs/en/memory) | CLAUDE.md and AGENTS.md support, competing files/settings, imports, path scoping, and discovery diagnostics. |
| [Claude Code best practices](https://code.claude.com/docs/en/best-practices#write-an-effective-claudemd) | Short, useful persistent context; separate occasional workflows; deterministic hooks versus advisory instructions. |
| [Claude Opus 5.5 model](https://platform.claude.com/docs/en/models/opus-5-5/overview) | Verified model name and formal ID `claude-opus-5-5`; the user's `opus-5.5` spelling is not the API identifier. |
| [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) | Completion and early-stop behavior, effort/harness boundaries, and pasted-content provenance. The page is not an AGENTS.md loading specification. |

Model IDs, host version requirements, feature availability, defaults, and size limits are version-sensitive. Verify current official documentation when adapting a real deployment; do not present this snapshot as a universal contract.

## Repository Snapshots

Exact file permalinks and observations are in [Repository patterns](repository-patterns.md).

| Repository | Inspected commit |
| --- | --- |
| `openai/codex` | `c3d3b142d10f4316b46e35aad7e5317e7e506cb7` |
| `microsoft/vscode` | `959031245ebb1fe077e0d512e1397c0ae82006e4` |
| `astral-sh/uv` | `4bf8e7be2777dc545cd554ba91a4d9cd4bb9e594` |
| `apache/airflow` | `65a83820fefdf693153c2f1016af4daa6c1fbe61` |
| `vercel/turborepo` | `34e255684268c31ef961dacd82b783baf69c6c35` |
| `earendil-works/pi` | `42a3497d03ad17e308a2299fa824727894f2c0ec` |

These established repositories were selected for contrasting flat, local, shared, and generated instruction patterns, not as a ranked popularity sample or a quality benchmark. Their commands, style rules, approval boundaries, and Git policies remain project-local.

For Pi, inspected the root `AGENTS.md`, `CONTRIBUTING.md`, `.pi/skills/interactive-testing.md`, and `.pi/skills/release.md` at the pinned commit. The analysis concerns instruction writing and task routing, not Pi host discovery. Its [LICENSE](https://github.com/earendil-works/pi/blob/42a3497d03ad17e308a2299fa824727894f2c0ec/LICENSE) is MIT, copyright 2025 Mario Zechner; this skill adds attributed analysis, not a vendored copy of those instructions.

## Reuse and Verification Boundaries

No upstream instruction bodies, templates, or scripts are copied into this skill. Examples are locally authored or summarized with attribution; linked material retains its own ownership and applicable terms. References do not confer redistribution rights, license this whole repository, or imply provider endorsement. If future maintenance copies upstream material, verify its license and preserve the required notices.

Source inspection supports the stated facts and design rationale. It does not establish that Codex or Claude Code loaded these files in a local session, that either named model passed the review scenarios, or that the redesign achieved a measured improvement.
