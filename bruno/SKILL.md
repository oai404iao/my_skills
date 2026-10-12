---
name: bruno
description: Create, edit, review, and run Bruno API collections, environments, assertions, and tests through files and the CLI. Use for .bru, bruno.json, collection.bru, folder.bru, OpenCollection YAML, bru run/import, API debugging, and CI integration. Not for GUI automation, developing Bruno itself, or replacing API contract design.
---

# Using Bruno

**GUI for humans, files for AI to edit, CLI for execution.**

Humans use the Bruno desktop app to browse collections, inspect responses, and collaborate. AI maintains version-controlled request, configuration, environment, and test files directly. Execute through the `bru` command from `@usebruno/cli`. Do not click through the GUI for routine request edits or bypass the collection with ad hoc HTTP scripts as the default execution method.

## Read References by Task

Resolve paths relative to this skill's directory. Load only the references needed for the current task.

| Task | Reference |
| --- | --- |
| Create or edit requests, environments, inherited configuration, scripts, and tests; identify `.bru` / YAML | [File format](references/file-format.md) |
| Installation and version checks, execution, filtering, reports, imports, or CI | [CLI usage](references/cli.md) |
| Find official repositories/docs, verify new capabilities, or check provenance and licensing | [Projects and sources](references/sources.md) |

## Required Workflow

### 1. Establish the Collection and Execution Boundaries

- Read the target project's instructions, existing Bruno files, execution scripts, and dependency declarations first. Find the collection root: Bru collections typically have `bruno.json`; YAML collections have `opencollection.yml`. When multiple collections exist, identify the target rather than assuming the Git root is the collection root.
- Inspect collection configuration, `collection.bru` / `folder.bru` (or their YAML equivalents), the selected environment, affected requests, and inherited scripts, authentication, and variables. Do not judge an execution side-effect-free by inspecting only one request.
- Preserve existing format, naming, ordering, and test style. `.bru` is not JSON, and OpenCollection YAML is not OpenAPI. Do not migrate formats, mix formats, or rebuild the collection without authorization.
- Distinguish read-only review, file edits, and sending requests. Permission to edit does not automatically authorize execution: requests reach real services, and scripts may send additional requests. Clarify an ambiguous target environment, write operation, or execution scope when it affects safety; continue unaffected file work.

### 2. Make Minimal Edits

- Follow the existing API contract and neighboring requests. Do not invent endpoints, success status codes, credentials, or business data. Clarify missing information that materially affects the result.
- Reuse environment variables and inherited authentication. Keep real secrets out of committable files, examples, output, and reports. Do not assume secrets stored locally by the GUI are automatically available to the CLI.
- Keep the method, URL, parameters, body mode, and corresponding content blocks consistent. Assign an appropriate `seq` to new requests. Avoid unrelated reordering, whole-file formatting, and bulk replacements.
- Add declarative `assert` entries or `tests` for the behavior being verified, not merely to confirm that a request was sent. Introduce scripts and runtime variables only when needed.
- Do not change module allowlists, filesystem permissions, TLS verification, or script sandbox configuration without the necessary authorization.

### 3. Separate File Validation from Network Execution

1. **File checks:** inspect diffs, format, inheritance, variable references, and secret exposure. Prefer an existing offline parser or validator when the project provides one. Do not treat `bru run` as a side-effect-free syntax checker.
2. **CLI checks:** use the project's established invocation and inspect `--version` and `run --help`. Do not assume newly documented options exist locally.
3. **Authorized execution:** run the specified request or necessary dependency chain from the collection root with an explicit environment. When login/token dependencies exist, execute the complete necessary chain rather than blindly running the entire collection. Expand to a folder or full collection only when authorized.
4. **Result assessment:** examine the process exit code, request errors, HTTP status, assertions, and tests together. A zero exit code does not prove business correctness; without assertions, an unexpected status code may not count as a test failure.

`--tests-only` filters requests with tests/assertions; it is not a dry run and does not prevent network requests. Before execution, inspect request chains, inherited scripts, and any data/iteration options actually supported by the installed CLI's help that may expand execution scope. See the CLI reference.

### 4. Report and Stop

Report changed files, commands actually executed and their working directories, request scope and environment, assertion/test results, and remaining issues. Redact sensitive data. Explicitly say "not run" when execution was skipped; successful parsing is not a passed API test.

Stop once required checks pass and no unresolved issues remain. Using this skill does not itself authorize full-collection runs, production requests, installations/upgrades, commits/pushes, publishing, or global configuration changes.

## Official Entry Points

- [Bruno repository](https://github.com/usebruno/bruno)
- [Bruno documentation](https://docs.usebruno.com/)
- [Bruno CLI documentation](https://docs.usebruno.com/bru-cli/overview)

See [Projects and sources](references/sources.md) for further implementation pointers and pinned source snapshots.
