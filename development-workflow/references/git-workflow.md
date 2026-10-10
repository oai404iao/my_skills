# Git Branching and Merging

Command details, boundaries on rebase and force-push, conflict resolution, and cleanup troubleshooting. See the [Development Workflow Guide](../SKILL.md) for the main workflow and default conventions.

## Inspect the Current State

```bash
git status --short --branch
git branch --show-current
git remote -v
git worktree list --porcelain
git log --oneline --decorate -10
```

Purpose:

- `status --short --branch` shows both the current branch and uncommitted changes, and is the first command to run before starting work.
- `worktree list --porcelain` is worth running even without isolation: another worktree may already have the development branch checked out.
- `log --decorate` confirms the integration branch's current tip, avoiding branching from stale local state.

When there is a remote repository, check the integration branch name against the remote default branch rather than assuming `main` / `master`:

```bash
git symbolic-ref --quiet --short refs/remotes/<remote>/HEAD
```

## Create and Switch Branches

When the workspace is clean and you need to start from the latest integration branch:

```bash
git fetch <remote> --prune
git switch <integration-branch>
git pull --ff-only <remote> <integration-branch>
git switch -c <type>/<short-description>
```

If there are already uncommitted changes belonging to this task, use `git switch -c` directly. The changes remain in the workspace; there is no need to commit or stash first.

Before creating a branch, check for a branch with the same name and existing worktrees:

```bash
git branch --list "<type>/<short-description>"
git worktree list --porcelain
```

If the branch already exists, continue using it rather than creating another. If another worktree has it checked out, work in that directory; do not use `--force` to put the same branch in two places.

## Boundaries on rebase

Sync with the integration branch:

```bash
git fetch <remote> --prune
git rebase <remote>/<integration-branch>
```

You may rebase:

- Local development branches used only by you.
- Branches that have not been pushed, or that have been pushed but you are certain nobody else is working from them.

Do not rebase:

- Integration branches, protected branches, or shared branches.
- History already merged into other branches or pulled by others.
- Public history that has already been pushed just to remove `Merge branch ...` commits.

Leave decisions about history-rewriting operations to the user; do not decide on your own. If recovering from an exceptional situation requires rewriting integration branch history, first confirm the range of commits and the user's intent.

## Boundaries on force-push

After rebasing your own development branch, when updating the remote copy is genuinely necessary:

```bash
git push --force-with-lease <remote> <development-branch>
```

Constraints:

- Use only `--force-with-lease`; do not override protection with plain `--force` or `--force-with-lease=<ref>`.
- Do not force-push integration branches, protected branches, or shared branches.
- Run `git fetch` before pushing, or the comparison baseline for `--force-with-lease` may be stale.

## Conflict Resolution

Resolve conflicts on your own development branch:

```bash
git status                 # View files with conflicts
# Edit each file, preserving the required semantics from both sides rather than simply choosing one side
git add <resolved-files>
git rebase --continue      # Or git merge --continue
```

Abort and return to the state before the operation:

```bash
git rebase --abort
git merge --abort
```

After resolving conflicts, rerun affected formatting, static checks, tests, and builds—conflict resolution can silently change behavior, so earlier verification results are not a substitute.

Do not switch to the integration branch, resolve conflicts hastily, and commit directly; that would put unverified merge results into the mainline.

## Merge Back to the Integration Branch

**PR/MR path**: Creating a PR/MR is the only exception to the default "do not push development branches" rule, and cleanup is mandatory when finished.

```bash
git push -u <remote> <development-branch>
gh pr merge --squash
```

It is recommended to turn off the platform's "automatically delete branches after merging" setting: it deletes remote branches before local cleanup, which can easily leave a series of local branch references that cannot be deleted.

**Local Squash Merge path**: Operate in the main working tree; the integration branch's workspace must be clean.

```bash
git -C <main-worktree> switch <integration-branch>
git -C <main-worktree> fetch <remote> --prune
git -C <main-worktree> pull --ff-only <remote> <integration-branch>
git -C <main-worktree> merge --squash <development-branch>
git -C <main-worktree> commit -m "<type>(<scope>): <description>"
git push <remote> <integration-branch>
```

`merge --squash` only stages changes and does not create a commit. It must be followed immediately by `git commit`, with a message that follows Conventional Commits.

## Cleanup Troubleshooting

### `git branch -d` Refuses to Delete

Squash Merge produces hashes different from the commits on the development branch, so `-d` considers it unmerged and refuses:

```text
error: the branch 'feat/x' is not fully merged
```

First confirm that the squash commit has reached the integration branch, then use `-D`:

```bash
git -C <main-worktree> log --oneline --grep="<squash commit subject>" <integration-branch>
git branch -D <development-branch>
```

`-D` unconditionally discards the branch reference; do not run it if you cannot confirm.

### Recover an Accidentally Deleted Branch

Shortly after deletion, you can recover it from the reflog:

```bash
git reflog --date=iso
git branch <development-branch> <sha>
```

The reflog expires and is stored only in the local clone; do not treat it as a backup.

### Remote Branch Deletion Fails

Branch protection or platform permission restrictions can prevent deletion:

```bash
git push <remote> --delete <development-branch>
```

If deletion fails, first remove protection on the platform or check permissions; do not resort to history-rewriting workarounds.

### Stale worktree Metadata

After a directory has been manually moved or deleted:

```bash
git worktree list --porcelain
git worktree prune --dry-run --verbose
```

Confirm that the dry-run output contains only stale entries belonging to this task, then run:

```bash
git worktree prune --verbose
```

### Post-Cleanup Checks

```bash
git branch --list
git worktree list
git status --short --branch
```

Confirm that development branches, worktrees, and uncommitted changes have been removed or retained as intended.

## Official References

- [git-branch](https://git-scm.com/docs/git-branch)
- [git-switch](https://git-scm.com/docs/git-switch)
- [git-rebase](https://git-scm.com/docs/git-rebase)
- [git-merge](https://git-scm.com/docs/git-merge)
- [git-push](https://git-scm.com/docs/git-push)
- [git-reflog](https://git-scm.com/docs/git-reflog)
