# Testing and Verification

Choose verification intensity by the risk of the changes, and specify which checks cannot be skipped. See the [Development Workflow Guide](../SKILL.md) for the main workflow.

## Find the Project's Required Commands First

Take verification methods from the project first, rather than applying generic commands:

- Development instructions in `AGENTS.md`, `CONTRIBUTING.md`, README, and `docs/`.
- Task scripts: `scripts` in `package.json`, `Makefile`, `justfile`, `pyproject.toml`, `Cargo.toml`, and `build.gradle`.
- CI configuration: `.github/workflows/`, `.gitlab-ci.yml`, and `.circleci/`. The commands run in CI are the de facto acceptance criteria.

The same command may have multiple aliases (`test` vs `test:unit` vs `pytest -q`). Choose the smallest set matching the scope of the changes, but do not replace explicitly required project commands with weaker ones.

## Risk Levels

| Risk | Typical Changes | Minimum Verification |
| --- | --- | --- |
| Low | Comments, documentation, copy-only changes, log wording | Format checks or build (if the project has them); confirm referenced paths exist |
| Medium | Local logic, parameter handling, new logic branches, single-file refactoring | Project-required formatting + static checks + affected unit tests |
| High | Concurrency, encryption, permissions, data migrations, public APIs, dependency upgrades, build and CI configuration | Full tests + integration tests + manual verification of real execution paths + rollback plan |

Assess risk by the consequences of failure, not the number of changed lines: a one-line permission check is a small change but can have severe consequences if it fails.

Additional requirements for high-risk changes:

- Explain which paths verification covered and which edge cases remain uncovered.
- For data migrations or deletion, first confirm that rollback is possible, or explicitly state that it is not.
- For dependency upgrades, check the changelog for breaking changes and verify real call paths.

## Checks That Cannot Be Skipped

Regardless of risk level, the following are mandatory whenever they apply to the changes:

- Project-required formatting and static checks. Formatting drift obscures actual changes in the review diff.
- Existing tests affected by the changes. Do not skip failing tests because they "look unrelated."
- At least one test covering added or modified logic; if there truly is no test infrastructure, substitute reproducible manual steps and include them in the report.
- Marking breaking changes in the commit or PR/MR.
- A full build before release, or an equivalent release check defined by the project.

Do not claim verification passed in these situations:

- Tests require external services, credentials, or network access unavailable in the current environment. Explain why they were skipped and the affected scope.
- Only a subset was run. Specify which part was run.
- Tests were already failing. First distinguish failures introduced by the changes from existing failures, then report honestly.

## How to Run Checks

Prefer reusing the project's installed dependencies and pinned tool versions; do not install globally or switch package managers just to run a test once. If the project prescribes execution methods such as `uv`, `pnpm`, `bundle exec`, or `cargo`, follow them rather than directly substituting `python` / `npm`.

When temporary dependencies are needed for one-off verification, use isolated execution (such as `uv run --with <package>` or `pnpm dlx`) to avoid polluting the project's dependency manifest.

## Changes to Tests Themselves

Add or adjust tests only when the task requires it. When adding tests:

- Cover the changes' actual behavior, including edge cases and failure paths, rather than asserting only implementation details.
- Follow the project's existing test framework, directory structure, and naming conventions.
- Do not weaken assertions, skip cases, or remove existing coverage just to make tests pass.
- When fixing a bug, preferably add a case that reproduces it first, then confirm that it passes after the fix.

When removing functionality, also clean up its tests, fixtures, and documentation; do not leave dead tests asserting removed behavior.

## Reporting Verification Results

Include in the report:

- Commands actually run.
- A results summary: pass and failure counts, skipped cases, and reasons for skipping.
- Checks not run and why.
- Manual verification steps so the user can reproduce them.

Example wording:

```text
Ran: pytest tests/api -q — 42 passed
Ran: ruff check . — passed
Not run: integration tests (require a local database unavailable in the current environment)
Manual verification: POST /users returns 201; a repeated call returns 409
```

Do not write unverifiable conclusions such as "fully tested."
