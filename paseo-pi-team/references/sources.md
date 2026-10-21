# 来源、宿主语义与验证边界

仅在维护或核实本 skill 时读取，不是每次开发任务的前置材料。

## 内容来源与许可范围

流程来自用户提供的《大型开发任务：Paseo + Pi 双层 Agent 团队启动指令》。本目录将它整理为显式调用入口、独立监督、工作区 / 集成 / 回收流程，保留授权、单写入 ownership、持续集成及真实验证要求；不是要求维护本 skill 的会话实际启动该团队。

编写方式参考以下官方资料，未整段转载第三方教程，也未捆绑第三方代码。本目录不替用户原文或整个仓库补造许可证；链接及参考不代表上游背书或统一再分发授权。

| 来源 | 本 skill 采用的内容 |
| --- | --- |
| [Agent Skills specification](https://agentskills.io/specification) | 目录与 `SKILL.md`、frontmatter 名称 / 描述 / 环境要求、相对引用与渐进加载 |
| [Agent Skills：Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) | 从现有流程提取技能，按实际阶段拆分参考材料，明确读取时机，避免无用脚手架 |
| [Anthropic：Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | 清晰触发边界、精简入口、浅层引用，按操作风险安排具体程度 |
| [Pi：Skills](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md) | `disable-model-invocation: true`、显式 `/skill:name`、参数追加与目录可迁移性 |
| [Pi：Settings](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/settings.md) / [Command Line](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/cli.md) | skill 命令发现设置、通过 `--skill` 为一次会话提供本地目录 |

## Pi 的“默认不加载”

维护时核对的本机 Pi 包为 `@earendil-works/pi-coding-agent` 1.2.0，并阅读了随包 `docs/skills.md`、相关 settings / CLI / packages 文档，以及 `dist/core/skills.js` 和 `dist/core/agent-session.js` 的相关实现。

- skill 仍可被宿主扫描并注册，但 `disable-model-invocation: true` 使其不进入提供给模型的自动选择列表；不是仅靠 description 写“不要自动调用”。
- `/skill:paseo-pi-team` 显式展开正文，后面的参数作为用户请求追加；`enableSkillCommands` 影响交互命令发现，不是本 skill 的禁用开关。
- 这是已核对的 Pi 宿主行为。Agent Skills 通用规范页面未列出该字段，不把它宣称为所有宿主都支持的标准开关；迁移到其他宿主前须核实。
- 该字段不是文件读取权限屏障。已有会话曾显式加载的正文也不会因它而从历史中消失。

## Paseo 与 Pi 工具证据

维护时阅读了宿主随附的 `paseo` skill，并只读检查了当前 Paseo MCP 工具声明：`create_workspace`、`create_agent`、`archive_workspace`、`list_profiles`、`send_agent_prompt`、`create_heartbeat`、`delete_heartbeat`、`create_schedule` 等。没有为验证文档而执行资源创建、归档或定时操作。

关键区别：

- 原生 workspace 创建与 agent 创建分离，`workspaceId` 显式绑定决定工作位置；Paseo 的会话父子关系不等于 Pi 的内部 subagent 层级，也不证明 Git 隔离。
- heartbeat 向调用者会话回送 prompt，schedule 可启动新会话；不假设有管理其他会话 heartbeat 的参数或通用 list / update 接口。
- 归档的 worktree 引用语义参考宿主随附说明；setup / teardown 影响仍须读取目标项目配置。工具声明本身不保证本地分支被删除。
- 消息后台执行与通知参数按具体接口确认，不把 Pi 的投递 / 启动语义套给 Paseo。

上述是维护时的文档及 schema 证据，不是对所有版本的承诺。运行时仍须发现真实工具并核实返回；本 skill 不硬编码 provider、model、安装路径或托管目录，也不要求其他 skill 必须安装。

## 维护时如何验证

检查 frontmatter、目录 / README 一致性、相对链接和 diff；可在已安装的 Pi 中对该目录调用实际 skill loader，检查无诊断且自动选择列表不含此 skill。不要为验证加载而启动真实开发团队。

静态走查以下代表性场景：

- 普通大型开发请求未点名：不自动选择本 skill；只审查本 skill：不启动团队。
- 显式调用但缺业务目标：只问必要问题，不猜目标。
- 拒绝 commit、整合或清理：分别保留 diff / 交付 / workspace，不扩大授权。
- 起始 dirty 修改或越权生命周期钩子：保护已有工作，停止受影响操作。
- 缺原生 workspace / heartbeat：报告对应限制，不用替代平台冒充。
- squash 已集成但分支清理受保护、归档回执不确定：核对实际成果和资源状态，不强制删除或盲目重试。

静态走查、loader 检查、交互命令实测和真实多 agent 行为是不同验证层次。未实际运行 heartbeat、创建 / 归档 workspace 或完整团队任务，不得报告这些流程已经通过实测。
