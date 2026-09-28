# my_skills 维护指南

这是个人 Agent Skills 单仓库，不是应用项目。根目录下包含 `SKILL.md` 的目录是可分发技能；`prompts/` 保存可选公共指令，不参与技能安装。

## 文件职责

- `README.md`：可用 skills、安装方式、仓库结构和维护规范。
- `<skill-name>/SKILL.md`：技能入口、触发条件和必要流程。
- `<skill-name>/references/`、`scripts/`、`assets/`：按需添加的技能专属材料。
- `prompts/coding-principles.md`：尚需单独接入宿主的公共编码原则。

## 修改与分发

- 本仓库是维护来源。不要只修改已安装副本而遗漏仓库源码。
- 每个 skill 的 frontmatter 至少包含 `name`、`description`；名称与目录一致。
- 新建或维护 skill 时可参考 [Agent Skills Quickstart](https://agentskills.io/skill-creation/quickstart.md) 了解基本格式和加载流程；其中的 VS Code 操作与 `.agents/skills/` 路径是教程示例，不是本仓库的安装要求。
- 技能内容要能随目录迁移；相对路径以该 skill 所在目录解析。
- 将长参考材料按需拆分，不添加无用途的空目录或跨 skill 隐式依赖。
- 保留第三方内容的来源、许可证及署名；不要替来源不明的内容补造授权。
- 新增、删除、重命名技能时检查 README、内部链接和相应安装记录。
- 安装目录与 Git 仓库的变更分别核对；同步前比较安装副本，保留用户的独立修改。
- 提交、推送、发布或修改全局提示配置仅在任务授权范围内执行。

## 验证

当前保留的技能是 Markdown 指令，没有应用构建流程或可执行脚本测试套件。

```bash
git diff --check
git diff --stat
git diff
```

另外检查：

- frontmatter 与技能目录、README 一致。
- 相对链接指向真实文件；模板占位符不冒充真实路径。
- 提示规则没有未经证实的项目政策、宿主工具假设或额外授权。
- 用相关代表性请求复核规则，如只读审查、局部更新、项目约定缺失。

新增可执行脚本时，为其真实行为提供必要测试并记录命令；不为纯措辞变更新建镜像文本测试。
