# User Services and XDG

Read for Linux `systemd --user` services and their paths, environment, lifecycle, permissions, or backup design. This is an alternative ownership profile to the system-service layout, not an instruction to migrate existing services. Examples and commands are documentation, not authorization to change accounts, start services, or enable linger. Primary evidence and version limits are recorded in [Sources and scope](sources.md#user-services-and-xdg-sources).

## Choose the Ownership and Lifecycle

| Profile | Use when | Contract |
| --- | --- | --- |
| System service running unprivileged | Shared infrastructure, privileged integration, or administrator-enforced separation of deployment and runtime | Administrator-managed system unit and artifacts; dedicated runtime identity; system paths from [Runtime layout](runtime-layout.md) |
| Session-bound user service | A personal tool or desktop/session component belongs to one account | Owning user's manager; define the required session target and stop behavior; no promise of unattended boot |
| Unattended user service | A service deliberately belongs to one account and must run without login | Owning user's manager, enabled activation, approved linger, boot-available HOME/storage, and logout/reboot acceptance |

- A non-root `User=` in a system unit does **not** make it a user service. Record manager scope and account alongside the unit name; identical names in the two managers are independent instances.
- A user manager is shared by the account's sessions, not created separately for every SSH terminal. It is not necessarily tied to the last shell's exit; logind policy and linger affect its lifetime.
- Personal user services normally share their owner's authority over files, credentials, and other processes. Use a separate account or system service when stronger separation is required; do not describe `0700`, an XDG layout, or a user unit as a sandbox.
- Do not add `User=`, `Group=`, `DynamicUser=`, sudo, or Docker-group membership to a normal non-root user unit to invent privilege separation. Existing container deployments retain their confirmed engine/socket and lifecycle contract; this profile does not authorize rootless-engine adoption.

## Directory Contract

Resolve paths for the **owning account**, not the administrator or invoking shell. Honor valid absolute XDG overrides. When unset or empty, use the specified defaults below; reject or ignore invalid relative values rather than interpreting them against the working directory. Do not silently migrate existing application data just to fit this table.

| Role | Resolved location / default | Rule |
| --- | --- | --- |
| Configuration | `$XDG_CONFIG_HOME/<app>/` → `~/.config/<app>/` | Non-secret settings and references to protected secrets; separate from release artifacts |
| Authoritative data | `$XDG_DATA_HOME/<app>/` → `~/.local/share/<app>/` | User-owned databases, uploads, unique models, and other irreplaceable content |
| Persistent operational state | `$XDG_STATE_HOME/<app>/` → `~/.local/state/<app>/` | History, checkpoints, resumable work, and other restart-persistent state; not automatically disposable |
| Rebuildable cache | `$XDG_CACHE_HOME/<app>/` → `~/.cache/<app>/` | Deletion must not lose unique content; verify re-acquisition first |
| Transient IPC / locks | `$XDG_RUNTIME_DIR/<app>/` | Local, user-owned runtime storage; on logind hosts commonly `/run/user/<uid>/<app>/`; never a database or backup destination |
| User-installed executable entry points | `~/.local/bin/` | XDG specifies no `XDG_BIN_HOME`; do not assume a service inherits the interactive shell's PATH |
| Locally managed release artifacts | `$XDG_DATA_HOME/<app>/releases/<version>/` and `current` | This skill's convention, **not an XDG requirement**; keep mutable content in separately identified subdirectories |
| User unit and drop-ins | `$XDG_CONFIG_HOME/systemd/user/<app>.service` and `<app>.service.d/*.conf` | Default `~/.config/systemd/user/`; inspect effective load paths and overrides, not just this file |
| Required file logs | `$XDG_STATE_HOME/log/<app>/` | Prefer the journal; this convention matches user `LogsDirectory=` and needs explicit rotation/retention |

`DATA` versus `STATE` describes purpose, not “back up” versus “discard.” An application's database/checkpoint may already live in either; record its real location, recovery value, and supported configuration options. XDG search roots (`XDG_CONFIG_DIRS`, `XDG_DATA_DIRS`) are ordered lookup paths, not extra writable homes. Preserve the application's documented lookup/merge behavior.

The runtime root must be owned by the user, mode `0700`, on a suitable local filesystem. Let logind manage it; do not manually create `/run/user/<uid>` or use `chmod 777` to repair a session. There is no persistent HOME default for `XDG_RUNTIME_DIR`. For this deployment baseline, a missing/invalid runtime root blocks dependent service startup rather than falling back to a shared `/tmp` directory. This is deliberately stricter than the XDG specification's application fallback guidance.

Treat runtime contents as ephemeral across manager teardown and reboot, even with linger. `RuntimeDirectory=` normally removes its own subdirectory on service stop. Never back up sockets, PID files, or locks for restoration as live runtime objects.

Preserve packaged/install-tool layouts when they already provide a stable executable. For locally managed releases, build outside the active version, retain a known-good artifact, and switch the entry point only through the approved cutover. A user-owned `current` link and read-only file modes reduce accidents, but the same UID can usually change permissions or replace objects through writable parents; they do not enforce immutable deployment authority.

## Manager Environment and Path Expansion

- User services do not run a login shell or automatically source `.profile`, `.bashrc`, virtualenv activation, nvm, or similar setup. Use a stable absolute executable path and explicit working directory, configuration, and dependency paths. Keep builds, installs, and background-shell launchers out of `ExecStart=`.
- Establish custom XDG roots in the manager's startup environment through the host's supported mechanism **before** relying on unit discovery and directory resolution. A terminal export, per-service `Environment=`, or `EnvironmentFile=` is not proof that the manager uses those roots.
- `environment.d` configures the environment passed to user-manager children; do not assume it relocates the manager's own unit search path. Avoid broad `import-environment` as a deployment fix: manager-wide changes affect other services and may import secrets or session-only settings.
- Inspect the running manager's load paths (`systemctl --user show -p UnitPath`) and effective unit/drop-in selection; a client tool's paths under the terminal's environment need not match the manager. Consult the target version's manuals for supported specifiers: `%h` is HOME, `%t` runtime, `%D` data, `%E` configuration, `%S` state, `%C` cache, and `%L` log root in user scope. HOME is not necessarily `/home/<name>`.
- Unit fields are not shell syntax: do not put `~`, `${XDG_STATE_HOME:-...}`, pipes, redirects, or `&&` in them expecting shell expansion. `ExecStart=` has its own limited substitution rules; the executable must not be an environment-variable expression. Prefer specifiers supported by the field or correctly escaped, resolved absolute paths. Use a wrapper only for a real launch requirement, with explicit interpreter and `exec` handoff.
- If the application does not implement XDG, configure its documented path options explicitly. Merely exporting XDG variables or creating directories does not relocate its state.

### Manager-created directories

Where supported, use these unit directives with relative, application-specific names:

| Directive | User-manager location | Exported application environment |
| --- | --- | --- |
| `RuntimeDirectory=<app>` | `$XDG_RUNTIME_DIR/<app>` | `RUNTIME_DIRECTORY` |
| `StateDirectory=<app>` | `$XDG_STATE_HOME/<app>` | `STATE_DIRECTORY` |
| `CacheDirectory=<app>` | `$XDG_CACHE_HOME/<app>` | `CACHE_DIRECTORY` |
| `LogsDirectory=<app>` | `$XDG_STATE_HOME/log/<app>` | `LOGS_DIRECTORY` |
| `ConfigurationDirectory=<app>` | `$XDG_CONFIG_HOME/<app>` | `CONFIGURATION_DIRECTORY` |

These manage directories, not application configuration. An application must consume these variables or receive explicit paths. There is no corresponding `DataDirectory=` directive; provision authoritative data explicitly. Do not move a contracted database into `StateDirectory=` merely because the directive is convenient.

Use restrictive `*DirectoryMode=` values for private content; configuration may be provisioned separately rather than auto-created. State/cache/log directories persist on ordinary stop; this does not make cache a backup or guarantee journal persistence. Check custom roots against the target manager and application; service-local overrides must not send writes to a second, unnoticed tree.

## Unit Baseline

The following is an illustrative user unit for a foreground daemon. `example-app`, paths, flags, and timeouts are placeholders to adapt to a verified application. It is not a ready-to-install service. Verify the target manager's specifier support and resolved XDG roots before use; render escaped absolute paths where required.

```ini
[Unit]
Description=Example user-owned application
StartLimitIntervalSec=60
StartLimitBurst=5

[Service]
Type=exec
WorkingDirectory=%D/example-app/current
ExecStart=%D/example-app/current/bin/example-app --config %E/example-app/config.toml
RuntimeDirectory=example-app
RuntimeDirectoryMode=0700
StateDirectory=example-app
StateDirectoryMode=0700
CacheDirectory=example-app
CacheDirectoryMode=0700
UMask=0077
NoNewPrivileges=yes
Restart=on-failure
RestartSec=5s
TimeoutStopSec=30s
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

- Verify `Type=exec` and other directives on the target system. Use `Type=notify` only when the application implements notification; successful exec is not business readiness. A session/GUI component needs its desktop's confirmed activation and stop coupling, not this unattended-daemon target.
- Configure the example application explicitly to use its intended state/cache/runtime locations; the sample does not invent flags for these. Retain safe control-group termination and graceful shutdown; do not daemonize with `&` or leave unmanaged children.
- Dependencies in user units resolve inside the **user manager**. `After=docker.service`, `After=network-online.target`, or `RequiresMountsFor=` in a user unit does not establish ordering against PID 1's Docker, network, or mount units. Even within one manager, `After=` alone does not pull in a dependency.
- Require retries/reconnection and actual dependency readiness. Provision privileged mount/network prerequisites through the authorized system-level contract; verify expected storage identity and fail before writes if unavailable. Do not create data under a missing mount or solve boot races with a fixed sleep.
- Start with portable restrictions such as `UMask=` and `NoNewPrivileges=`. Filesystem namespace hardening and resource controls have user-manager, kernel, user-namespace, and delegation limits. Validate their actual effects rather than copying a system-service hardening block; `ProtectHome=yes` can hide the very release/configuration needed here. Never weaken host-wide security controls merely to make a sample unit start.

## Activation, Linger, and Operations

Operate as the owning account in a supported user-manager connection. `sudo systemctl --user` normally targets root's manager, not the intended user's; `sudo -u` alone need not establish the required runtime/bus environment. Diagnose the correct account, logind session, runtime root, and bus before retrying; do not forge another UID's environment or relax permissions.

Read-only diagnostics, from any working directory after substituting the verified unit/account:

```sh
systemctl --user show example-app.service -p FragmentPath -p DropInPaths -p ActiveState -p SubState
systemctl --user is-enabled example-app.service
journalctl --user -u example-app.service -n 100 --no-pager
loginctl show-user example-owner -p Linger -p State -p RuntimePath
```

Treat logs and configuration output as potentially secret-bearing; redact evidence. Nonzero `is-enabled` can describe a disabled unit rather than a broken connection; inspect the reported state, since even a zero exit status need not mean explicit enablement (for example, `static`). Journal availability/retention depends on host policy; do not promise persistent per-user journals or change host-wide journald settings without authorization.

For an authorized installation/change, validate the actual unit with `systemd-analyze --user verify <absolute-unit-path>` on the target version. Then apply only the necessary operations:

| Operation | Meaning and side effect |
| --- | --- |
| `systemctl --user daemon-reload` | Reload this manager's unit definitions; does not restart the application |
| `systemctl --user enable <unit>` | Install activation links; does not start the unit or provide boot-time user-manager availability |
| `systemctl --user start <unit>` / `restart <unit>` | Start now / interrupt and restart now; requires service-operation authorization |
| `loginctl enable-linger <owner>` | Arrange boot-time user manager and survival after logout; account-wide policy change, subject to host authorization |
| `systemctl --user disable <unit>` / `stop <unit>` | Remove enablement / stop now; neither alone blocks every other activation path |

Do not combine `enable --now` as an incidental documentation-validation step. Before using linger for unattended service, confirm the owner, intended account-wide effects, boot-available HOME/config/secrets, and mount/dependency behavior. Login-unlocked encrypted HOME or interactive secret prompts can make unattended boot impossible despite linger. Do not change global logind settings as a shortcut.

Linger does not enable the application or guarantee readiness; enabled units without a boot-started manager do not satisfy unattended boot either. Disabling linger or terminating/restarting the entire user manager affects unrelated units and sessions, so it is not a single-service rollback step.

For cutover, stop all relevant activation sources (timers, sockets, path/D-Bus activation, old units/managers, container restart policies) as necessary under authorization. Check both system and user instances for duplicate listeners/writers. Do not infer quiescence from `disabled` alone. Apply the data-preserving cutover/rollback rules in [Release and recovery](release-and-recovery.md).

## Permissions, Secrets, and Backup

- Create private application directories as `0700` and secret files as `0600`, with restrictive creation modes from the start. Do not recursively chmod/chown HOME or change unrelated XDG parents. Non-secret units may use ordinary readable modes, but must not contain credentials.
- Prefer application-supported secret files or supported `LoadCredential=` facilities; verify availability and same-UID limits. Environment variables are not a secret store. If a legacy application only accepts an environment file, protect it and record its exposure; do not publish secrets in unit files, command arguments, logs, or reports.
- Read [Backup management](backup-management.md#user-owned-service-mapping) before any copy, including pre-edit units/config. User-owned backup staging is an explicit profile, not a fallback after `/var/backups` fails. Keep it outside all captured application trees and releases.
- Back up configuration, authoritative data, necessary operational state, and irreplaceable artifacts with the existing consistency/retention contract. Exclude only verified cache/reproducible artifacts and transient IPC. Record account identity, effective XDG roots, original paths, unit/drop-ins, activation/linger state, and protected recovery-key references.
- A same-UID backup directory is writable by a compromised application just like its source. Do not claim backup/runtime separation: use approved independent storage and protected deletion authority for retained recovery points. Do not place independent backup credentials in the application's environment.

## Acceptance

For the affected contract, statically check scope/account, actual roots and overrides, executable/config paths, writable boundaries, directive support, activation sources, and backup mapping. A custom-XDG scenario must resolve consistently in manager discovery, directory directives, application settings, and restore destinations.

Runtime checks require authorization: confirm the actual UID, useful logs, dependency recovery, graceful stop, no duplicate writers, and data survival across service restart. For session-bound services, check intended session start/stop coupling; for unattended services, check logout of all sessions and a full-machine restart **without first logging the owner in**, including HOME/storage/secrets availability.

A successful `verify`, `active`, enablement, or `Linger=yes` is not evidence that these runtime/recovery checks passed. Report omitted checks and same-UID/backup isolation gaps rather than declaring full acceptance.
