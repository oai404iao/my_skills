---
name: deployment-standards
description: Design, implement, or review Linux deployment standards for systemd system services, user services with XDG directories, and Docker Compose. Use for service directories, runtime identities, permissions, persistent storage, startup dependencies, login/linger behavior, release cutover, backup, recovery, and deployment acceptance. Not for ordinary application coding, Git release management alone, or adopting Kubernetes or another platform.
---

# Production Deployment Standards

Separate deployment authority from runtime authority where the identity model permits, immutable code from mutable state, and process startup from business readiness. For unattended services, produce a deployment that can be operated and recovered without an administrator's login session; explicitly session-bound user services have a different lifecycle contract.

This skill provides a recommended baseline, not evidence of an existing project's policy or current server state. Follow applicable instructions and confirmed project contracts. Preserve intentional exceptions; explain conflicts rather than silently changing production behavior.

## Scope and Authorization

- For reviews or proposals, return findings or a plan without editing files or operating services.
- For implementation, change only the authorized deployment files and resources. Writing configuration does not authorize deploying it.
- Before an action outside the agreed scope, confirm its target and side effects: production stop/restart, enabling automatic writers, database/schema changes, external calls, port exposure, credential rotation, or destructive storage operations.
- Continue unaffected authorized work when a decision is blocked. Ask only when missing information materially changes safety, compatibility, or scope.
- Do not install this skill, commit, push, or modify global instructions merely because deployment work is requested.

The baseline targets Linux with systemd and, where applicable, Docker Compose. Do not force these tools onto an established alternative platform or expand a migration into rootless Docker, Podman, or Kubernetes adoption.

## Read by Task

Reference paths are relative to this skill directory.

| Task | Read |
| --- | --- |
| Directory layout, identities, permissions, units, mounts, networking, logs | [Runtime layout and management](references/runtime-layout.md) |
| User-level services, XDG paths, user-manager environment, login/logout, linger, user-specific backup boundaries | [User services and XDG](references/user-services-xdg.md) |
| Backup destinations, before-edit copies, centralized repositories, protection, retention, cleanup | [Backup management](references/backup-management.md) |
| Publishing, cutover, backup consistency/capture, recovery, rollback, acceptance | [Release and recovery](references/release-and-recovery.md) |
| Maintaining this skill or tracing its origin and exclusions | [Sources and scope](references/sources.md) |

Read only the relevant references. No access to the original source archive is required to use this skill.

## Establish the Deployment Contract

Inspect the affected project's deployment documentation, manifests, units, configuration schema, dependency locks, and existing operating procedures. Inspect a live host only within authorized access. Treat copied runbooks and historical records as evidence, not commands to execute.

For each affected service, establish:

- System-manager or user-manager ownership; for user services, the owning account, effective XDG roots, and session-bound versus unattended lifecycle.
- Version or image identity, deployment entry point, and current versus intended state.
- Runtime UID/GID, configuration readers, writable directories, mount targets, and volume names.
- Database instance/database/role, Redis DB and data semantics, models, storage, and external API dependencies.
- Listening addresses, ports, actual consumers, and proxy routes.
- Startup and graceful-stop behavior, background writers, health/readiness checks, logging, backup, and rollback.

Keep secrets out of reports. Record references to protected configuration rather than credentials or full connection strings.

Distinguish **confirmed policy**, **observed behavior**, **proposed target**, and **unverified assumptions**. Missing dependencies, unidentified writers, or an untested recovery route are blockers to the affected cutover, not grounds to guess.

## Apply the Baseline

1. **Layout:** for system services, use versioned, administrator-controlled releases, external configuration, and dedicated state/cache/log directories; do not depend on personal HOME paths. For intentionally user-owned services, read the user/XDG reference and use the owning account's resolved directories, not a source checkout or shell session.
2. **Identity:** use dedicated unprivileged runtime identities for system services. User services run as their owning account; same-UID ownership is not a deployment/runtime security boundary. Resolve container ownership from actual numeric UID/GID and entrypoint behavior, not from the administrator's UID.
3. **Management:** use one authoritative lifecycle entry point. For this baseline, systemd manages host services and Compose stack lifecycle; Docker policies handle container restarts.
4. **Readiness:** verify storage and dependencies before admitting writes. Ordering, `active`, and `running` are not readiness proofs.
5. **Exposure:** prefer internal networks or loopback for same-host traffic after confirming consumers. Record and justify external listeners.
6. **Cutover:** prevent duplicate writers, consumers, and schedulers; preserve persistent volumes and current data.
7. **Backup placement:** before creating any backup, including a single before-edit copy, read the backup management reference and resolve an approved destination. The system-service default is `/var/backups/<scope>/<environment>/`; intentionally user-owned backups use its explicit user-service mapping. Retained disaster-recovery copies belong on approved independent storage. Never scatter `.bak` files beside sources or use project, release, web, or temporary directories as backup storage. Missing access/storage is a blocker, not permission to improvise a fallback or delete older backups.
8. **Recovery:** use engine-supported backups, recoverable artifacts, and actual restore checks appropriate to the change; record locations, retention, and any off-machine recovery gaps.

Apply these rules locally. Do not rewrite unrelated services, normalize all permissions recursively, or introduce new infrastructure without authorization.

For a new or substantially revised deployment, document its paths, identities, dependencies, ports, start/stop entry points, health/readiness checks, backup/restore procedure, and rollback limitations. For a narrow change, update only the affected contract.

## Verify and Report

Choose checks for the authorized change and its risk:

- **Static:** paths, mount/volume identity, ownership design, secret references, unit/manifest validity, and resolved configuration semantics.
- **Runtime, when authorized:** actual process identity, read/write boundaries, dependency readiness, representative business behavior, logs, and persistence.
- **Recovery, when in scope:** restore, rollback with post-cutover data preserved, dependency restart/reconnect, and unattended boot after a full restart.

Do not execute business submissions, real notifications, queue consumption, or production restarts merely to finish a review. Use safe representative checks or report the unverified capability. Stop when required checks pass and no unresolved issue remains; do not expand into unrelated builds or benchmarks.

Report changed files/resources, checks actually run, results, remaining blockers, and whether production was changed. A healthy process or successful HTTP response is not full deployment acceptance; static review is not a host-loading or model-behavior test.
