# Isolated Development with Worktrees

This reference covers creating, using, syncing, recovering, and cleaning up repo-local linked worktrees.

**Read only when isolation is genuinely needed**: The default workflow is branch-based development in the current working tree, without worktrees. Follow this reference only when the user requests isolation, multiple tasks need to run in parallel, or unrelated changes in the current workspace must not be disturbed. See the [Development Workflow Guide](../SKILL.md) for the main workflow and default conventions.

## Conventions

- Main working tree: The working tree created by `git init` or `git clone`.
- Linked worktree: An additional working tree created with `git worktree add`.
- Root directory: Put all linked worktrees under `.worktrees/` in the main working tree.
- Directory name: Replace `/` in the development branch name with `-`; for example, `fix/api-timeout` maps to `.worktrees/fix-api-timeout`.
- Branch ownership: A development branch is checked out in only one worktree at a time.
- Local ignore: By default, write `/.worktrees/` to `$GIT_COMMON_DIR/info/exclude`; do not modify the project's tracked `.gitignore`.

Linked worktrees share the object database, ordinary refs, and repository configuration with the main working tree, but have their own `HEAD`, index, and working directory. Commits and branches created in any worktree are immediately visible to other worktrees in the same repository; uncommitted changes are not shared.

## Pre-Creation Checks

```bash
git status --short --branch
git branch --show-current
git remote -v
git worktree list --porcelain
```

Confirm:

- The target baseline branch and remote come from project rules, not guesses based on names.
- Whether current uncommitted changes belong to this task.
- Whether the development branch already exists or is checked out in another worktree.
- Whether `.worktrees/<task-slug>` is already used by another task.

If uncommitted changes belong to the current task, normally run `git switch -c <branch>` directly in the current working tree. If the changes are unrelated, preserve the original working tree and create a linked worktree from a committed baseline. Do not automatically stash or copy the entire dirty working directory.

## Locate the Main Working Tree

`git rev-parse --show-toplevel` returns the current worktree's root directory; when run in a linked worktree, this is not the main working tree's root. `git worktree list --porcelain` guarantees that the main working tree appears first:

```bash
main_worktree="$(git worktree list --porcelain | sed -n '1s/^worktree //p')"
git_common_dir="$(git -C "$main_worktree" rev-parse --absolute-git-dir)"
```

A bare repository has no main working tree, so do not use this reference's `.worktrees/` layout; follow project conventions or ask the user first.

## Ignore `.worktrees/`

`.worktrees/` is a local auxiliary directory for the current clone; add it to the repository-specific exclude by default:

```bash
mkdir -p "$git_common_dir/info"
touch "$git_common_dir/info/exclude"
grep -qxF '/.worktrees/' "$git_common_dir/info/exclude" ||
  printf '%s\n' '/.worktrees/' >> "$git_common_dir/info/exclude"
```

Verify that the main working tree does not report this directory as untracked:

```bash
git -C "$main_worktree" status --short
git -C "$main_worktree" check-ignore -v .worktrees/
```

Consider adding `/.worktrees/` to the version-controlled `.gitignore` only when the project explicitly requires all developers to use the same directory convention; do not maintain duplicate rules in both places.

Be especially careful when running `git clean` in the main working tree. `git clean -x` includes the ignored `.worktrees/` directory in cleanup; do not clean the main working tree with `git clean -fdx`, `git clean -ffdx`, or equivalent commands unless you have inspected every item in the dry-run output and explicitly confirmed that all linked worktrees can be deleted. Manage linked worktrees with `git worktree remove`.

## Create a Worktree with a New Branch

When there is a remote repository, prefer creating directly from the latest remote-tracking branch; there is no need to switch the main working tree first:

```bash
remote="origin"
target_branch="main"
development_branch="feat/user-export"
worktree_name="${development_branch//\//-}"
worktree_path="$main_worktree/.worktrees/$worktree_name"

git fetch "$remote" --prune
git worktree add -b "$development_branch" \
  "$worktree_path" \
  "$remote/$target_branch"
```

For a local-only repository:

```bash
target_branch="main"
development_branch="feat/user-export"
worktree_name="${development_branch//\//-}"
worktree_path="$main_worktree/.worktrees/$worktree_name"

git worktree add -b "$development_branch" \
  "$worktree_path" \
  "$target_branch"
```

Verify after creation:

```bash
git worktree list
git -C "$worktree_path" status --short --branch
git -C "$worktree_path" branch --show-current
```

Perform subsequent editing, testing, commits, and development branch syncing in `"$worktree_path"`.

## Attach an Existing Branch

First check branches and worktrees:

```bash
git branch --list "<development-branch>"
git worktree list --porcelain
```

If a worktree already has the branch checked out, continue working in that directory. Do not use `git worktree add --force` to put the same branch in multiple worktrees.

If the local branch exists and is not checked out:

```bash
development_branch="<type>/<short-description>"
worktree_name="${development_branch//\//-}"
worktree_path="$main_worktree/.worktrees/$worktree_name"

git worktree add "$worktree_path" "$development_branch"
```

If only a remote branch exists, first establish the local branch name and upstream:

```bash
git fetch <remote> --prune
git worktree add --track -b "<development-branch>" \
  "$worktree_path" \
  "<remote>/<development-branch>"
```

Do not reset an existing branch with `-B` unless the user explicitly requests it and you have confirmed that no commits will be lost.

## Sync and Verify

Sync with the target branch in the development worktree:

```bash
git -C "$worktree_path" fetch <remote> --prune
git -C "$worktree_path" rebase <remote>/<target-branch>
```

After resolving conflicts, rerun the project's required formatting, static checks, tests, and builds. Check before committing:

```bash
git -C "$worktree_path" status --short
git -C "$worktree_path" diff
git -C "$worktree_path" diff --cached
```

Do not assume that dependency directories, build artifacts, environment files, or untracked files are shared between worktrees. Prepare them separately in each worktree according to project requirements, or use the project's existing shared cache mechanism.

## Local Squash Merge

Keep the development worktree on the development branch. Update the target branch and merge in the main working tree:

```bash
git -C "$main_worktree" status --short
git -C "$main_worktree" switch <target-branch>
git -C "$main_worktree" fetch <remote> --prune
git -C "$main_worktree" pull --ff-only <remote> <target-branch>
git -C "$main_worktree" merge --squash <development-branch>
git -C "$main_worktree" commit -m "<type>(<scope>): <description>"
```

If another worktree already has the target branch checked out, complete integration there; do not force a duplicate checkout.

## Safe Cleanup

Confirm that the changes have been merged and the development branch is no longer needed, then check the development worktree:

```bash
git -C "$worktree_path" status --short --branch
```

If the output shows changes or untracked files, handle them first; do not skip checks with `--force`. Once the workspace is clean, run from the main working tree or another worktree:

```bash
git worktree remove "$worktree_path"
git branch -D <development-branch>
```

Squash Merge creates a new commit, so ordinary `git branch -d` may refuse to delete the development branch. Before using `-D`, you must confirm that the squash commit has reached the target branch.

If the remote branch needs cleanup:

```bash
git push <remote> --delete <development-branch>
```

Do not use `rm -rf "$worktree_path"` directly. Manually deleting the directory leaves worktree management metadata behind.

## Recovery and Troubleshooting

View machine-readable status:

```bash
git worktree list --porcelain
```

Preview stale metadata eligible for cleanup:

```bash
git worktree prune --dry-run --verbose
```

When the worktree must be retained but its path needs to change:

```bash
git worktree move <old-path> <new-path>
```

When the directory has been manually moved, or a change to the main working tree's path has broken the association:

```bash
git worktree repair <new-path>
```

When the directory has been manually deleted and you have confirmed that it contains nothing that needs recovery:

```bash
git worktree prune --dry-run --verbose
git worktree prune --verbose
```

`prune` processes stale worktree metadata for the entire repository. Check whether the dry-run output includes worktrees unrelated to the current task, temporarily offline, or unmounted; if in doubt, stop and confirm first.

When encountering a locked worktree, first check why it is locked:

```bash
git worktree list --verbose
```

Run `git worktree unlock <path>` only after confirming that the lock is no longer needed. Do not use repeated `--force` options to bypass protection for locked or dirty worktrees.

## Official References

- [git-worktree](https://git-scm.com/docs/git-worktree)
- [gitignore](https://git-scm.com/docs/gitignore)
- [git-clean](https://git-scm.com/docs/git-clean)
- [git-rev-parse](https://git-scm.com/docs/git-rev-parse)
