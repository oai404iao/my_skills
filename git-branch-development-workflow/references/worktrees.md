# Git Worktree 操作参考

本参考用于创建、使用、同步、恢复和清理 repo-local linked worktree。主流程和分支策略见 [Git Branch Development Workflow](../SKILL.md)。

## 约定

- 主工作树：`git init` 或 `git clone` 创建的工作树。
- linked worktree：通过 `git worktree add` 创建的附加工作树。
- 根目录：所有 linked worktree 放在主工作树的 `.worktrees/` 下。
- 目录名：把开发分支名中的 `/` 替换为 `-`，例如 `fix/api-timeout` 对应 `.worktrees/fix-api-timeout`。
- 分支归属：一个开发分支同时只在一个 worktree 中检出。
- 本地忽略：默认把 `/.worktrees/` 写入 `$GIT_COMMON_DIR/info/exclude`，不修改项目跟踪的 `.gitignore`。

linked worktree 与主工作树共享对象数据库、普通 refs 和仓库配置，但拥有独立的 `HEAD`、index 和工作目录。任一 worktree 创建的提交和分支会立即对同一仓库的其他 worktree 可见，未提交改动不会共享。

## 创建前检查

```bash
git status --short --branch
git branch --show-current
git remote -v
git worktree list --porcelain
```

确认：

- 目标基线分支和 remote 来自项目规则，而不是名称猜测。
- 当前未提交改动是否属于本任务。
- 开发分支是否已存在或已由其他 worktree 检出。
- `.worktrees/<task-slug>` 是否已经被其他任务使用。

如果未提交改动属于当前任务，通常直接在当前工作树执行 `git switch -c <branch>`。如果改动与任务无关，保留原工作树，并从已提交的基线创建 linked worktree。不要自动 stash 或复制整个脏工作目录。

## 定位主工作树

`git rev-parse --show-toplevel` 返回当前 worktree 的根目录；从 linked worktree 中执行时，它不是主工作树根目录。`git worktree list --porcelain` 保证主工作树排在第一项：

```bash
main_worktree="$(git worktree list --porcelain | sed -n '1s/^worktree //p')"
git_common_dir="$(git -C "$main_worktree" rev-parse --absolute-git-dir)"
```

在 bare repository 中没有主工作树，不使用本参考的 `.worktrees/` 布局；遵循项目约定或先询问用户。

## 忽略 `.worktrees/`

`.worktrees/` 是当前 clone 的本地辅助目录，默认写入 repository-specific exclude：

```bash
mkdir -p "$git_common_dir/info"
touch "$git_common_dir/info/exclude"
grep -qxF '/.worktrees/' "$git_common_dir/info/exclude" ||
  printf '%s\n' '/.worktrees/' >> "$git_common_dir/info/exclude"
```

验证主工作树不会把该目录报告为未跟踪：

```bash
git -C "$main_worktree" status --short
git -C "$main_worktree" check-ignore -v .worktrees/
```

只有项目明确要求所有开发者使用同一目录约定时，才考虑把 `/.worktrees/` 加入受版本控制的 `.gitignore`；不要同时维护重复规则。

在主工作树执行 `git clean` 时要特别谨慎。`git clean -x` 会把被忽略的 `.worktrees/` 纳入清理范围；不要使用 `git clean -fdx`、`git clean -ffdx` 或等价命令清理主工作树，除非已经逐项检查 dry-run 输出并明确确认所有 linked worktree 均可删除。linked worktree 应通过 `git worktree remove` 管理。

## 创建新分支 Worktree

有远程仓库时，优先直接从最新 remote-tracking branch 创建，不必先切换主工作树：

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

纯本地仓库：

```bash
target_branch="main"
development_branch="feat/user-export"
worktree_name="${development_branch//\//-}"
worktree_path="$main_worktree/.worktrees/$worktree_name"

git worktree add -b "$development_branch" \
  "$worktree_path" \
  "$target_branch"
```

创建后验证：

```bash
git worktree list
git -C "$worktree_path" status --short --branch
git -C "$worktree_path" branch --show-current
```

后续编辑、测试、提交和开发分支同步都在 `"$worktree_path"` 中执行。

## 挂载已有分支

先检查分支和 worktree：

```bash
git branch --list "<development-branch>"
git worktree list --porcelain
```

如果分支已由某个 worktree 检出，进入该目录继续工作。不要使用 `git worktree add --force` 让同一分支出现在多个 worktree。

如果本地分支存在且未被检出：

```bash
development_branch="<type>/<short-description>"
worktree_name="${development_branch//\//-}"
worktree_path="$main_worktree/.worktrees/$worktree_name"

git worktree add "$worktree_path" "$development_branch"
```

如果只有远程分支，先明确本地分支名和上游：

```bash
git fetch <remote> --prune
git worktree add --track -b "<development-branch>" \
  "$worktree_path" \
  "<remote>/<development-branch>"
```

不要用 `-B` 重置已有分支，除非用户明确要求并已确认不会丢失提交。

## 同步与验证

在开发 worktree 中同步目标分支：

```bash
git -C "$worktree_path" fetch <remote> --prune
git -C "$worktree_path" rebase <remote>/<target-branch>
```

解决冲突后重新运行项目规定的格式化、静态检查、测试和构建。提交前检查：

```bash
git -C "$worktree_path" status --short
git -C "$worktree_path" diff
git -C "$worktree_path" diff --cached
```

不要假设依赖目录、构建产物、环境文件或未跟踪文件会在 worktree 之间共享。按项目要求在每个 worktree 中单独准备，或使用项目已有的共享缓存机制。

## 本地 Squash Merge

开发 worktree 保持在开发分支。在主工作树中更新和合并目标分支：

```bash
git -C "$main_worktree" status --short
git -C "$main_worktree" switch <target-branch>
git -C "$main_worktree" fetch <remote> --prune
git -C "$main_worktree" pull --ff-only <remote> <target-branch>
git -C "$main_worktree" merge --squash <development-branch>
git -C "$main_worktree" commit -m "<type>(<scope>): <description>"
```

如果目标分支已在另一个 worktree 中检出，应在那个 worktree 中完成集成，不要强行重复检出。

## 安全清理

确认改动已合并、开发分支不再需要，并检查开发 worktree：

```bash
git -C "$worktree_path" status --short --branch
```

输出显示有修改或未跟踪文件时先处理，不使用 `--force` 跳过检查。工作区干净后，从主工作树或其他 worktree 执行：

```bash
git worktree remove "$worktree_path"
git branch -D <development-branch>
```

Squash Merge 生成新的提交，因此普通 `git branch -d` 可能拒绝删除开发分支。使用 `-D` 前必须确认 squash 提交已经进入目标分支。

若需要清理远程分支：

```bash
git push <remote> --delete <development-branch>
```

不要直接用 `rm -rf "$worktree_path"`。手动删除目录会留下 worktree 管理元数据。

## 恢复与排错

查看机器可读状态：

```bash
git worktree list --porcelain
```

预览可清理的陈旧元数据：

```bash
git worktree prune --dry-run --verbose
```

worktree 仍需保留但路径需要调整时：

```bash
git worktree move <old-path> <new-path>
```

目录已经被手动移动，或主工作树路径变化导致关联失效时：

```bash
git worktree repair <new-path>
```

目录已经被手动删除，并确认其中没有需要恢复的内容时：

```bash
git worktree prune --dry-run --verbose
git worktree prune --verbose
```

`prune` 会处理整个仓库的陈旧 worktree 元数据。检查 dry-run 输出中是否包含与当前任务无关、暂时离线或未挂载的 worktree；有疑问时先停止并确认。

遇到 locked worktree，先检查锁定原因：

```bash
git worktree list --verbose
```

只有确认不再需要锁定后才执行 `git worktree unlock <path>`。不要用多次 `--force` 绕过 locked 或 dirty worktree 的保护。

## 官方参考

- [git-worktree](https://git-scm.com/docs/git-worktree)
- [gitignore](https://git-scm.com/docs/gitignore)
- [git-clean](https://git-scm.com/docs/git-clean)
- [git-rev-parse](https://git-scm.com/docs/git-rev-parse)
