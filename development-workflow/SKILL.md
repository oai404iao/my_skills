---
name: development-workflow
description: Git development workflow guidelines covering branches, commits, testing and verification, merging and cleanup, and version releases. Use when making changes in a Git repository - creating branches, writing Conventional Commits, deciding what to verify before merging, squash merging back to the integration branch, cleaning up branches and worktrees, or bumping versions, tagging releases, and updating a changelog. Read the worktree reference as needed when the user requests isolated parallel development.
---

# Development Workflow Guide

When making feature, fix, documentation, refactoring, test, or maintenance changes in a Git repository, organize the work using this guide: **develop on a branch → verify → Squash Merge back to the integration branch → clean up → release a version when needed**.

This is the default workflow, not a rigid restriction that blocks development. The project's existing `AGENTS.md`, `CONTRIBUTING.md`, branch protection rules, and team conventions take precedence. If the user explicitly asks to work on the current branch, the project is unsuitable for branching, or the environment is restricted, continue completing the request, but explain any deviations.

## Default Conventions

These four points are where this guide is most likely to differ from common practice, so establish the defaults first:

1. **Branches, not worktrees**: By default, create a development branch in the current working tree with `git switch -c`. Use a linked worktree only when the user requests isolation, multiple tasks need to run in parallel, or unrelated changes in the current workspace must not be disturbed (see [Isolated Development with Worktrees](references/worktrees.md)).
2. **Push only the integration branch**: By default, do not push development branches to the remote. Merge them directly after finishing locally, avoiding an extra push and remote cleanup.
3. **Clean up immediately after merging**: Delete the development branch as soon as the Squash Merge succeeds; if a worktree was used, remove it too; if the development branch was actually pushed, also delete the remote branch.
4. **Squash Merge by default**: Each integration adds just one commit representing the changes to the integration branch, keeping the mainline history readable.

Tasks that do not modify the repository, such as read-only inspection, code explanation, searches, and log viewing, do not require branches, commits, or releases.

## Workflow

### 1. Inspect the Current State

Check the state before editing files; do not guess based on branch names:

```bash
git status --short --branch
git branch --show-current
git remote -v
```

Confirm that the current directory is a Git repository, whether the current branch is the integration branch or another task's development branch, whether the workspace has uncommitted changes, and whether the integration branch is called `main`, `master`, `develop`, or something else. Determine the integration branch from project documentation, the user's instructions, and the remote default branch.

### 2. Create a Development Branch

One logical topic per branch.

```bash
git fetch <remote> --prune
git switch <integration-branch>
git pull --ff-only <remote> <integration-branch>
git switch -c <type>/<short-description>
```

Follow the project's branch naming conventions. If none exist, use `<type>/<short-description>` with a prefix matching the commit type: `feat/`, `fix/`, `docs/`, `refactor/`, `perf/`, `test/`, `build/`, `ci/`, `style/`, or `chore/`. Include a task number when available, as in `feat/PROJ-123-user-export`.

If already on a development branch that matches the current task, keep using it rather than creating another. If the workspace already has uncommitted changes belonging to this task, use `git switch -c <branch>` directly; the changes will be preserved. If the workspace contains changes **unrelated to the task**, do not stash them or overwrite them with reset / checkout: handle them first or use a worktree for isolation, and do not include them in this commit.

### 3. Implement and Verify

Change only files relevant to the task, do not include other people's changes in your commits, and do not use `git add .` by default. After completing the changes, run the formatting, static checks, tests, and builds required by the project; choose verification intensity using the risk levels in [Testing and Verification](references/testing.md). See [Implementation and Commits](references/development.md) for scope control and pre-commit checks.

Commit messages must follow Conventional Commits:

```text
<type>[optional scope][!]: <description>
```

For example, `fix(api): handle empty upstream response`. Keep one logical change per commit, avoid vague descriptions such as `update stuff` or `fix issue`, and mark breaking changes with `!` and a `BREAKING CHANGE:` footer.

### 4. Sync with the Integration Branch

Before merging, ensure that the development branch is based on the latest integration branch, then rerun affected verification:

```bash
git fetch <remote> --prune
git rebase <remote>/<integration-branch>
```

Resolve conflicts on your own branch. Do not switch to the integration branch, resolve conflicts hastily, and commit directly. See [Git Branching and Merging](references/git-workflow.md) for the boundaries on rebase and force-push.

### 5. Merge Back to the Integration Branch

**When using remote hosting** (the default path):

```bash
git push -u <remote> <development-branch>   # Push only when PR/MR review is needed
# Select Squash Merge on the platform
```

Use Conventional Commits format for the PR/MR title, and include at least a summary of changes and verification results in the description. GitHub CLI example: `gh pr merge --squash`.

**For local-only projects, personal projects, or when local integration is explicitly allowed**:

```bash
git -C <main-worktree> switch <integration-branch>
git -C <main-worktree> pull --ff-only <remote> <integration-branch>
git -C <main-worktree> merge --squash <development-branch>
git -C <main-worktree> commit -m "<type>(<scope>): <description>"
git push <remote> <integration-branch>
```

Creating a PR/MR requires pushing the development branch; this is the only exception to the default rule, and it must be deleted when the task is finished. Turn off the hosting platform's "automatically delete branches after merging" setting: it acts before local cleanup, leaving local branches that cannot be deleted.

### 6. Clean Up After Merging

First confirm that the squash commit has reached the integration branch, then clean up in this order:

```bash
git worktree remove <worktree-path>              # If a worktree was used, remove its directory first
git branch -D <development-branch>               # Squashing changes hashes, so -d usually refuses
git push <remote> --delete <development-branch>  # Clean up only branches that were pushed
```

Before using `-D`, you must confirm that the changes are in the integration branch, or commits will be lost. Do not remove a worktree with `rm -rf`; do not add `--force` to `git worktree remove` just for convenience to bypass dirty-workspace checks. Inspect its contents first.

### 7. Release a Version (As Needed)

When the task requires external delivery, a release tag on the integration branch, or maintaining a CHANGELOG as required by the project, read [Versioning and Releases](references/versioning.md): choose the version using SemVer, mark it with an annotated tag, and update the CHANGELOG.

## Exceptional Cases

- **Committed on the integration branch but not yet pushed**: Create a development branch from the current commit and continue. Before rewriting integration branch history, confirm the range of commits and the user's intent; do not blindly `reset`.
- **The development branch has already been pushed**: Delete it both locally and remotely after merging. Explain why if it truly needs to be retained, and do not leave unintended orphaned branches.
- **Unable to create a branch or worktree**: Explain the reason and risks, then continue completing the request; do not stop just because the workflow cannot be followed.
- **The project requires a different merge strategy**: Project rules take precedence; explicitly state that the default Squash Merge was not used. The strategy affects where release tags land, so also review [Versioning and Releases](references/versioning.md) when changing strategies.

## Completion Criteria

- Changes are on a separate branch matching the task, with only one logical topic.
- Commit messages follow Conventional Commits, with no unrelated changes included.
- Formatting, checks, tests, or builds that were run have been reported honestly; checks not run have not been described as passing.
- Integration is complete through a PR/MR or local Squash Merge, adding just one commit representing these changes to the integration branch.
- The development branch has been deleted, any worktree used has been removed, and any pushed development branch has been deleted remotely.
- When a release is needed, the version number, annotated tag, and CHANGELOG agree and match the actual changes on the integration branch.

## References

- [Git Branching and Merging](references/git-workflow.md): Command details, boundaries on rebase and force-push, conflict resolution, and cleanup troubleshooting.
- [Implementation and Commits](references/development.md): Scope control, pre-commit checks, and reporting completion.
- [Testing and Verification](references/testing.md): Choosing verification intensity by risk level and checks that cannot be skipped.
- [Versioning and Releases](references/versioning.md): SemVer decisions, annotated tags, CHANGELOG, and release steps.
- [Isolated Development with Worktrees](references/worktrees.md): Read only when parallel tasks need isolation.
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Semantic Versioning 2.0.0](https://semver.org/)
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
