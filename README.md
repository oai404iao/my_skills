# my_skills

个人维护的 Agent Skills 单仓库。每个 skill 独立存放；本仓库是维护来源，安装目录只是分发副本。

## 可用 Skills

| Skill | 用途 |
| --- | --- |
| [api-design](api-design/SKILL.md) | HTTP API 命名、批量写入、初始化、检索、上传、分页及兼容迁移；按需读取 SM2+SM4 加密实现契约及风险 |
| [agents-md](agents-md/SKILL.md) | 根据项目证据创建、更新或审查 Agent 仓库指令，避免传播未经确认的通用政策 |
| [frontend-design](frontend-design/SKILL.md) | 参考 Anthropic 指引的前端设计技能，强调主体特征、排版、克制表达与可用交互 |
| [git-branch-development-workflow](git-branch-development-workflow/SKILL.md) | 分支开发、worktree 隔离、验证、提交和合并流程 |

## 安装

通过 Skills CLI 查看和安装已发布到远程仓库的版本：

```bash
npx skills add oai404iao/my_skills --list
npx skills add oai404iao/my_skills --skill api-design
npx skills add oai404iao/my_skills --skill agents-md
npx skills add oai404iao/my_skills --skill frontend-design
npx skills add oai404iao/my_skills --skill git-branch-development-workflow
```

交互式安装会选择目标 Agent 和安装范围。远程安装不包含本地尚未发布的修改。

本地验证后，可以将对应 skill 目录同步到实际安装目录。同步前检查目标是否有本地修改；同步该 skill 的入口和必要引用文件，不复制整个仓库，也不覆盖其他 skills。

## 仓库结构

```text
my_skills/
├── README.md                  # 技能目录、安装和维护说明
├── AGENTS.md                  # 本仓库维护约定
├── prompts/
│   └── coding-principles.md   # 可选公共指令，不是可安装的 skill
├── api-design/
│   ├── SKILL.md
│   └── references/
│       ├── application-encryption.md
│       └── sm2-sm4.md
├── agents-md/
│   └── SKILL.md
├── frontend-design/
│   ├── SKILL.md
│   └── references/
│       └── sources.md
└── git-branch-development-workflow/
    ├── SKILL.md
    └── references/
        └── worktrees.md
```

新增 skill 使用根目录下的 `<skill-name>/SKILL.md`。只有确有需要时才添加 `references/`、`scripts/`、`assets/` 和测试；不为凑齐模板创建空目录。

## 纳入来源

`frontend-design` 最初从本机安装副本纳入，现参考 Anthropic 的 frontend-design skill 重新整理，并保留本仓库的任务范围与验证约束。固定版本链接、采用内容及本地调整见 [来源说明](frontend-design/references/sources.md)；来源仅供追溯，不代表统一授权或上游背书。

`git-branch-development-workflow` 从本机原有的 `~/.agents/skills/` 对应目录原样纳入，包括 worktree 参考文档；未调整其行为规则。本地来源未附带许可证声明。

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
