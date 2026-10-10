# Git 分支与合并

命令细节、rebase 与 force-push 边界、冲突处理和清理排错。主流程和默认约定见 [开发流程指南](../SKILL.md)。

## 侦察现状

```bash
git status --short --branch
git branch --show-current
git remote -v
git worktree list --porcelain
git log --oneline --decorate -10
```

用途：

- `status --short --branch` 同时给出当前分支和未提交改动，是每次动手前的第一命令。
- `worktree list --porcelain` 在非隔离场景也值得运行：开发分支可能已经被另一个 worktree 检出。
- `log --decorate` 确认集成分支当前的顶端，避免基于过期的本地状态开分支。

有远程仓库时，用远程默认分支核对集成分支名，不要凭 `main` / `master` 的印象猜：

```bash
git symbolic-ref --quiet --short refs/remotes/<remote>/HEAD
```

## 创建与切换分支

工作区干净、需要从最新集成分支开始时：

```bash
git fetch <remote> --prune
git switch <integration-branch>
git pull --ff-only <remote> <integration-branch>
git switch -c <type>/<short-description>
```

已有属于本任务的未提交改动时，直接 `git switch -c` 即可，改动会随工作区保留，不需要先提交或 stash。

创建前检查同名分支和 worktree：

```bash
git branch --list "<type>/<short-description>"
git worktree list --porcelain
```

分支已存在时继续用它，不要重复创建；分支已被其他 worktree 检出时，进入那个目录工作，不要用 `--force` 让同一分支出现在两处。

## rebase 的边界

同步集成分支：

```bash
git fetch <remote> --prune
git rebase <remote>/<integration-branch>
```

可以 rebase：

- 只有自己使用的本地开发分支。
- 尚未推送，或推送后确定没有别人基于它工作的分支。

不要 rebase：

- 集成分支、受保护分支、共享分支。
- 已被其他分支合并或已被别人拉取过的历史。
- 仅仅为了去掉 `Merge branch ...` 提交而改写已经推送的公共历史。

会改写历史的操作交给用户决定，不要自作主张。从异常情况恢复到需要改写集成分支历史时，先确认提交范围和用户意图。

## force-push 边界

rebase 过自己的开发分支、确实需要更新远程副本时：

```bash
git push --force-with-lease <remote> <development-branch>
```

约束：

- 只用 `--force-with-lease`，不要用裸 `--force` 或 `--force-with-lease=<ref>` 覆盖掉保护。
- 不对集成分支、受保护分支或共享分支强制推送。
- 推送前先 `git fetch`，否则 `--force-with-lease` 的比较基准可能是过期的。

## 冲突处理

冲突在自己的开发分支上解决：

```bash
git status                 # 查看冲突文件
# 逐个编辑并保留双方需要的语义，不是简单取一侧
git add <resolved-files>
git rebase --continue      # 或 git merge --continue
```

放弃并回到操作前：

```bash
git rebase --abort
git merge --abort
```

解决冲突后重新运行受影响的格式化、静态检查、测试和构建——冲突解决可能悄悄改变行为，不能用解决前的验证结果代替。

不要切到集成分支上草率解决冲突后直接提交，那会把未经验证的合并结果写进主干。

## 合并回集成分支

**PR/MR 路径**：创建 PR/MR 是默认“不推送开发分支”规则的唯一例外，完成后必须清理。

```bash
git push -u <remote> <development-branch>
gh pr merge --squash
```

平台的“合并后自动删除分支”建议关掉：它会在本地清理之前删除远端分支，容易留下一串无法删除的本地分支引用。

**本地 Squash Merge 路径**：在主工作树操作，集成分支工作区必须干净。

```bash
git -C <main-worktree> switch <integration-branch>
git -C <main-worktree> fetch <remote> --prune
git -C <main-worktree> pull --ff-only <remote> <integration-branch>
git -C <main-worktree> merge --squash <development-branch>
git -C <main-worktree> commit -m "<type>(<scope>): <description>"
git push <remote> <integration-branch>
```

`merge --squash` 只暂存改动，不产生提交，必须紧跟一次 `git commit`，且提交信息要符合 Conventional Commits。

## 清理排错

### `git branch -d` 拒绝删除

Squash Merge 产生的哈希与开发分支上的提交不同，`-d` 会认为未合并而拒绝：

```text
error: the branch 'feat/x' is not fully merged
```

先确认 squash 提交已进入集成分支，再用 `-D`：

```bash
git -C <main-worktree> log --oneline --grep="<squash 提交的 subject>" <integration-branch>
git branch -D <development-branch>
```

`-D` 会无条件丢弃分支引用，确认不了就不要执行。

### 误删分支的恢复

删除后短时间内可以从 reflog 找回：

```bash
git reflog --date=iso
git branch <development-branch> <sha>
```

reflog 有有效期，且只保存在本地克隆中，不要把它当备份。

### 远端分支删除失败

受保护分支或平台权限限制会拒绝删除：

```bash
git push <remote> --delete <development-branch>
```

失败时先在平台上解除保护或确认权限，不要改用改写历史的绕行手段。

### worktree 元数据陈旧

目录被手动移动或删除后：

```bash
git worktree list --porcelain
git worktree prune --dry-run --verbose
```

确认 dry-run 输出里只有本任务的陈旧条目，再执行：

```bash
git worktree prune --verbose
```

### 清理后的核对

```bash
git branch --list
git worktree list
git status --short --branch
```

确认开发分支、worktree 和未提交改动都已按预期消失或保留。

## 官方参考

- [git-branch](https://git-scm.com/docs/git-branch)
- [git-switch](https://git-scm.com/docs/git-switch)
- [git-rebase](https://git-scm.com/docs/git-rebase)
- [git-merge](https://git-scm.com/docs/git-merge)
- [git-push](https://git-scm.com/docs/git-push)
- [git-reflog](https://git-scm.com/docs/git-reflog)
