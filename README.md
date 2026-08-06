# my_skills

可通过 [Skills CLI](https://github.com/vercel-labs/skills) 安装的 Agent Skills 集合。

## 可用 Skills

| Skill | 说明 |
| --- | --- |
| `imagegen` | 使用 Codex 内置图片工具或 OpenAI Images API 生成、编辑图片 |

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

### 只安装 `imagegen`

```bash
npx skills add oai404iao/my_skills --skill imagegen
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

## 更新

更新全局安装的 `imagegen`：

```bash
npx skills update imagegen --global
```

更新当前项目中的 `imagegen`：

```bash
npx skills update imagegen --project
```

## `imagegen` 的 API Key 认证

正常的 Codex 图片生成优先使用内置 `image_gen` 工具。只有显式选择 CLI/API 模式时，才会调用：

```text
imagegen/scripts/image_gen.py
```

CLI 使用 `AsyncOpenAI`，按以下顺序读取 API Key：

1. `OPENAI_API_KEY`
2. Codex 文件凭证：`$CODEX_HOME/auth.json`
3. 未设置 `CODEX_HOME` 时使用 `~/.codex/auth.json`

Codex 凭证必须是 API Key 模式。OAuth 凭证继续由 Codex 内置工具处理，不会被此脚本读取。

如需让 Codex 持久化 API Key，在 `$CODEX_HOME/config.toml` 中设置：

```toml
cli_auth_credentials_store = "file"
```

然后导入一次：

```bash
printenv OPENAI_API_KEY | codex login --with-api-key
```

之后运行 CLI 时可以不再保留 `OPENAI_API_KEY` 环境变量，脚本会读取 Codex 的 `auth.json`。

OpenAI Base URL 的读取顺序：

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
