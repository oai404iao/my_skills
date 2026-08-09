# my_skills

可通过 [Skills CLI](https://github.com/vercel-labs/skills) 安装的 Agent Skills 集合。

## 可用 Skills

| Skill | 说明 |
| --- | --- |
| `agents-md` | 创建、更新、审查和重构面向 AI 编码 Agent 的 `AGENTS.md` |
| `imagegen` | 使用宿主内置图片工具，或按 Codex Provider 配置调用 OpenAI-compatible Images API |

## 使用 `npx skills` 安装

无需全局安装 Skills CLI，直接通过 `npx` 调用。

### 查看仓库中的 Skills

```bash
npx skills add oai404iao/my_skills --list
```

### 交互式安装

```bash
npx skills add oai404iao/my_skills
```

### 只安装指定 Skill

```bash
npx skills add oai404iao/my_skills --skill imagegen
```

```bash
npx skills add oai404iao/my_skills --skill agents-md
```

也可以使用完整仓库地址：

```bash
npx skills add https://github.com/oai404iao/my_skills --skill imagegen
```

### 全局安装到 Codex

```bash
npx skills add oai404iao/my_skills \
  --skill imagegen \
  --global \
  --agent codex \
  --yes
```

### 全局安装到 Pi

```bash
npx skills add oai404iao/my_skills \
  --skill imagegen \
  --global \
  --agent pi \
  --yes
```

去掉 `--global` 即安装到当前项目。

## Skill 路径

Skills CLI 会根据安装范围和目标 Agent 选择实际目录，因此本项目不硬编码 Codex 内置 Skill 的安装位置。

文档中的以下路径都相对于已安装的 `imagegen` 目录，也就是包含 `SKILL.md` 的目录：

```text
scripts/image_gen.py
scripts/remove_chroma_key.py
references/*.md
```

执行脚本前，应先将该目录解析为绝对路径。例如：

```bash
export IMAGEGEN_SKILL_DIR="<包含 imagegen/SKILL.md 的目录>"
python "$IMAGEGEN_SKILL_DIR/scripts/image_gen.py" --help
```

## Codex：屏蔽内置 `imagegen`

Codex 自带一个同名的 bundled/system `imagegen`。安装本仓库版本后，为确保 Codex 使用本仓库中的 Skill，需要在用户的 `$CODEX_HOME/config.toml`（默认 `~/.codex/config.toml`）中按**绝对路径**禁用内置版本：

```toml
[[skills.config]]
path = "/实际的/CODEX_HOME/skills/.system/imagegen/SKILL.md"
enabled = false
```

请将 `path` 替换为本机内置 `imagegen/SKILL.md` 的真实绝对路径。

> 不要按 Skill 名称禁用 `imagegen`，否则内置版本和本仓库版本可能会一起被禁用。

如果希望禁用 Codex 的所有 bundled Skills，也可以使用：

```toml
[skills.bundled]
enabled = false
```

## Codex：开启 `web.run`

`web.run` 是 Codex Web Search extension 提供的 standalone 工具。是否暴露该工具，取决于模型是否使用 Responses Lite、Provider 能力、搜索模式、feature 配置以及 extension 是否成功注册。

下面的示例使用：

```toml
web_search = "live"
```

这样会明确请求实时外网搜索。未配置 `web_search` 时默认是 `cached`；工具仍可能出现，但 `external_web_access = false`。

### GPT-5.5：普通 Responses，非 Lite

GPT-5.5 默认使用 hosted `web_search`。要让 standalone `web.run` 优先替代 hosted 工具，需要开启 `standalone_web_search` feature：

```toml
model = "gpt-5.5"
model_provider = "openai"
web_search = "live"

[features]
standalone_web_search = true
```

如果已有 `[features]` 表，只需把 `standalone_web_search = true` 合并进去，不要重复声明 TOML 表。

此模式下：

- `web.run` 成功注册时，Codex 不再向模型发送 hosted `type: web_search`
- `web.run` 未安装、注册失败或发生工具名冲突时，会回退到 hosted `web_search`
- `standalone_web_search` 当前属于开发中 feature，GPT-5.5 必须显式开启

### GPT-5.6 系列：Responses Lite

当前 Codex 模型目录中的 `gpt-5.6-sol`、`gpt-5.6-terra` 和 `gpt-5.6-luna` 都使用 Responses Lite。Lite 模型本身已经满足 standalone 搜索条件，因此使用 OpenAI Provider 时不需要开启 `standalone_web_search` feature：

```toml
model = "gpt-5.6-sol" # 也可以是 gpt-5.6-terra 或 gpt-5.6-luna
model_provider = "openai"
web_search = "live"
```

Responses Lite 永远不会发送 hosted `type: web_search`。因此：

- Web Search extension 正常注册时，只暴露 `web.run`
- `web.run` 没有成功注册时，不会回退到 hosted 搜索，而是没有任何搜索工具

Codex App Server 默认安装 Web Search extension。其他自定义宿主需要确保该 extension 已安装。

### 自定义 Provider

普通自定义 Provider 默认没有 standalone 搜索资格。除非使用非空的 `x-openai-actor-authorization`，否则需要在 Provider 配置中显式开启：

```toml
model_provider = "corp"
web_search = "live"

[model_providers.corp]
name = "Corp"
base_url = "https://responses.example.com/v1"
env_key = "CORP_API_KEY"
supports_standalone_web_search = true
```

`supports_standalone_web_search = true` 只是声明 Provider 具备该能力；对应后端仍需真正实现 standalone Web Search endpoint。

另外：

- GPT-5.5 / 非 Lite 模型仍需 `[features] standalone_web_search = true`
- GPT-5.6 / Responses Lite 模型不需要该 feature
- Amazon Bedrock 不支持 standalone `web.run`；Responses Lite 下也没有 hosted 搜索可回退
- `web_search = "disabled"`、Guardian 或 Review 会话不会暴露搜索工具

搜索模式：

| `web_search` | 行为 |
| --- | --- |
| `"live"` | 允许实时外网访问 |
| `"indexed"` | 允许外网访问并启用 indexed 模式 |
| `"cached"` | 使用缓存结果，不允许实时外网访问 |
| `"disabled"` | 不暴露任何搜索工具 |

> “开启”表示把 `web.run` 暴露给模型；最终是否调用仍由模型在 `tool_choice: auto` 下决定。

## 更新

更新全局安装的 `imagegen`：

```bash
npx skills update imagegen --global
```

更新当前项目中的 `imagegen`：

```bash
npx skills update imagegen --project
```

## `imagegen` 的 Provider 与认证

宿主提供 `image_gen` 工具时，普通图片生成优先使用该内置工具。只有显式选择 CLI/API 模式，或内置工具不可用且用户确认使用 fallback 时，才会调用：

```text
imagegen/scripts/image_gen.py
```

CLI 使用 `AsyncOpenAI`，首先读取 `$CODEX_HOME/config.toml` 中的：

- `model_provider`
- `[model_providers.<id>]`
- `base_url`
- `env_key`
- `env_key_instructions`
- `experimental_bearer_token`
- `[model_providers.<id>.auth]`
- `query_params`
- `http_headers`
- `env_http_headers`
- `request_max_retries`

自定义 Provider 的认证优先级：

1. `env_key` 指定的动态环境变量
2. `experimental_bearer_token`
3. Provider `auth.command` 的标准输出
4. `requires_openai_auth = true` 时读取 Codex API Key 文件凭证
5. Provider 自定义请求头或无 Bearer Token 模式

例如：

```toml
model_provider = "corp-images"

[model_providers.corp-images]
name = "Corp Images"
base_url = "https://images.example.com/v1"
env_key = "CORP_IMAGES_API_KEY"
query_params = { region = "us-east" }
http_headers = { "X-Client" = "codex-imagegen" }
env_http_headers = { "X-Tenant" = "CORP_TENANT_ID" }
request_max_retries = 6
```

此时脚本读取的是：

```bash
CORP_IMAGES_API_KEY
```

不会错误回退到 `OPENAI_API_KEY`。

> Provider 必须实现 OpenAI-compatible Images API。只兼容 Responses API 并不代表能够生成图片。AWS/Bedrock 认证不受该 CLI fallback 支持。

### 内置 OpenAI Provider

当 `model_provider = "openai"` 或未配置 Provider 时，API Key 顺序为：

1. `OPENAI_API_KEY`
2. Codex 文件凭证：`$CODEX_HOME/auth.json`
3. 未设置 `CODEX_HOME` 时使用 `~/.codex/auth.json`

Codex 文件凭证必须是 API Key 模式。OAuth 凭证继续由 Codex 内置工具处理，不会被此脚本读取。

如需让 Codex 持久化 API Key，在 `$CODEX_HOME/config.toml` 中设置：

```toml
cli_auth_credentials_store = "file"
```

然后导入一次：

```bash
printenv OPENAI_API_KEY | codex login --with-api-key
```

之后运行 CLI 时可以不再保留 `OPENAI_API_KEY` 环境变量，脚本会读取 Codex 的 `auth.json`。

内置 OpenAI Provider 的 Base URL 读取顺序：

1. `OPENAI_BASE_URL`
2. `$CODEX_HOME/config.toml` 中的 `openai_base_url`
3. OpenAI SDK 默认地址

### Python 依赖

```bash
uv pip install openai
```

Python 3.10 及更早版本如需读取 Codex `config.toml`，还需：

```bash
uv pip install tomli
```

透明背景后处理或图片缩放还需要：

```bash
uv pip install pillow
```

## 来源与许可证

`imagegen` 基于 OpenAI Codex 内置 image generation skill 提取并调整。许可证见：

```text
imagegen/LICENSE.txt
```
