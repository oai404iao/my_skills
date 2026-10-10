---
name: development-workflow
description: Git 开发流程规范，覆盖分支、提交、测试验证、合并清理与版本发布。Use when making changes in a Git repository - creating branches, writing Conventional Commits, deciding what to verify before merging, squash merging back to the integration branch, cleaning up branches and worktrees, or bumping versions, tagging releases, and updating a changelog. 用户要求隔离并行开发时按需读取 worktree 参考。
---

# 开发流程指南

对 Git 仓库做功能、修复、文档、重构、测试或维护改动时，按本指南组织流程：**分支开发 → 验证 → Squash Merge 回集成分支 → 清理 → 需要时发布版本**。

这是默认流程，不是阻塞开发的硬性限制。项目已有的 `AGENTS.md`、`CONTRIBUTING.md`、分支保护规则和团队约定优先；用户明确要求在当前分支工作、项目不适合建分支或环境受限时继续完成请求，但要说明偏离了什么。

## 默认约定

以下四项是本指南与常见做法最容易出现分歧的地方，先明确默认值：

1. **分支，不是 worktree**：默认在当前工作树用 `git switch -c` 创建开发分支。只有用户要求隔离、需要并行处理多个任务、或当前工作区的无关改动不该被打断时，才使用 linked worktree（见 [Worktree 隔离开发](references/worktrees.md)）。
2. **只推送集成分支**：默认不推送开发分支到远程。开发分支在本地完成后直接合并，减少一次推送和一次远端清理。
3. **合并后立即清理**：Squash Merge 成功即删除开发分支；用过 worktree 的连 worktree 一起删；确实推送过开发分支的，同步删除远端分支。
4. **合并默认 Squash Merge**：集成分支每次整合只新增一个代表改动的提交，主干历史保持可读。

只读检查、代码解释、搜索、日志查看等不修改仓库的任务不需要分支、提交或发布。

## 流程

### 1. 侦察现状

改文件之前先确认状态，不要凭分支名猜测：

```bash
git status --short --branch
git branch --show-current
git remote -v
```

确认当前目录是 Git 仓库、当前分支是集成分支还是其他任务的开发分支、工作区有没有未提交改动、集成分支到底叫 `main`、`master`、`develop` 还是别的名字。集成分支以项目文档、用户指定和远程默认分支为准。

### 2. 创建开发分支

一个分支一个逻辑主题。

```bash
git fetch <remote> --prune
git switch <integration-branch>
git pull --ff-only <remote> <integration-branch>
git switch -c <type>/<short-description>
```

分支名沿用项目规范；没有规范时用 `<type>/<short-description>`，前缀与 commit type 一致：`feat/`、`fix/`、`docs/`、`refactor/`、`perf/`、`test/`、`build/`、`ci/`、`style/`、`chore/`。有任务编号时写成 `feat/PROJ-123-user-export`。

已经位于匹配当前任务的开发分支就继续用，不要重复建。工作区已有属于本任务的未提交改动时，可直接 `git switch -c <branch>`，改动会保留。工作区有**与任务无关**的改动时，不要 stash / reset / checkout 覆盖：要么先处理它们，要么改用 worktree 隔离，不要混入本次提交。

### 3. 实施与验证

只改与任务相关的文件，不顺带提交其他人的改动，不要默认 `git add .`。改动完成后运行项目规定的格式化、静态检查、测试和构建；验证强度按 [测试与验证](references/testing.md) 的风险分级选择。改动范围控制和提交前自检见 [实施与提交](references/development.md)。

提交信息必须符合 Conventional Commits：

```text
<type>[optional scope][!]: <description>
```

例如 `fix(api): handle empty upstream response`。一个提交一个逻辑改动，不用 `update stuff`、`fix issue` 这类模糊描述，破坏性变更用 `!` 并补 `BREAKING CHANGE:` footer。

### 4. 同步集成分支

合并前确认开发分支基于最新集成分支，然后重新运行受影响的验证：

```bash
git fetch <remote> --prune
git rebase <remote>/<integration-branch>
```

冲突在自己分支上解决。不要切到集成分支草率解决冲突后直接提交。rebase 与 force-push 的边界见 [Git 分支与合并](references/git-workflow.md)。

### 5. 合并回集成分支

**有远程托管时**（默认路径）：

```bash
git push -u <remote> <development-branch>   # 仅在需要 PR/MR 评审时推送
# 平台上选择 Squash Merge
```

PR/MR 标题用 Conventional Commits 格式，描述至少写改动摘要和验证结果。GitHub CLI 示例：`gh pr merge --squash`。

**纯本地项目、个人项目或明确允许本地集成**：

```bash
git -C <main-worktree> switch <integration-branch>
git -C <main-worktree> pull --ff-only <remote> <integration-branch>
git -C <main-worktree> merge --squash <development-branch>
git -C <main-worktree> commit -m "<type>(<scope>): <description>"
git push <remote> <integration-branch>
```

创建 PR/MR 时必须推送开发分支，这是默认规则里唯一的例外，任务结束就删掉它。托管平台的"合并后自动删除分支"要关掉：它会抢在本地清理之前动手，留下删不掉的本地分支。

### 6. 合并后清理

先确认 Squash 提交已经进入集成分支，再按顺序清理：

```bash
git worktree remove <worktree-path>              # 用过 worktree 时，先删目录
git branch -D <development-branch>               # Squash 后哈希已变，-d 通常拒绝
git push <remote> --delete <development-branch>  # 只清理推送过的分支
```

`-D` 之前必须确认改动已经进集成分支，否则会丢提交。不要用 `rm -rf` 删 worktree；也不要为了省事给 `git worktree remove` 加 `--force` 绕过脏工作区检查，先看里面有什么。

### 7. 版本发布（按需）

任务需要对外交付、集成分支要打发布标记，或项目要求维护 CHANGELOG 时，读取 [版本与发布](references/versioning.md)：按 SemVer 决定版本号，用注解 tag 标记，更新 CHANGELOG。

## 异常情况

- **已在集成分支提交但未推送**：从当前提交建开发分支继续。改写集成分支历史前必须确认提交范围和用户意图，不盲目 `reset`。
- **开发分支已推送过**：合并后在本地和远端都删除；确实需要保留时说明理由，不要留下无意的孤儿分支。
- **无法建分支或建 worktree**：说明原因和风险后继续完成请求，不要因为流程执行不了就停下。
- **项目要求其他合并策略**：项目规则优先，明确说明没有采用默认 Squash Merge。策略会影响发布标记的落点，改策略时同步检查 [版本与发布](references/versioning.md)。

## 完成标准

- 改动位于与任务匹配的独立分支，且分支只包含一个逻辑主题。
- 提交信息符合 Conventional Commits，未混入无关改动。
- 运行过的格式化、检查、测试或构建已如实报告，未运行的没有被说成通过。
- 已通过 PR/MR 或本地 Squash Merge 整合，集成分支只新增一个代表本次改动的提交。
- 开发分支已删除，用过的 worktree 已移除，推送过的开发分支已从远端删除。
- 需要发布时，版本号、注解 tag 和 CHANGELOG 一致，且与集成分支上的实际改动匹配。

## 参考

- [Git 分支与合并](references/git-workflow.md)：命令细节、rebase 与 force-push 边界、冲突处理和清理排错。
- [实施与提交](references/development.md)：改动范围控制、提交前自检、如何报告完成情况。
- [测试与验证](references/testing.md)：按风险分级选择验证强度，以及不能跳过的验证项。
- [版本与发布](references/versioning.md)：SemVer 决策、注解 tag、CHANGELOG 与发布步骤。
- [Worktree 隔离开发](references/worktrees.md)：仅在需要隔离并行任务时读取。
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Semantic Versioning 2.0.0](https://semver.org/)
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
