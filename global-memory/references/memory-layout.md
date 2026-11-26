# 共享全局记忆结构与同步说明

## 目录定位

- 记忆根目录：`~/.agents/memory/`（由 `GLOBAL_MEMORY_DIR` 环境变量覆盖）。
- 技能目录：`~/.agents/skills/global-memory/`（由 `my_skills/global-memory/` 维护并同步）。

## 主题文件与元数据

每个主题文件为 `~/.agents/memory/<topic>.md`，包含固定 YAML frontmatter：

```markdown
---
type: environment | tooling | network
keywords:
- 常用名称、别名、错误特征
verified: 2026-11-26
source: 来源说明
---
```

- `keywords` 每项一个词条；`search.sh` 对 `keywords` 做精确匹配（忽略大小写），未命中再做正文固定字符串匹配。
- 正文按主题分段整理，使用平实陈述句，不写防御性免责套话，不存放公司敏感服务路由、凭据或活跃任务。

## 同步到其他机器（如 `ssh dev`）

`my_skills` 仓库本身只维护 `global-memory` 技能与本结构说明，不托管本机 `~/.agents/memory/` 的具体记忆文件（避免跨环境混入本机专属路径）。向其他机器同步时：

1. **同步技能**：在目标机通过 `npx skills add oai404iao/my_skills --skill global-memory` 安装，或将 `my_skills/global-memory/` 复制到目标机 `~/.agents/skills/global-memory/`（确保 `scripts/search.sh` 有可执行权限）。
2. **同步全局规范**：目标机通过 `chezmoi` 或 `scripts/sync-pi-agents.sh` 获取 `my_skills/prompts/global-agents.md`，部署到 `~/.config/pi/agent/AGENTS.md` 与 `~/.gemini/GEMINI.md`。
3. **同步记忆内容**：按需将本机 `~/.agents/memory/` 中的通用主题文件同步到目标机 `~/.agents/memory/`（例如 `rsync -av ~/.agents/memory/ dev:~/.agents/memory/`），并剔除仅适用源机器的条目。
