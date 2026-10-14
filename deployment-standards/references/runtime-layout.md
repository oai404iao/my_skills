# Runtime Layout and Management

Use this reference when designing or reviewing paths, identities, permissions, startup, networking, and logs. The paths below are baseline examples: replace `<app>`, `<stack>`, `<version>`, and `<site>` with verified names. They are not existing resources or commands to execute.

## Directory Responsibilities

| Path | Purpose | Write boundary |
| --- | --- | --- |
| `/srv/stacks/<stack>/` | Compose manifests and non-secret deployment notes | Administrator-controlled; runtime cannot write |
| `/opt/<app>/releases/<version>/` | Code, independent runtime environment, immutable artifacts | Administrator-controlled; runtime read/execute only |
| `/opt/<app>/current` | Link to the selected release | Administrator-controlled |
| `/etc/<app>/` | Effective configuration and credentials | Administrator writes; grant only necessary read access |
| `/var/lib/<app>/` | Databases, uploads, task state, persistent outputs | Corresponding runtime identity |
| `/var/cache/<app>/` | Verified rebuildable/downloadable cache | Corresponding runtime identity |
| `/var/log/<app>/` | Required file logs | Corresponding runtime identity; rotate |
| `/var/backups/<scope>/<environment>/` | Before-change backup sets and local export staging | Backup administrator only; not the sole disaster-recovery copy |
| `/var/www/html/<site>/` | Static published artifacts | Administrator publishes; web worker reads |

- Do not depend on personal HOME directories, shell profiles, login activation, or administrator-owned per-user tools.
- Keep dependency installation and builds out of the running release. Put generated files and caches in explicit writable locations.
- A model directory called `cache` is not disposable until re-acquisition is verified. Unique weights and custom models are persistent assets.
- Keep uploads outside static release and web-server configuration directories.
- Preserve Docker-managed named volumes when appropriate; do not manually relocate Docker's internal directories. For new bind-mounted state, prefer `/var/lib/<app>/`.
- Record each volume's real name, owner, container target, backup procedure, and consumers. A Compose project rename must not silently select an empty volume.
- If using separate data filesystems, account for Docker volumes as well as bind mounts. Mounting `/srv` alone does not move Docker-managed storage.
- Declare required mount dependencies and fail when storage is unavailable rather than writing into an unmounted directory on the root filesystem.
- Before creating backup copies, read [Backup management](backup-management.md) for type-specific paths, permissions, retention, and independent storage. `/var/backups` is this baseline's convention, not a universal FHS mandate.

## Identities and Permissions

- Prefer dedicated non-login `svc-*` system accounts for host applications, without sudo or container-management privileges. Do not reuse the administrator's UID.
- The rootful Docker control plane and systemd may remain administrator/root managed while business processes run unprivileged.
- Inspect actual container process UID/GID and initialization/drop-privilege behavior. An empty image user field does not prove the final database process runs as root.
- Do not force database images to `1000:1000` or assume a host service group is automatically present in a container.
- Runtime users must not modify code, units, manifests, deployment scripts, the `current` link, or any parent directory that would let them replace those objects.
- Configuration examples: `root:<service-group>` directory `0750`, files `0640`; administrator-only secrets `0600`. If only the control plane needs to read a file, do not grant the runtime unnecessary access.
- Check traversal permissions and actual read access for bind-mounted configuration; use read-only mounts when possible.
- Grant writable state only to its runtime identity. For necessary sharing, use an explicit group and minimum access.
- Do not use recursive blanket ownership changes, `0777`, `privileged`, or Docker socket access as permission fixes. Docker group membership is administrative authority, not business-process isolation.
- Retain root or device access only for demonstrated needs such as privileged system maintenance or GPU workloads; document the exception and verify its boundaries.
- Create secret-bearing files with restrictive permissions from the start. Do not rely only on a final chmod after writing.
- Keep configuration examples and non-secret manifests versionable. If a legacy manifest embeds secrets, restrict it and do not commit it.

## Effective Configuration

Moving configuration to `/etc` changes more than filenames. Verify working-directory-relative databases, workflows, certificates, models, uploads, and log paths.

Do not assume dotenv syntax matches systemd `EnvironmentFile=`. Check quoting, multiline values, interpolation, and the application's actual configuration loader. Preserve the intended effective values without printing secrets.

## systemd and Compose

### Host services

- Use absolute executable paths and explicit `User`, `Group`, `WorkingDirectory`, and configuration locations.
- Define appropriate restart/backoff, stop timeout, and graceful shutdown behavior. Workers must finish or safely return in-flight work.
- Test hardening such as `NoNewPrivileges`, `ProtectSystem`, `ProtectHome`, and writable-path allowances against actual behavior. Device isolation can break GPUs; other restrictions can break browsers or subprocesses.
- Validate unit definitions on the target system before enabling them. Do not restore unrelated cron jobs or add timers that duplicate an application's scheduler.
- Do not let systemd and Supervisor manage the same process simultaneously. Retain a disabled legacy manager only where the confirmed rollback plan needs it.

### Compose stacks

- Use a stable project name, fixed manifest/configuration locations, and an administrator-controlled `stack-<stack>.service` lifecycle entry point.
- Declare Docker and required storage dependencies. Stop actions must actually stop the stack without deleting persistent volumes.
- Coordinate systemd stack lifecycle with Docker restart policies. A oneshot unit's `active` state does not prove container health.
- Docker may restart containers without re-running the stack unit. `disabled` alone is not proof that containers cannot start or write.
- Within a stack, use health checks and readiness dependencies where supported. Across stacks, explicitly handle dependency readiness; applications still need retries and reconnection.
- Do not promote a manually started, undocumented container into an official production service.

## Ports, Proxying, and Logs

- Record binding address, port, protocol, consumer, and intended exposure. Verify IPv4 and IPv6 listeners as relevant.
- Prefer container networking for container-only consumers and loopback for same-host consumers; preserve confirmed remote access until its replacement is agreed.
- Container loopback refers to that container, not the host. Define cross-stack networks and endpoints explicitly.
- Do not infer safety from an inactive firewall, or disable Docker's network rules to satisfy a request not to configure a firewall. Firewall/SSH policy is project-specific.
- Use the packaged Nginx service where applicable; preserve its necessary master privileges and unprivileged workers.
- Keep backup configuration outside include directories. Test configuration before reload, then check routes, path prefixes, static resources, uploads, and streaming behavior as applicable.
- Prefer stdout/journald or managed container logs; configure retention. If file logs are required, use the dedicated log directory and rotation.
