# Codex permissions, network, and sandbox notes

This file is for the fallback CLI mode only. Read it when the user explicitly asks to use `scripts/image_gen.py` / CLI / API / model controls, or after the user explicitly confirms that a transparent-output request should use the `gpt-image-1.5` true-transparency fallback path.

The bundled CLI performs outbound Images API requests. It also reads Codex provider configuration and, for file-backed API-key auth, Codex credentials from inside the sandboxed process.

## Approvals and sandbox permissions are separate

Two independent controls apply:

1. `approval_policy` controls when Codex asks before running commands.
2. The active sandbox/permissions profile controls filesystem and network access.

`--ask-for-approval never` or `approval_policy = "never"` suppresses approval prompts, but does **not** enable network access or broaden filesystem reads.

## Current Codex: named `[permissions]` profiles

Current Codex supports named profiles selected with `default_permissions`. For image generation, the simplest configuration is a custom profile that extends the built-in `:workspace` profile and enables network:

```toml
approval_policy = "on-request"
default_permissions = "imagegen"

[permissions.imagegen]
description = "Workspace access plus outbound network for image generation."
extends = ":workspace"

[permissions.imagegen.network]
enabled = true
```

In the current Codex implementation, `:workspace` includes:

- read access to the filesystem
- write access to the active workspace roots
- write access to the configured temporary directories
- read-only protection for workspace metadata such as `.git`, `.agents`, and `.codex`

Therefore this profile can normally read:

- the installed `imagegen` Skill
- `$CODEX_HOME/config.toml`
- `$CODEX_HOME/auth.json`, when file-backed API-key auth is used
- the active Python interpreter, packages, and CA bundle

It can also write generated files into the current project.

### Equivalent explicit filesystem configuration

If you prefer to spell out the filesystem policy instead of extending `:workspace`, use:

```toml
approval_policy = "on-request"
default_permissions = "imagegen-explicit"

[permissions.imagegen-explicit]
description = "Readable filesystem, workspace writes, and image API network."

[permissions.imagegen-explicit.filesystem]
":root" = "read"
":workspace_roots" = "write"
":tmpdir" = "write"
":slash_tmp" = "write"

[permissions.imagegen-explicit.network]
enabled = true
```

The special filesystem keys above are resolved by Codex:

- `:root`: the full filesystem
- `:workspace_roots`: the current project and any configured workspace roots
- `:tmpdir`: the platform temporary directory from the environment
- `:slash_tmp`: `/tmp` on Unix-like systems

Use canonical access values: `read`, `write`, or `deny`.

### Tighter explicit-read configuration

For a narrower profile, replace `":root" = "read"` with `":minimal" = "read"` and grant the required directories explicitly:

```toml
approval_policy = "on-request"
default_permissions = "imagegen-restricted"

[permissions.imagegen-restricted]
description = "Only the files and network required by imagegen."

[permissions.imagegen-restricted.filesystem]
":minimal" = "read"
":workspace_roots" = "write"
":tmpdir" = "write"
":slash_tmp" = "write"
"/absolute/path/to/installed/imagegen" = "read"
"/absolute/path/to/CODEX_HOME" = "read"
"/absolute/path/to/python/environment" = "read"

[permissions.imagegen-restricted.network]
enabled = true
```

Replace every placeholder with a real path. Filesystem keys must be absolute paths, `~/...` paths, or supported `:special` paths.

`:minimal` grants only platform runtime paths needed to launch common system executables and libraries; it does not automatically include user-installed Python environments or packages.

Additional read grants may be required when:

- the Skill is installed outside the workspace
- Python or `openai` is installed in a user-managed virtual environment
- the selected provider uses `[model_providers.<id>.auth] command`
- the provider auth command uses a separate executable, script, or working directory

`$CODEX_HOME/auth.json` is only needed when the CLI resolves file-backed API-key credentials. A provider using `env_key`, `experimental_bearer_token`, `auth.command`, or custom headers may not need that file.

## Optional managed network allowlist

`network.enabled = true` enables sandbox network access. If Codex's managed network proxy feature is also enabled, add every hostname used by the selected provider:

```toml
[features]
network_proxy = true

[permissions.imagegen.network]
enabled = true
mode = "full"

[permissions.imagegen.network.domains]
"api.openai.com" = "allow"
"images.example.com" = "allow"
```

Replace `images.example.com` with the hostname from the active provider's `base_url`. A custom provider that only implements the Responses API is still insufficient; it must expose OpenAI-compatible Images API endpoints.

When the managed proxy is active, a domain deny rule wins over an allow rule. If no domain is allowed, provider requests are blocked.

## Legacy Codex sandbox configuration

Older Codex versions use `sandbox_mode` and `[sandbox_workspace_write]` instead of named permissions profiles:

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = true
```

This legacy syntax remains supported by the current source, but new configurations should prefer `default_permissions` and `[permissions.<id>]`. Avoid mixing the legacy and named-profile forms in the same example.

## Safety note

Enabling network and broad filesystem reads lowers friction, but increases risk when running untrusted code or working in an untrusted repository. Prefer the restricted profile when its required paths are known.
