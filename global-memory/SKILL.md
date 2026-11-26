---
name: global-memory
description: 检索跨工具共享的全局长期记忆（~/.agents/memory/），获取通用环境坑、工具/集合约定与非公司公共事实。遇到本机环境异常、工具链差异、Bruno/rbw/Pi/agy/hc/ROCm/mihomo 等通用问题时使用；对 Worker 默认只读。
---

# Global Memory

本技能用于检索 `~/.agents/memory/` 中的跨工具共享长期记忆（`pi` 与 `agy` 共用）。这里只存放所有 Worker 与 Router 都需要知道的通用环境坑、通用工具/集合约定与非公司公共事实，不包含项目私有实现、公司业务路由、活跃任务或凭据。

## 检索方式

优先使用内置检索脚本（相对本 `SKILL.md` 所在目录的 `scripts/search.sh`）：

```bash
~/.agents/skills/global-memory/scripts/search.sh 关键词1 关键词2
```

- 先在各主题文件 YAML frontmatter 的 `keywords` 列表中逐项精确匹配（忽略大小写），未命中的文件再检索正文；多个关键词为 OR。
- 命中则退出码为 `0` 并输出匹配文件；未命中退出码为 `1`；参数缺失或记忆目录不存在退出码为 `2`。
- 若脚本不可用，可直接执行 `rg -in -e 关键词 ~/.agents/memory/`。
- 只读取命中的主题文件，不预读全目录。

## 权限与写入约定

- **对 Worker 默认只读**：Worker（含 `pi` 与 `agy`）在任务中只检索和读取 `~/.agents/memory/`，不直接修改其中的文件。
- **新经验反馈**：Worker 在任务中发现新的通用环境坑或工具约定时，在向用户或上级（如 `hc send` 汇报）的结果中附带建议条目与证据，由维护者或经授权后写入。
- **结构与跨机同步**：目录结构、frontmatter 规范与同步到其他机器（如 `ssh dev`）的方法见 [references/memory-layout.md](references/memory-layout.md)。
