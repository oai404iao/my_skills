# Repository Patterns

Use these examples to select an organization pattern, not to import another project's policies. Examined on **2026-10-10**; links pin the inspected commits. The selection spans established coding-agent, editor, packaging, and monorepo projects. It is not a popularity ranking or evidence that every instruction in those repositories is good.

## Observed Patterns and Transferable Choices

| Repository and inspected file | Observation | Choice to consider | Do not generalize |
| --- | --- | --- | --- |
| [OpenAI Codex: bottom-pane AGENTS.md](https://github.com/openai/codex/blob/c3d3b142d10f4316b46e35aad7e5317e7e506cb7/codex-rs/tui/src/bottom_pane/AGENTS.md) | A narrow instruction keeps state-machine module documentation aligned with behavior and names a concrete sanity check. | Put a local invariant and its maintenance obligation near the affected subsystem. | This does not establish identical nested-file discovery for every host. |
| [Microsoft VS Code: root AGENTS.md](https://github.com/microsoft/vscode/blob/959031245ebb1fe077e0d512e1397c0ae82006e4/AGENTS.md) | A short root file directs agents to the existing Copilot instructions. | Reuse a maintained source instead of duplicating an architecture/style guide. | A Markdown pointer is not a guaranteed import; required context still needs a verified loading path. |
| [Astral uv: AGENTS.md](https://github.com/astral-sh/uv/blob/4bf8e7be2777dc545cd554ba91a4d9cd4bb9e594/AGENTS.md) | A flat list points to CONTRIBUTING.md for tool use and states concrete testing and implementation decisions. | A focused single file can be enough; headings and nesting are optional. | Its Rust conventions, snapshot preferences, and release-build restrictions are uv policy, not this skill's defaults. |
| [Apache Airflow: root AGENTS.md](https://github.com/apache/airflow/blob/65a83820fefdf693153c2f1016af4daa6c1fbe61/AGENTS.md), [UI instructions](https://github.com/apache/airflow/blob/65a83820fefdf693153c2f1016af4daa6c1fbe61/airflow-core/src/airflow/ui/AGENTS.md) | Root guidance contains marked generated commands and explicit decision boundaries; the UI file references contributor docs and adds local conventions. | Separate repository-wide rules from local additions; recognize generated text and use its owner to maintain it. | Its environment commands and approval policies cannot be copied into unrelated repositories. |
| [Vercel Turborepo: AGENTS.md](https://github.com/vercel/turborepo/blob/34e255684268c31ef961dacd82b783baf69c6c35/AGENTS.md) | A managed block points to installed-version docs, identifies the CLI template, and explains automatic rewriting and opt-out behavior. | Before modifying instructions, identify the generated block, template, and triggering tool. Use version-matched evidence. | Do not delete the block or change its opt-out configuration without authorization; unrelated PR rules are not a universal template. |
| [Pi: root AGENTS.md](https://github.com/earendil-works/pi/blob/42a3497d03ad17e308a2299fa824727894f2c0ec/AGENTS.md) | Concrete implementation constraints and risk-aware commands stay in the root; interactive testing and release procedures have task-triggered links. | Pair a constraint with its reason and safe alternative; route occasional workflows out of the always-relevant guidance. | Pi's compatibility, dependency, Git, temporary-file, and release policies are not portable defaults. See the focused analysis below. |

## Pi: Concrete Rules with Conditional Procedures

The [inspected root](https://github.com/earendil-works/pi/blob/42a3497d03ad17e308a2299fa824727894f2c0ec/AGENTS.md) illustrates how to make a rule useful at the point of decision:

- **Name the invariant and the alternative.** Asset lookup points to package configuration helpers and explains the different installation layouts they support. Generated model data points to its generator. The transferable writing pattern is affected path → supported edit or API → reason, rather than a bare prohibition.
- **Explain verification risk.** The command section distinguishes code changes from documentation, checks from tests, and selected tests from a suite that can contact endpoints when credentials are present. Learn to document working directory, coverage, and hidden side effects—not to copy Pi's command bans or infer that a check also runs tests.
- **State the collaboration assumption.** Git restrictions are motivated by simultaneous sessions sharing a working tree. For another project, establish whether that situation exists, then specify change ownership and safe inspection methods. Do not assume every repository needs the same restrictions.

The root's links to [interactive testing](https://github.com/earendil-works/pi/blob/42a3497d03ad17e308a2299fa824727894f2c0ec/.pi/skills/interactive-testing.md) and [release procedures](https://github.com/earendil-works/pi/blob/42a3497d03ad17e308a2299fa824727894f2c0ec/.pi/skills/release.md) each name the triggering task. This is a **root plus conditional procedures** layout, not evidence of automatic nested-file discovery. A target project can use ordinary supporting documents; it need not adopt Pi's skill directory.

Read adjacent policy before extracting a rule. Pi's [contributor guide](https://github.com/earendil-works/pi/blob/42a3497d03ad17e308a2299fa824727894f2c0ec/CONTRIBUTING.md) adds pre-submission checks and reserves changelog edits for maintainers. A local edit, contributor PR, and maintainer release do not have identical obligations.

Do not imitate the entire document or its emphatic tone. In particular, its default against preserving compatibility, generated-diff exception, and user-override confirmation clause need target-specific justification. Keep exceptions next to their scope, respect the actual instruction hierarchy, and retain only rules backed by the target project's evidence.

## Choose the Smallest Useful Layout

- **Flat:** a small set of broadly applicable rules and commands. Do not add nested files merely because a famous monorepo has them.
- **Layered:** distinct subtrees have different commands, owners, or contracts. Keep local additions narrow and check the host's actual discovery.
- **Shared:** a maintained document owns common facts. Link it with a reading condition or use a supported adapter; do not maintain two independent policy copies.
- **Generated:** a tool owns some instructions. Trace markers to their template or generator and keep hand-maintained additions outside the managed region.

These patterns can coexist. Popularity is not evidence that a target project needs a pattern, a strict tone, a particular package manager, or an arbitrary word limit.

## Maintenance and Sharing Traps

Airflow's [CLAUDE.md](https://github.com/apache/airflow/blob/65a83820fefdf693153c2f1016af4daa6c1fbe61/CLAUDE.md) is a symlink to AGENTS.md. This demonstrates a single content source, not universal symlink portability. Check the [host compatibility](host-compatibility.md) trade-offs before adopting it.

For managed content, preserve markers and inspect the owner before editing. A direct patch may be overwritten on the next CLI invocation. If the owning generator cannot be identified or safely run within scope, report that gap instead of pretending a hand edit is durable.

Review actual examples for contradictions too. In the inspected Airflow root, the environment section directs Python/test execution through Breeze, while the generated commands include direct `uv run` entries. That conflict needs project-specific resolution; neither statement should be copied as a supposedly universal best practice.

No upstream templates or instruction bodies are vendored here. This reference is locally authored comparative analysis; see [Sources](sources.md) for provenance and reuse boundaries.
