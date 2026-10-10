# Implementation and Commits

Scope control, pre-commit checks, and reporting completion. See the [Development Workflow Guide](../SKILL.md) for the main workflow.

## Scope Control

Each branch covers only one logical topic. In practice:

- Change only files relevant to the current task. Fix unrelated issues on a separate branch, or explicitly raise them and obtain consent.
- Do not commit other people's changes. If the workspace contains changes outside this task, determine their source first; do not include them in `git add`.
- Do not use `git add .` by default. Add files individually, or add everything only after `git status --short` confirms that all changes belong to this task.
- Do not delete, format, or refactor unrelated code as incidental cleanup.
- Do not change project configuration, CI, dependency versions, or ignore rules just to move the task forward—unless the task itself requires it.

When the scope needs to exceed expectations (for example, fixing a bug requires changing a public interface), explain why before acting; do not silently expand the scope.

## Pre-Commit Checks

```bash
git status --short
git diff
git add <relevant-files>
git diff --cached
```

Checklist:

- Staged content matches what `git status` reports, with no missing or mistakenly added changes.
- The diff contains no debugging leftovers: temporary `print` / `console.log` statements, commented-out old code, hard-coded local paths, or test accounts.
- Generated artifacts, dependency directories, caches, and local environment files are not accidentally committed; confirm that ignore rules actually cover them.
- The changes implement the task requirements without adding unrequested features or abstractions.
- Dead code introduced by this change has been removed from the new code; untouched existing code remains unchanged.

## Commit Messages

```text
<type>[optional scope][!]: <description>
```

- Use the project's prescribed values for `type`; if none exist, use `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `ci`, `style`, or `chore`.
- `scope` is optional and identifies a module or subsystem, such as `api`, `parser`, or `auth`.
- Write `description` in the imperative, starting with a lowercase letter and without a period, describing the actual change.
- One logical change per commit. Split "refactoring + incidental behavior changes" into two commits.
- Add `!` for breaking changes and a `BREAKING CHANGE:` footer explaining how to migrate.
- Put related tasks or issues in the footer, for example, `Refs: #123`.

Avoid descriptions such as `update stuff`, `fix issue`, `changes`, or `wip` that cannot be used to generate a CHANGELOG.

Examples:

```text
feat(auth): add passkey login
fix(api): handle empty upstream response
docs: correct local installation steps
refactor(parser): simplify token handling
feat(api)!: remove deprecated user endpoint
```

A development branch can have multiple commits; there is no need to force them into one, since Squash Merge combines them on the integration branch. However, each commit should be understandable on its own to support review and your own rollbacks.

## When to Commit

- Commit when a coherent logical unit is complete; do not pile an entire day's changes into one commit.
- For complex changes, commit a runnable state before continuing, rather than leaving a huge uncommitted diff for a long time.
- Full tests need not run before every commit, but commits should be in a runnable state; choose verification intensity using the levels in [Testing and Verification](testing.md).
- Do not stash changes the user wants to keep or clean the workspace with `reset --hard` just to "make the commit clean."

## Reporting Completion

The user cannot see your terminal, so the report should stand in for running the commands themselves:

- Explain what was actually done, not what you intend to do.
- List the commands actually run and their results; do not describe unrun verification as passing.
- State which files changed and whether there were deviations from the default workflow (such as not creating a branch or using another merge strategy).
- When blocked, explain the blocker and what you tried; do not describe partial completion as full completion.
- Explicitly mark anything that could not be verified as "not verified," explaining why and the remaining risks.

Statements to avoid:

- "Tests passed" when only a build was run.
- "Verified" when only a visual inspection was performed.
- Describing planned steps as completed.
- Reporting only successes when some checks failed.

Honestly reporting unfinished items saves the user more time than claiming everything passed.
