# Bruno Projects, Documentation, and Sources

Read this reference when checking version differences, locating implementations, or updating this skill. This skill is independently authored. Its core workflow, "GUI for humans, files for AI to edit, CLI for execution," comes from this repository's maintenance requirements, not an official Bruno standard or a policy of the target project.

## Official Links

| Entry point | Link and purpose |
| --- | --- |
| Bruno website | [usebruno.com](https://www.usebruno.com/) |
| Source repository | [usebruno/bruno](https://github.com/usebruno/bruno) |
| Official documentation | [docs.usebruno.com](https://docs.usebruno.com/) |
| Documentation repository | [usebruno/bruno-docs](https://github.com/usebruno/bruno-docs) |
| Releases and versions | [Releases](https://github.com/usebruno/bruno/releases) |
| Bru format | [Language](https://docs.usebruno.com/bru-lang/language), [Tags](https://docs.usebruno.com/bru-lang/tag-reference), [Samples](https://docs.usebruno.com/bru-lang/samples) |
| CLI | [Overview](https://docs.usebruno.com/bru-cli/overview), [Installation](https://docs.usebruno.com/bru-cli/installation), [Run](https://docs.usebruno.com/bru-cli/run/overview), [Options](https://docs.usebruno.com/bru-cli/run/options), [Reports](https://docs.usebruno.com/bru-cli/run/reports), [Import](https://docs.usebruno.com/bru-cli/import/overview) |
| Variables and tests | [Process environment](https://docs.usebruno.com/variables/process-env), [JavaScript API](https://docs.usebruno.com/testing/script/javascript-reference), [Tests](https://docs.usebruno.com/testing/tests/introduction), [Script flow](https://docs.usebruno.com/testing/script/script-flow) |
| YAML format | [Overview](https://docs.usebruno.com/opencollection-yaml/overview), [Structure](https://docs.usebruno.com/opencollection-yaml/structure-reference), [Bru → YAML migration](https://docs.usebruno.com/bru-lang/yaml-migration) |

## Inspected Source Snapshots

Official repository `main` snapshots inspected on 2026-10-12:

- Bruno: [`8833538ce20548f26b88079ce701095e7b06f682`](https://github.com/usebruno/bruno/tree/8833538ce20548f26b88079ce701095e7b06f682)
- Bruno docs: [`3381866fc132a9a2a2aaf18c86bac3ec947e8530`](https://github.com/usebruno/bruno-docs/tree/3381866fc132a9a2a2aaf18c86bac3ec947e8530)

These SHAs record research evidence; they are not required installation versions. Package versions in source manifests do not establish the latest npm release. Do not infer app, CLI, or language-package versions from each other. Use the project's pinned version and the installed CLI's help.

Paths below are relative to the Bruno source root. Start here when updating the references:

| Location | What to verify |
| --- | --- |
| `packages/bruno-lang/v2/src/bruToJson.js` / `jsonToBru.js` | Request tags, disabled fields, body modes, uploads, and text blocks |
| `packages/bruno-lang/v2/src/collectionBruToJson.js` / `jsonToCollectionBru.js` | Collection/folder authentication, variables, scripts, and tests |
| `packages/bruno-lang/v2/src/envToJson.js` / `jsonToEnv.js` | Environment variables, secret names, and environment extensions |
| `packages/bruno-lang/v2/tests/` | Format and round-trip examples |
| `packages/bruno-filestore/src/formats/bru/index.ts` / `packages/bruno-filestore/src/formats/yml/items/parseHttpRequest.ts` | File parsing layer called by the CLI; wraps the Bru parser and converts YAML requests |
| `packages/bruno-cli/src/commands/run.js` | cwd, recursion defaults, options, environment merging, filtering, reports, and exit behavior |
| `packages/bruno-cli/src/commands/import.js` | Import types, output, and default format |
| `packages/bruno-cli/src/utils/collection.js` | Root configuration detection, request ordering, and collection loading |
| `packages/bruno-cli/src/runner/prepare-request.js` / `run-single-request.js` | URL, query, upload paths, HTTP status handling, scripts, and execution |
| `packages/bruno-cli/src/utils/persist-variables.js` / `sanitize-results.js` | Variable persistence and report field filtering |
| `packages/bruno-js/src/bruno-response.js` / `runtime/assert-runtime.js` | Response API and assertion execution |
| `packages/bruno-tests/collection/` | Executable request examples; research material, not permission to access their test services |

## Documentation and Implementation Boundaries

- The Bru tag-reference test example uses `body:test`, but the snapshot parser registers `tests`. This skill follows the parser and actual request examples rather than copying that example.
- The YAML overview claims `.bru` and `.yml` can coexist, whereas the migration page explicitly prohibits mixed formats within a collection. This skill does not claim to resolve that upstream contradiction. It conservatively preserves the existing single format without automatic mixing or migration.
- CLI documentation includes options not registered by the snapshot's `run` builder, such as some parallel/data-iteration options. A website capability list is not a guarantee for every installed CLI.
- `--tests-only` is the snapshot's option name. An older changelog uses singular `--test-only`; that does not establish a supported alias in the current CLI.
- Static source inspection and example parsing are not desktop loading tests or live CLI execution tests. Do not claim end-to-end verification without actually running a collection, import, or GUI operation.

During this skill's initial authoring, the 11 Bru / JSON / YAML examples in `file-format.md` were parsed offline: Bru used the snapshot's request, collection, and environment parsers; JSON used standard parsing; YAML was checked for syntax only. No HTTP requests were sent, and no real collection, import, or desktop session was run. This does not establish full schema, script, or API compatibility with a target version.

## Provenance and Licensing

The `license.md` files at the Bruno repository root and in `bruno-lang` declare MIT licensing with **Copyright (c) 2022 Anoop M D, Anusree P S and Contributors**. See the [pinned license](https://github.com/usebruno/bruno/blob/8833538ce20548f26b88079ce701095e7b06f682/license.md).

This skill independently summarizes source behavior and official documentation, with independently written examples. It does not vendor upstream implementations, complete test collections, screenshots, or documentation text. No standalone LICENSE file was found at the documentation snapshot's root. Do not automatically extend the code repository's MIT license to the website, documentation, trademarks, or product services. If substantial source code is copied later, retain the upstream MIT license in full and its attribution. Check the applicable license separately before copying documentation or assets.
