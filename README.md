# my_skills

个人维护的 Agent Skills 单仓库。每个 skill 独立存放；本仓库是维护来源，安装目录只是分发副本。

## 可用 Skills

| Skill | 用途 |
| --- | --- |
| [api-design](api-design/SKILL.md) | HTTP API 命名、批量写入、初始化、检索、上传、分页及兼容迁移；按需读取 SM2+SM4 加密实现契约及风险 |
| [agents-md](agents-md/SKILL.md) | 按项目证据创建、更新、审查或重设计仓库指令；按需处理 Codex / Claude Code 兼容性、指令分层与行为复核 |
| [bruno](bruno/SKILL.md) | GUI for humans, files for AI to edit, CLI for execution: Bruno request/environment/test formats, CLI usage, and official sources |
| [frontend-design](frontend-design/SKILL.md) | 完整迁入 ikadesign3 的强制 design.md 流程：提取、创建、实现与审查 |
| [development-workflow](development-workflow/SKILL.md) | 开发流程指南：Git 分支与提交、实施与自检、测试验证分级、版本与发布；worktree 仅按需隔离 |
| [deployment-standards](deployment-standards/SKILL.md) | Linux/systemd/Compose deployment standards: system and user/XDG layouts, identities, lifecycle/linger, backup, recovery, and acceptance |
| [llm-prompt-design](llm-prompt-design/SKILL.md) | 按任务设计、比较与评估 LLM 提示词；区分生图/非生图，以及工具和结构化响应契约 |
| [paseo-pi-team](paseo-pi-team/SKILL.md) | 仅显式调用的 Paseo + Pi 双层开发团队：独立监督、原生 worktree 隔离、持续集成、验证与授权回收 |

## 安装

通过 Skills CLI 查看和安装已发布到远程仓库的版本：

```bash
npx skills add oai404iao/my_skills --list
npx skills add oai404iao/my_skills --skill api-design
npx skills add oai404iao/my_skills --skill agents-md
npx skills add oai404iao/my_skills --skill bruno
npx skills add oai404iao/my_skills --skill frontend-design
npx skills add oai404iao/my_skills --skill development-workflow
npx skills add oai404iao/my_skills --skill deployment-standards
npx skills add oai404iao/my_skills --skill llm-prompt-design
npx skills add oai404iao/my_skills --skill paseo-pi-team
```

交互式安装会选择目标 Agent 和安装范围。远程安装不包含本地尚未发布的修改。

当前工作树的 `frontend-design` 直接迁入了 Ikaleio 的原文，其适用的再分发许可尚未确认。发布或分发该版本前须明确授权；不要把安装命令或公开源码当成许可声明。详见 [来源说明](frontend-design/references/sources.md)。

本地验证后，可以将对应 skill 目录同步到实际安装目录。同步前检查目标是否有本地修改；同步该 skill 的入口和必要引用文件，不复制整个仓库，也不覆盖其他 skills。

### 仅显式调用：paseo-pi-team

该 skill 声明 `disable-model-invocation: true`：Pi 可注册它，但不会将它加入模型的自动选择列表。安装后使用显式命令，不因任务较大就自动启动团队：

```text
/skill:paseo-pi-team 项目路径：{{路径}}；任务目标：{{目标}}；验收结果：{{结果}}；明确不做：{{排除项}}；其他约束：{{约束}}
```

`{{...}}` 替换为本次任务信息。在仓库根目录运行 `pi --skill ./paseo-pi-team`，可仅向该次 Pi 会话提供本地未发布版本，不修改全局配置；随后仍需显式调用。实际执行需当前会话可用的 Paseo 原生能力，普通独立 Pi 会话不一定具备。

该字段的行为以 [Pi 官方 Skills 文档](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md) 为依据；不保证其他宿主支持同样的自动加载限制。详见 [来源与验证边界](paseo-pi-team/references/sources.md)。

## 仓库结构

```text
my_skills/
├── README.md                  # 技能目录、安装和维护说明
├── AGENTS.md                  # 本仓库维护约定
├── prompts/
│   ├── coding-principles.md   # 可选公共指令，不是可安装的 skill
│   └── pi-global-agents.md    # Pi 全局指令，由 chezmoi 分发
├── api-design/
│   ├── SKILL.md
│   └── references/
│       ├── application-encryption.md
│       └── sm2-sm4.md
├── agents-md/
│   ├── SKILL.md
│   └── references/
│       ├── host-compatibility.md
│       ├── instruction-design.md
│       ├── repository-patterns.md
│       ├── review-scenarios.md
│       └── sources.md
├── frontend-design/
│   ├── SKILL.md
│   └── references/
│       ├── design-contract.md
│       ├── build-workflow.md
│       ├── review-loop.md
│       └── sources.md
├── bruno/
│   ├── SKILL.md
│   └── references/
│       ├── file-format.md
│       ├── cli.md
│       └── sources.md
├── development-workflow/        # 开发流程指南：git / 开发 / 测试 / 版本发布
│   ├── SKILL.md
│   └── references/
│       ├── git-workflow.md
│       ├── development.md
│       ├── testing.md
│       ├── versioning.md
│       └── worktrees.md
├── deployment-standards/
│   ├── SKILL.md
│   └── references/
│       ├── runtime-layout.md
│       ├── user-services-xdg.md
│       ├── backup-management.md
│       ├── release-and-recovery.md
│       └── sources.md
├── llm-prompt-design/
│   ├── SKILL.md
│   └── references/
│       ├── foundations.md
│       ├── strategy-selection.md
│       ├── tasks/
│       │   ├── non-gen-image.md
│       │   └── gen-image.md
│       ├── interfaces/
│       │   ├── tool-schema.md
│       │   └── structured-output.md
│       ├── engineering/
│       │   ├── evaluation.md
│       │   └── provider-compatibility.md
│       └── sources.md
└── paseo-pi-team/
    ├── SKILL.md                 # Pi 仅显式调用
    └── references/
        ├── supervision.md
        ├── workspaces.md
        └── sources.md
```

新增 skill 使用根目录下的 `<skill-name>/SKILL.md`。只有确有需要时才添加 `references/`、`scripts/`、`assets/` 和测试；不为凑齐模板创建空目录。

## 纳入来源

`agents-md` 依据 AGENTS.md 官方格式、OpenAI Codex / Anthropic Claude Code 文档、GPT-6 Astra / Claude Opus 5.5 提示指南及五个 GitHub 仓库快照独立重设计。入口保留必要流程，宿主差异、模型适配、组织样例与验收场景按需读取；不复制上游指令正文，也不把其他项目的政策强加给目标仓库。具体来源、固定提交与未实测边界见 [来源说明](agents-md/references/sources.md)。

`bruno` is independently authored from Bruno's official source code and documentation, following "GUI for humans, files for AI to edit, CLI for execution." The main skill defines task and authorization boundaries; references cover Bru / OpenCollection YAML formats, CLI commands, and project links on demand. See [Sources](bruno/references/sources.md) for pinned commits, documentation conflicts, and licensing boundaries.

`frontend-design` 当前完整迁入 `Ikaleio/skills` 的 `ikadesign3`（固定提交 `5276d6e`），保留其强制 design.md 前置、测量记录、规则标签、实现绑定和单次复查流程；适配技能名称与来源引用，并按用户要求加入少用口径、脚注和底部说明的文案约束。上游检查规则的已知冲突原样保留并另行记录。此前 Anthropic 版本的来源也保留在 [来源说明](frontend-design/references/sources.md)；来源仅供追溯，不代表再分发许可、统一授权或上游背书。

`development-workflow`（原 `git-branch-development-workflow`）由本机原有 skill 调整而来：默认改为分支开发而非 worktree、默认只推送集成分支、合并后同步清理本地与远端开发分支，并新增按社区实践（SemVer、Conventional Commits、Keep a Changelog、release-please/semantic-release/changesets）整理的版本发布指引。原有 worktree 参考文档保留为按需读取的隔离方案。本地来源未附带许可证声明。

`deployment-standards` is independently written from the user-provided `ai_server_info` deployment archive and primary references from FHS, Borg, restic, CISA, XDG, and systemd. It separates reusable Linux/systemd/Compose deployment guidance from machine-specific migration decisions, rehearsal isolation, and historical status. References cover system runtime layout, [user services and XDG](deployment-standards/references/user-services-xdg.md), [backup placement and management](deployment-standards/references/backup-management.md), release/recovery, and [sources and scope](deployment-standards/references/sources.md). It does not bundle private configuration, business data, or operational scripts.

`llm-prompt-design` 依据 OpenAI、Anthropic、Google 示例及 DAIR.AI 资料独立编写；采用主题、来源及许可说明见 [来源说明](llm-prompt-design/references/sources.md)。图像提示词七槽位公式来自本仓库维护任务，不作为第三方标准。

`paseo-pi-team` 由用户提供的双层 Agent 团队 prompt 整理而来，参考 Agent Skills 官方规范、编写教程及 Pi 的显式调用机制；保留原生 workspace、监督 heartbeat、授权和交付边界。未附带自动化脚本，不会因安装而自动启动团队；来源和未实测范围见 [来源说明](paseo-pi-team/references/sources.md)。

## 维护规范

- **入口清楚**：`SKILL.md` 包含 YAML frontmatter，至少声明与目录一致的 `name` 和明确的 `description`。说明何时触发、何时不适用。
- **按需读取**：入口保留任务边界和必要流程；长示例与领域细节放入引用文件，由入口说明读取时机。
- **独立可用**：引用路径相对 skill 目录解析。不依赖本机绝对路径、未提供的代理名称或未经检查的宿主能力。
- **规则有范围**：区分 API/数据约束、项目政策与默认建议。skill 不应把默认偏好强制写入目标项目，也不应扩大用户授权。
- **单一维护来源**：先修改本仓库并验证，再更新安装副本。发现安装副本有独立修改时，先比较，不直接覆盖。
- **保留来源**：引入第三方内容时记录来源，保留适用的许可证和署名，不将第三方授权扩展到整个仓库。
- **同步目录**：新增、删除或重命名 skill 时，同时更新 README、内部链接及受影响的安装记录。

## 验证

文档和提示修改先检查差异：

```bash
git diff --check
git diff --stat
git diff
```

再确认 frontmatter、引用路径、命令示例和 README 目录一致。行为规则变更使用少量代表性场景复核，例如：

- 只请求审查时，不写入文件。
- 只更新一条命令时，不改写整份 AGENTS 或添加通用政策。
- 项目没有某项约定时，不将 skill 的默认偏好声明为项目规则。

存在可执行脚本时，保留覆盖真实行为的必要测试，并在该 skill 中说明运行方法。纯文档修改不要求全量构建；删除功能时清理对应测试、依赖和说明。

## 可选公共指令

[coding-principles.md](prompts/coding-principles.md) 提炼了最小改动、合理自主性和适度验证等编码原则。

它不是 skill，也不会因安装本仓库或读取本仓库的 `AGENTS.md` 自动全局生效。需要时，仅将其中的“指令正文”接入实际宿主的用户级指令；接入前检查已有规则是否重复。确认接入后，再考虑停用原 `karpathy-guidelines` skill。

### Pi 全局指令

[pi-global-agents.md](prompts/pi-global-agents.md) 是 Pi 全局指令的唯一维护来源，
包含编码原则、agent 派工、工具偏好与临时目录约定。它不是通用 skill，
派工规则依赖当前 Pi subagent 工具；不会因安装 skills 自动生效。

在这里修改并发布到远程 `main` 后，dotfiles 仓库的 `.chezmoiexternal.toml`
通过 HTTPS 获取该文件，部署为 `~/.config/pi/agent/AGENTS.md`（`0600`）。
刷新周期为 24 小时，不是后台定时同步；本地未推送的修改不会被获取。
跟随 `main` 意味着后续应用可能改变全局指令，应先审查差异。

备份已有目标后，可在配置好 dotfiles 的机器上手动刷新、审查并应用：

```sh
chezmoi diff --refresh-externals=always --skip-secrets --exclude=scripts,encrypted \
  ~/.config/pi/agent/AGENTS.md
chezmoi apply --refresh-externals=never --exclude=scripts,encrypted \
  ~/.config/pi/agent/AGENTS.md
```

第二条命令使用刚审查的缓存。首次获取需要网络；不要直接修改部署副本或在
dotfiles 中另存一份正文。应用后用 Pi 的 `/reload` 或新会话加载。
