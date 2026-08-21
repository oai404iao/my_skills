---
name: agents-md
description: AGENTS.md and agents.md authoring guide. Use when creating, updating, reviewing, or restructuring repository instructions for AI coding agents.
---

# AGENTS.md Guide

Use this skill when the user asks to create, update, review, or improve `AGENTS.md`, `agents.md`, `.agents.md`, or equivalent repository instructions for AI coding agents.

The target document is an operational handbook for coding agents, not a generic README. It should help an agent make correct changes faster by naming the project shape, authoritative commands, architecture constraints, risky areas, local conventions, and verification paths.

## Source Pattern

This skill follows the structure observed in `maximhq/bifrost`'s `AGENTS.md`:

- A short project identity section before details
- A commented repository tree with high-value files and directories
- Workspace/package/module rules before commands
- Canonical build, test, dev, lint, and format commands
- Architecture flows and design principles
- Project-specific implementation patterns
- Numbered gotchas that prevent expensive mistakes
- Feature/change checklists
- Testing guidance by test layer
- Common workflows
- Key file quick references
- Code style and frontend/backend conventions where relevant

## When to Use

Use this skill for:

- Creating a new `AGENTS.md` from an existing codebase
- Updating stale agent instructions after code, commands, architecture, or tests changed
- Converting vague agent instructions into a specific operational guide
- Reviewing an existing `AGENTS.md` for missing commands, false claims, or weak guidance
- Adding project-specific gotchas, workflows, or quick references

Do not use this skill for marketing copy, public README prose, or human onboarding docs unless the user explicitly wants those merged into agent instructions.

## Core Principles

### Be Specific and Verifiable

Every claim should come from the repository, docs, CI, package manifests, Makefiles, scripts, or nearby code. Do not invent commands, architecture, module boundaries, package managers, or conventions.

Prefer:

- `make test-core PROVIDER=openai`
- `cd ui && npm run build`
- `transports/config.schema.json is the source of truth for config.json`

Avoid:

- `run the tests`
- `follow best practices`
- `this is a standard React app`

### Optimize for Agent Decisions

Good `AGENTS.md` content answers questions an agent would otherwise rediscover:

- Where does this kind of change belong?
- Which file is the source of truth?
- Which command is canonical instead of merely possible?
- What changes cascade across modules?
- Which tests are live, slow, flaky, or require services/API keys?
- Which conventions are load-bearing for CI, tests, generated files, or runtime behavior?

### Keep It Project-Specific

Generic advice belongs in global instructions, not project `AGENTS.md`. Include only facts and constraints that materially affect work in this repository.

## Creation Workflow

### Step 1: Inventory the Repository

Inspect the repo before drafting. Look for:

- Root files: `README*`, `CONTRIBUTING*`, `Makefile`, `justfile`, `Taskfile.yml`, `docker-compose*`, `AGENTS.md`
- Package and workspace files: `package.json`, `pnpm-workspace.yaml`, `go.work`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `requirements*.txt`, `pom.xml`, `build.gradle*`
- CI files: `.github/workflows/*`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`
- Test config: `playwright.config.*`, `vitest.config.*`, `jest.config.*`, `pytest.ini`, `tox.ini`, `go test` wrappers
- Lint/format config: `eslint*`, `prettier*`, `ruff.toml`, `biome.json`, `.golangci.yml`, `rustfmt.toml`
- Docs and schema sources: `docs/`, `openapi.*`, `schema.*`, `*.schema.json`, generated code comments
- Existing agent/tooling directories: `.claude/`, `.opencode/`, `.cursor/`, `.github/copilot-instructions.md`

Use broad searches for high-value facts:

- Commands: `scripts`, `make`, `test`, `lint`, `format`, `build`, `dev`
- Generated files: `generated`, `do not edit`, `codegen`, `schema`, `openapi`
- Test selectors: `data-testid`, fixtures, page objects, test helpers
- Architecture terms used repeatedly in docs and code

### Step 2: Identify Sources of Truth

For each domain, name the authoritative source:

- Config schema source
- API type source
- Route/source-of-truth registry
- Generated file inputs
- Canonical command wrapper
- Shared test fixture location
- Main extension interfaces
- Ownership boundary between frontend, backend, plugins, packages, or services

If there is a wrapper command in `Makefile`, `package.json`, `justfile`, or CI, prefer documenting that wrapper over raw lower-level commands.

### Step 3: Draft the Structure

Use this skeleton and omit sections that do not apply. The `## Code Comments Rules (Strict)` section is mandatory in every created or updated target document; copy it verbatim and do not weaken it:

````markdown
# AGENTS.md - <Project Name>

> Context for AI coding agents working on this codebase. Read this before making changes.

## What is <Project Name>?

One or two dense paragraphs: product purpose, runtime shape, primary languages/frameworks, and deployment/runtime context.

## Repository Layout

```text
repo/
|-- path/                 # Why this matters to agents
|-- package/              # Key responsibility and notable source files
`-- tests/                # Test layer and fixtures
```

## Workspace / Package Rules

- Monorepo/module layout
- Package manager and lockfile expectations
- Where to run dependency commands
- Cross-module import/release constraints

## Build, Test & Dev Commands

```bash
# Development
<canonical dev command>

# Tests
<canonical test command>

# Code quality
<format/lint/build command>
```

## Architecture

### <Primary Flow>

```text
Request/Event/Input
  -> subsystem
  -> subsystem
  -> output
```

### Design Principles

- Principle that affects implementation choices
- Isolation, ordering, caching, data consistency, performance, or security constraints

## Core Patterns

### <Pattern Name>

- Where it lives
- Naming conventions
- Required helper APIs
- Side effects to avoid
- Minimal code example if useful

## Gotchas

### 1. <Specific Failure Mode>

Explain the failure, why it happens, and the correct pattern.

## Adding or Changing <Major Feature Type>

1. Update source-of-truth type/schema/registry
2. Wire implementation sites
3. Update docs/generated outputs if required
4. Run targeted verification

## Testing

### <Test Layer>

- What it covers
- Whether it hits live services
- Required environment
- Canonical command

## Common Workflows

### <Workflow Name>

1. First file or subsystem to change
2. Dependent files to update
3. Tests to run

## Key Files Quick Reference

| What | Where |
|------|-------|
| Main entry point | `path/file` |
| Config schema | `path/schema.json` |

## Code Style

- Language-specific formatting
- Naming rules
- Dependency rules
- Error/logging conventions
- UI conventions, if relevant

## Code Comments Rules (Strict)

- Prefer self-explanatory code through clear naming and structure. Comments are secondary.
- ONLY add or update comments when the logic is **not self-evident**.
- Comment these things (and only these):
  - Non-obvious intent and design decisions (the "why")
  - Important constraints, invariants, ordering requirements, and error modes
  - Interface/usage contracts that prevent plausible misuse
  - Business rules or domain constraints that cannot be expressed in code alone
  - Non-obvious edge cases or workarounds (with brief reason)
- Do NOT:
  - Restate what the code obviously does
  - Add comments to code you did not change
  - Write play-by-play, change history, ticket numbers, or "TODO/FIXME" status notes
  - Invent undocumented behavior or constraints
  - Repeat the same fact across callers and implementations (keep each fact at its owning interface)
  - Leave tombstones, removed-code explanations, or boilerplate
- Keep comments short, precise, and up-to-date. Outdated comments are worse than no comments.
- When in doubt, write clearer code instead of a longer comment.
````

### Step 4: Fill Sections With Evidence

When drafting, include only confirmed facts. If a section cannot be verified, either omit it or phrase it as a question for the user.

For repository layout comments:

- Mention responsibility, not just name
- Name key files inside large directories
- Call out generated, shared, or risky directories
- Keep comments short enough to scan

For commands:

- Group by workflow: development, unit tests, integration tests, e2e tests, lint, format, build
- Include important arguments and examples
- Mark commands that hit live APIs, need credentials, start services, or are slow
- State command working directory when not root

For architecture:

- Prefer one accurate flow diagram over a long prose essay
- Name queues, caches, hooks, middleware, workers, stores, or event paths if those terms exist in the code
- Include ordering guarantees and lifecycle constraints

For gotchas:

- Use numbered headings
- Make each gotcha concrete: what breaks, where it lives, and the correct behavior
- Include warning signs agents can search for

## Update Workflow

When updating an existing `AGENTS.md`:

1. Read the current file fully before editing.
2. Identify what changed: commands, directory layout, dependencies, architecture, testing, generated files, conventions, or known pitfalls.
3. Verify each changed fact against source files or CI.
4. Patch only affected sections unless the file is structurally unusable.
5. Preserve useful project-specific details and remove stale instructions.
6. Keep command examples synchronized with actual scripts and Makefile targets.
7. Add a gotcha or workflow only when it prevents a plausible agent mistake.
8. Add or preserve the required `## Code Comments Rules (Strict)` section verbatim.
9. Re-read the final document for contradictions.

## Review Checklist

Before finishing, confirm:

- The document names the project and its runtime/workspace shape.
- The repository layout lists the directories agents are likely to touch.
- Commands are exact, current, and grouped by purpose.
- Slow/live-service tests are clearly marked.
- Architecture constraints are specific enough to guide edits.
- Gotchas describe real failure modes, not vague caution.
- Source-of-truth files are identified.
- Common workflows include update order and verification.
- Quick references point to real files.
- Style guidance matches existing code, not external preference.
- The required `Code Comments Rules (Strict)` section is present and unchanged.
- There are no invented commands, dependencies, or policies.
- There is no obsolete content copied from another project.

## Anti-Patterns

Avoid these common failures:

- Rewriting `README.md` as `AGENTS.md`
- Filling the file with generic coding advice
- Listing every file instead of the files that guide agent decisions
- Documenting raw commands when wrapper commands are canonical
- Ignoring CI and test fixtures when documenting verification
- Omitting environment requirements for integration or e2e tests
- Describing architecture without naming the actual code paths
- Adding broad checklists that do not match the repo
- Leaving stale paths after a refactor
- Copying another project's gotchas without evidence

## Output Expectations

When creating a new file, produce a complete `AGENTS.md` that is immediately useful but not bloated. A strong first version usually covers:

- Project identity
- Repository layout
- Workspace/package rules
- Commands
- Architecture overview
- Core patterns
- Gotchas
- Testing
- Common workflows
- Key files
- Code style
- Code comments rules

When updating, summarize the sections changed and the evidence used. If verification was not possible, state the gap explicitly.
