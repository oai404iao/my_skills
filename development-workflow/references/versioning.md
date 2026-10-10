# 版本与发布

按需读取。任务需要对外交付、要在集成分支打发布标记，或项目维护 CHANGELOG 时，按本参考执行。

约定来自社区通行实践：[Semantic Versioning 2.0.0](https://semver.org/)、[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)、[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)，以及 release-please、semantic-release、changesets 这几类工具的主流做法。项目已有的发布流程、版本方案（含 CalVer）和发布记录优先于本参考。

## 版本号决策

格式 `MAJOR.MINOR.PATCH`：

| 变更 | 版本位 | 判断依据 |
| --- | --- | --- |
| 不兼容的 API 或行为变更 | MAJOR | 提交带 `!` 或 `BREAKING CHANGE:` footer |
| 向后兼容的新功能 | MINOR | `feat` |
| 向后兼容的修复或内部改进 | PATCH | `fix`、`perf`、`refactor`、`docs` 等 |

判断看对外契约，不看提交数量或代码量：

- 内部重构、脚手架调整、测试补充、文档修正通常是 PATCH，即使改动很大。
- 修改默认值、收紧校验、改变错误码、删除已废弃的导出，都可能是 MAJOR，即使只有一行。
- 安全修复按常规规则定级，必要时在 CHANGELOG 的 `Security` 分类下单独说明，但不要借安全为名回避 MAJOR 判断。
- 多个变更同时发布时取最高位：只要包含一个破坏性变更，就是 MAJOR。

`0.y.z` 阶段：`0.y.z` 中 MINOR 可以包含破坏性变更，PATCH 仍应保持兼容。是否把 `0.x` 的破坏性变更提升成 MAJOR，取决于项目文档的声明；项目没有声明时按此约定，并在发布说明里写清影响。

预发布版本用 `-alpha.1`、`-beta.2`、`-rc.1` 之类的后缀。预发布版本排在对应正式版本之前，且不同时推进多个预发布标识。

## 版本记录在哪里

- 语言的包清单：`package.json`、`pyproject.toml`、`Cargo.toml`、`pom.xml`、`*.gemspec`。
- 单独的 `VERSION`、`version.go`、`__version__`。
- 项目文档里的版本徽章或引用。

发布时同步更新所有记录版本号的位置。只改一处会留下不一致，下游按包清单安装得到的版本和 tag 不同。

## Tag

在集成分支上打注解 tag：

```bash
git switch <integration-branch>
git pull --ff-only <remote> <integration-branch>
git tag -a v1.4.0 -m "v1.4.0"
git push <remote> v1.4.0
```

规则：

- 用 `-a` 创建注解 tag，不要用轻量 tag。注解 tag 带作者、日期和说明，`git describe` 和多数发布工具依赖这些信息。
- 命名沿用项目既有格式（`v1.4.0` 或 `1.4.0`），不要混用。
- tag 指向集成分支上实际发布的那个提交，通常就是本次发布的版本提交。
- 已推送的 tag 不要移动或覆盖。下游可能已经按它构建；需要修正时发新的 PATCH 版本，而不是改旧 tag。
- 打错且尚未推送时，直接删除重打：
  ```bash
  git tag -d v1.4.0
  ```
- 团队要求签名时用 `git tag -s`，并确认本地签名密钥已配置。

## CHANGELOG

按 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 的格式维护，面向使用者而不是面向提交历史：

```markdown
## [Unreleased]

## [1.4.0] - 2025-03-11

### Added
- 支持通过 `--format json` 导出结果

### Changed
- 默认超时从 30 秒调整为 10 秒

### Fixed
- 修复空响应体导致的解析失败

### Security
- 升级存在已知漏洞的解析依赖
```

要点：

- 分类使用 `Added` / `Changed` / `Deprecated` / `Removed` / `Fixed` / `Security`，不添加自定义分类。
- 条目写用户可见的变化，不逐条抄提交信息。Squash Merge 让一个 PR/MR 对应一条，正好匹配这种粒度。
- 每个发布版本一个二级标题，带日期和版本号，最新的在上方。
- 保留 `Unreleased` 小节，日常改动先记在那里。
- 破坏性变更单列 `Removed` / `Changed` 并在条目中说明迁移方式。
- 底部保留版本对比链接（若项目使用）。

## 发布步骤

手动发布的完整顺序：

```bash
# 1. 确认集成分支包含本次全部改动且工作区干净
git -C <main-worktree> switch <integration-branch>
git -C <main-worktree> pull --ff-only <remote> <integration-branch>
git -C <main-worktree> status --short

# 2. 更新版本号（包清单、VERSION 等所有记录位置）

# 3. 把 Unreleased 的内容移入新的版本小节，更新对比链接

# 4. 提交版本改动
git add CHANGELOG.md pyproject.toml
git commit -m "chore(release): 1.4.0"

# 5. 打注解 tag
git tag -a v1.4.0 -m "v1.4.0"

# 6. 推送集成分支和 tag（tag 可精确推送，避免顺带推送无关 tag）
git push <remote> <integration-branch>
git push <remote> v1.4.0
```

推送 tag 前运行项目的构建或打包检查。发布后核对 tag 指向的提交包含版本提交，且 CHANGELOG 的版本号、tag 名和包清单三处一致。

## 自动化方案

社区主流有三类，按项目的提交规范和产物形态选择：

- **release-please**：由 Conventional Commits 推断版本位，生成一个“发布 PR”，里面包含版本号和 CHANGELOG 改动；合并该 PR 后创建 tag 和 release。适合希望发布前仍有人工确认的项目，对 GitHub 支持最完整。
- **semantic-release**：在 CI 上全自动完成版本推断、CHANGELOG 生成、打 tag 和发布。适合提交规范执行严格、希望零人工干预的项目；配置失误会直接影响发布产物，首次接入要先在预发布分支验证。
- **changesets**：以显式的变更文件描述改动，再由命令汇总版本和 CHANGELOG。适合 monorepo 或多包仓库，需要跨包协调版本时优势明显。

共同前提是提交信息符合 Conventional Commits——这也是本指南要求提交规范的直接原因。接入自动化前先确认项目历史提交的规范程度，否则自动生成的版本号和 CHANGELOG 会失真。

工具选定后写进项目文档和 CI 配置，不要在同一仓库并行维护两套发布机制。

## 与合并策略的关系

- 默认的 Squash Merge 让一个 PR/MR 在集成分支上只留一个提交，正好对应一条 CHANGELOG 条目和一次版本判断。
- 若项目改用 Rebase Merge 或普通 Merge，集成分支会累积开发分支的中间提交，自动版本推断会把 `wip`、`fix typo` 之类的提交也算进去。此时要么在合并前整理提交，要么改用显式变更文件（changesets 方式）。
- 合并策略变更后重新检查版本工具的依据来源：从提交信息推断的工具依赖 squash 粒度。

## 常见错误

- 版本号改了一处，漏掉包清单或 `__version__`。
- 用轻量 tag，导致发布工具读不到 tag 说明。
- 移动或强制覆盖已发布的 tag。
- CHANGELOG 直接罗列提交信息，或长期不更新，发布时才补写。
- 破坏性变更只写在提交里，没有出现在 CHANGELOG 和版本位上升级。
- 在开发分支上打 tag 后合并，导致 tag 指向未进入主干的提交。
- 自动化接管后仍手工改版本号，造成工具与文件冲突。

## 官方参考

- [Semantic Versioning 2.0.0](https://semver.org/)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- [release-please](https://github.com/googleapis/release-please)
- [semantic-release](https://semantic-release.gitbook.io/semantic-release/)
- [changesets](https://github.com/changesets/changesets)
