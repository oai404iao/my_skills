---
name: git-branch-development-workflow
description: Recommends branch- and worktree-based Git development for features, fixes, documentation, refactors, tests, chores, and other project changes. Use when changing a Git repository to create a scoped branch, isolate parallel work under .worktrees/, write Conventional Commits, verify the work, and integrate with Squash Merge through a PR/MR or a local merge according to project practice. 在 Git 项目中进行功能、修复、文档、重构、测试或维护改动时使用。
---

# Git Branch Development Workflow

在本地 Git 项目中进行代码、文档、配置或测试改动时，默认推荐使用独立分支开发。一个分支对应一个清晰、可独立合并的改动主题。

这是推荐工作流，不是阻塞开发的硬性限制。应优先遵循项目已有的 `AGENTS.md`、`CONTRIBUTING.md`、README、分支保护规则和团队约定。用户明确要求使用当前分支、项目不适合创建分支或操作环境受限时，可以继续工作，但要说明偏离了推荐流程。

需要并行处理任务、隔离无关改动或保留当前工作区上下文时，使用 linked worktree。没有项目级约定时，所有 linked worktree 统一放在主工作树根目录的 `.worktrees/` 下。执行 worktree 创建、恢复或清理前，读取 [Worktree 操作参考](references/worktrees.md)。

## 适用范围

以下改动都应优先使用独立分支：

- 新功能
- 缺陷修复
- 文档更新
- 代码重构
- 性能优化
- 测试增补或调整
- 构建和 CI 配置
- 依赖、工具或其他维护工作

只读检查、代码解释、搜索、日志查看等不修改项目的任务不需要创建分支。已经位于与当前任务匹配的独立分支时，应继续使用该分支，不要重复创建。

## 核心原则

1. 每个分支只处理一个逻辑主题，避免混入无关改动。
2. 修改前检查当前分支和工作区，不覆盖用户已有改动。
3. 分支名表达改动类型和目的。
4. 每条提交信息都必须符合 Conventional Commits 格式。
5. 合并默认采用 Squash Merge，使目标分支只新增一个代表本次改动的提交。
6. PR/MR 不是强制要求，是否使用取决于项目协作方式。
7. 没有远程仓库或项目允许本地集成时，可以执行本地 Squash Merge。
8. 不对共享或受保护分支执行强制推送。
9. 分支是改动和合并单元，worktree 只是工作目录隔离机制。
10. 同一分支只在一个 worktree 中检出，不使用 `--force` 绕过该保护。
11. 默认通过 `$GIT_COMMON_DIR/info/exclude` 忽略 `/.worktrees/`，不把本地工作流目录加入项目提交。

## 分支命名

优先沿用项目已有规范。没有明确规范时使用：

```text
<type>/<issue-id>-<short-description>
<type>/<short-description>
```

推荐映射：

| 改动类型 | 分支前缀 | Commit Type |
| --- | --- | --- |
| 新功能 | `feat/` | `feat` |
| 缺陷修复 | `fix/` | `fix` |
| 文档更新 | `docs/` | `docs` |
| 代码重构 | `refactor/` | `refactor` |
| 性能优化 | `perf/` | `perf` |
| 测试改动 | `test/` | `test` |
| 构建系统 | `build/` | `build` |
| CI 配置 | `ci/` | `ci` |
| 代码格式 | `style/` | `style` |
| 其他维护 | `chore/` | `chore` |

示例：

```text
feat/PROJ-123-user-export
fix/handle-empty-response
docs/update-installation-guide
refactor/simplify-token-parser
test/add-session-expiry-cases
chore/update-development-tools
```

命名要求：

- 前缀和描述部分使用小写。
- 任务编号保持项目原有格式，例如 `PROJ-123`。
- 描述中的单词使用连字符分隔。
- 名称简短、具体，避免只使用 `update`、`changes`、`new-feature` 等模糊名称。

## 分支与 Worktree 选择

根据当前状态选择开发位置：

- **已经位于匹配任务的独立分支**：继续使用当前工作树。
- **位于共享分支且工作区干净，当前只处理一个任务**：可以直接在当前工作树创建开发分支。
- **当前工作区存在与任务无关的改动**：保留原工作区，优先从已提交的目标分支创建 `.worktrees/<task-slug>`。
- **当前分支属于其他任务**：不要切走或混入改动，使用新的 linked worktree。
- **需要并行开发、验证或评审多个分支**：每个任务使用一个独立 linked worktree。
- **未提交改动全部属于当前任务**：优先在当前工作树直接创建分支；worktree 不会自动包含未提交改动。
- **开发分支已经由其他 worktree 检出**：进入已有 worktree，不重复创建，不使用 `--force`。

worktree 目录名使用开发分支名的可读 slug，通常把 `/` 替换为 `-`：

```text
branch:   feat/user-export
worktree: .worktrees/feat-user-export
```

## 推荐流程

### 1. 检查仓库状态

修改文件前执行：

```bash
git status --short --branch
git branch --show-current
git remote -v
git symbolic-ref --quiet --short refs/remotes/origin/HEAD
git worktree list --porcelain
```

确认：

- 当前目录是否为 Git 仓库。
- 当前分支是共享集成分支还是独立开发分支。
- 工作区是否存在未提交改动。
- 当前仓库是否已经有 linked worktree，以及目标分支是否已被检出。
- 实际目标分支是 `main`、`master`、`develop` 还是其他分支。
- 项目是否已有分支、提交、测试和合并规范。

不要仅根据分支名称猜测目标分支。优先使用项目文档、用户指定和远程默认分支。

### 2. 创建或选择开发分支与 Worktree

根据当前状态处理：

- **已经位于匹配当前任务的独立分支**：继续使用。
- **位于共享分支且工作区干净**：从最新目标分支创建新分支。
- **位于共享分支且未提交改动属于当前任务**：直接创建新分支，现有改动会随工作区保留。
- **存在与当前任务无关的改动**：不要自动 stash、reset、checkout 或覆盖；从已提交的目标分支创建 linked worktree。
- **位于其他任务的开发分支**：不要混合任务；从目标分支创建 linked worktree。

在当前工作树创建分支，有远程仓库且工作区干净时：

```bash
git fetch <remote> --prune
git switch <target-branch>
git pull --ff-only <remote> <target-branch>
git switch -c <type>/<short-description>
```

纯本地仓库：

```bash
git switch <target-branch>
git switch -c <type>/<short-description>
```

若当前未提交改动属于本次任务：

```bash
git switch -c <type>/<short-description>
```

如果用户选择不创建分支，不要阻塞任务；确认当前分支和风险后继续。

需要隔离时，在主工作树的 `.worktrees/` 下创建 linked worktree。有远程仓库时先获取远程状态；纯本地仓库跳过 `fetch`。然后定位主工作树和共享 Git 目录：

```bash
git fetch <remote> --prune

main_worktree="$(git worktree list --porcelain | sed -n '1s/^worktree //p')"
git_common_dir="$(git -C "$main_worktree" rev-parse --absolute-git-dir)"

mkdir -p "$git_common_dir/info"
touch "$git_common_dir/info/exclude"
grep -qxF '/.worktrees/' "$git_common_dir/info/exclude" ||
  printf '%s\n' '/.worktrees/' >> "$git_common_dir/info/exclude"
```

从远程目标分支创建开发分支和 worktree：

```bash
development_branch="<type>/<short-description>"
worktree_name="${development_branch//\//-}"
worktree_path="$main_worktree/.worktrees/$worktree_name"

git worktree add -b "$development_branch" \
  "$worktree_path" \
  "<remote>/<target-branch>"
```

纯本地仓库将最后一个参数替换为本地目标分支：

```bash
git worktree add -b "$development_branch" \
  "$worktree_path" \
  "<target-branch>"
```

创建后进入 `"$worktree_path"` 实施、验证和提交。不要在原工作树重复修改同一任务。若开发分支已经存在，按 [Worktree 操作参考](references/worktrees.md) 检查它是否已被其他 worktree 使用，再决定进入现有目录或挂载该分支。

### 3. 实施与验证

- 只修改与当前任务相关的文件。
- 不顺带提交其他任务或用户已有改动。
- 添加与改动风险相匹配的测试。
- 使用项目规定的格式化、静态检查、测试和构建命令。
- 提交前检查未暂存和已暂存差异。

```bash
git status --short
git diff
git add <relevant-files>
git diff --cached
```

不要默认使用 `git add .`。只有确认工作区全部改动都属于本次任务时才可使用。

### 4. 编写 Conventional Commits

每条提交信息使用：

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

示例：

```text
feat(auth): add passkey login
fix(api): handle empty upstream response
docs: update local installation guide
refactor(parser): simplify token handling
test(auth): cover expired sessions
chore(deps): update development dependencies
feat(api)!: remove deprecated user endpoint
```

要求：

- `type` 必须来自项目规范；没有项目规范时使用分支命名表中的类型。
- `scope` 可选，用于标识模块、包或子系统。
- `description` 应简短、具体，说明实际变化。
- 不使用 `update stuff`、`fix issue`、`changes` 等模糊描述。
- 一个提交只表达一个逻辑改动。
- 破坏性变更使用 `!`，并在需要时添加 `BREAKING CHANGE:` footer。
- Issue 或任务关联可放在 footer，例如 `Refs: #123`。

提交示例：

```bash
git commit -m "fix(api): handle empty upstream response"
```

开发分支允许存在多个符合规范的提交。最终 Squash 提交也必须符合 Conventional Commits。

### 5. 合并前同步

如果目标分支存在远程跟踪分支，在集成前获取最新状态：

```bash
git fetch <remote> --prune
git rebase <remote>/<target-branch>
```

若项目规定使用其他同步方式，应遵循项目规则。解决冲突后重新运行相关验证。

只有在当前开发分支由自己独占，且 rebase 后需要更新远程历史时，才可使用：

```bash
git push --force-with-lease
```

禁止使用裸 `--force`，禁止对共享分支强制推送。

## 合并方式

根据项目实际协作方式选择 PR/MR 或本地合并。不要为纯本地项目强行引入 PR/MR，也不要绕过项目已有的评审和分支保护流程。

### 方式一：通过 PR/MR 合并

适用于有远程托管、代码评审、CI 或分支保护的项目。

```bash
git push -u <remote> <development-branch>
```

PR/MR 标题使用 Conventional Commits，例如：

```text
fix(api): handle empty upstream response
```

描述至少包含改动摘要和验证结果。合并时选择托管平台提供的 Squash Merge，并确保最终提交信息仍符合 Conventional Commits。

GitHub CLI 示例：

```bash
gh pr merge --squash
```

GitLab 或其他平台使用等价的 squash 选项。使用 linked worktree 时，不要让托管工具在合并阶段自动删除仍被检出的本地开发分支；按“合并后清理”顺序处理。

### 方式二：本地 Squash Merge

适用于纯本地项目、个人项目，或明确允许本地集成的仓库。

先确认开发分支已提交并验证通过，然后在工作区干净的主工作树中切换到目标分支。使用 linked worktree 时，开发 worktree 保持在开发分支：

```bash
git switch <target-branch>
```

如果目标分支有远程跟踪分支，先更新目标分支：

```bash
git fetch <remote> --prune
git pull --ff-only <remote> <target-branch>
```

执行本地 Squash Merge，并使用符合 Conventional Commits 的最终提交信息：

```bash
git merge --squash <development-branch>
git commit -m "<type>(<scope>): <description>"
```

合并后按项目需要推送：

```bash
git push <remote> <target-branch>
```

若更新目标分支后开发分支出现冲突，应先切回开发分支同步并验证，不要在目标分支中草率解决后直接提交。

## 合并后清理

如果本任务使用 linked worktree，确认目标分支已经包含 Squash 提交，并且开发 worktree 工作区干净后，先移除 linked worktree：

```bash
git -C "$worktree_path" status --short
git worktree remove "$worktree_path"
```

不要直接使用 `rm -rf` 删除 worktree。`git worktree remove` 默认拒绝删除有未提交或未跟踪内容的 worktree；遇到这种情况先检查内容，不要直接加 `--force`。

未使用 linked worktree 时跳过上述步骤。移除 worktree 后，可以删除开发分支：

```bash
git branch -D <development-branch>
```

Squash Merge 会生成新的提交哈希，因此 Git 可能不允许使用普通 `git branch -d`。使用 `-D` 前必须确认改动已成功进入目标分支。

如果开发分支已推送到远程，并且项目策略要求清理：

```bash
git push <remote> --delete <development-branch>
```

## 异常情况

### 已在共享分支产生未提交改动

如果改动全部属于当前任务，创建新分支即可：

```bash
git switch -c <type>/<short-description>
```

### 已在共享分支提交但尚未推送

先基于当前提交创建开发分支。恢复共享分支会改写本地状态，执行前必须确认提交范围和用户意图，不得盲目执行 `reset`。

### 当前环境无法创建分支

说明原因和风险后继续完成用户请求。不要因为推荐流程无法执行而停止必要的代码修改。

### Worktree 路径丢失或被移动

先检查：

```bash
git worktree list --porcelain
git worktree prune --dry-run
```

路径被移动时优先使用 `git worktree move`；已经手动移动时使用 `git worktree repair <path>`。目录已被手动删除且确认不再需要时，再执行 `git worktree prune` 清理陈旧元数据。

`git worktree prune` 会检查整个仓库的 linked worktree 元数据。执行前先使用 `--dry-run`，避免清理与当前任务无关但暂时离线、未挂载或未正确锁定的 worktree。

### 项目明确要求其他合并策略

项目规则优先。使用项目要求的合并方式，并明确说明没有采用默认 Squash Merge。

## 完成标准

- 已优先考虑并采用与任务匹配的独立分支。
- 分支只包含一个逻辑主题。
- 所有提交信息符合 Conventional Commits。
- 相关格式化、检查、测试或构建已执行并报告。
- 根据项目选择 PR/MR 或本地合并。
- 默认使用 Squash Merge，最终提交信息符合 Conventional Commits。
- 未覆盖、丢弃或混入用户的无关改动。
- 使用 linked worktree 时，目录位于主工作树的 `.worktrees/` 下，并已通过本地 exclude 忽略。
- 合并完成后，相关 worktree 已安全移除，未留下待处理改动或陈旧元数据。

## 参考

- [Worktree 操作参考](references/worktrees.md)
- [Git 官方 `git-worktree` 文档](https://git-scm.com/docs/git-worktree)
- [Git 官方 `gitignore` 文档](https://git-scm.com/docs/gitignore)
- [Git 官方 `git-clean` 文档](https://git-scm.com/docs/git-clean)
- [Git 官方 `git-rev-parse` 文档](https://git-scm.com/docs/git-rev-parse)
