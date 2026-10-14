# Release and Recovery

Read for publishing, production cutover, backup/restore, rollback, or deployment acceptance. These are procedures to adapt, not authorization to operate a host. Check exact commands against project wrappers, installed versions, working directories, and intended side effects before use.

## Prepare a Recoverable Release

1. Record the source revision or release identifier, including relevant uncommitted changes when preserving an existing deployment.
2. Publish into a new versioned release directory under administrator control. Keep runtime configuration and mutable state outside it.
3. Rebuild language environments from compatible dependency locks on the target system. Do not assume a copied virtual environment is portable.
4. Record immutable container image identity: image ID and available digest. Retain offline images or reproducible build inputs where registry recovery is uncertain.
5. Verify configuration semantics, actual dependency addresses, container UID/GID, mounts, free space, and startup/stop behavior.
6. Prepare the rollback route and acceptance criteria before changing the production entry point.

Do not combine an operating-system or directory migration with unapproved database major-version upgrades, extension upgrades, driver replacement, or algorithm/configuration changes.

## Backup Contract

Before capturing or copying anything, read [Backup management](backup-management.md) and resolve its destination, protection, set identity, manifest, and retention owner. This applies to ad hoc pre-change configuration copies as well as full migrations; do not leave backup files beside active sources. The rules below define capture and recovery semantics rather than a second storage convention.

Cover code and locks, effective configuration, necessary secrets, images/build inputs, database state, uploads, outputs, unique models, and required logs. Treat shared database instances by their verified contents and consumers, not guessed ownership from names.

For each backup, record source, capture time, engine/tool version, size, checksum, write-quiescence status, protection/encryption method, restore procedure, and verification result. Keep credentials and business records out of public evidence.

- **PostgreSQL:** use compatible engine-supported logical or physical backup procedures. Include databases and required global objects such as roles, permissions, and tablespaces; preserve extension/configuration requirements. Do not treat copying a live data directory as a consistent backup or run physical data across major versions.
- **Redis:** determine whether keys are cache, queue, locks, sessions, or business state. Verify effective RDB/AOF settings and produce a recoverable snapshot/file set; include ACL/configuration and multipart AOF components where applicable. A mounted volume or successful `PING` does not prove recoverable state.
- **SQLite:** use supported backup semantics or a fully quiesced database copy, accounting for WAL. Verify the working copy's ownership, including WAL/SHM created by administrative checks.
- **Files/models:** verify database-to-file relationships, referenced external objects, symlink targets, and re-acquisition of anything excluded as cache.

Online snapshots may be individually valid without being consistent across databases, Redis, and files. For a coordinated migration, produce final backups within one confirmed stop-write window covering every writer, including remote consumers.

Keep at least one recoverable backup outside the physical machine being migrated or erased. Keys and restore tools must also survive its loss. Test restoration in isolation: a checksum, archive listing, or successful dump command is not a restore test.

## Isolated Restore or Rehearsal

- Do not attach a restored copy to live production dependencies, real writers, notifications, or schedulers without explicit authorization for those effects.
- Preserve authentication and data sensitivity; do not expose an unauthenticated copy for convenience.
- Identify startup side effects such as cleanup, task-state transitions, auto-migrations, or background threads before starting the copy.
- Hold consumers and schedulers until replay, duplication, lock expiry, and idempotency behavior are understood.
- Record what isolation actually blocks and what remains reachable. Network flags, disabled units, or a written sandbox directive are not proof of isolation.
- Keep rehearsal-only unavailable upstreams, network proxies, CSP policies, and disabled task settings out of production defaults.

## Cutover

For a single-service replacement, stop the old instance and confirm process/port release before starting the new one. Avoid global legacy-manager operations that might activate unrelated programs.

For a coordinated stateful migration:

1. Block new writes at business entry points and from remote clients.
2. Pause schedulers and other task producers.
3. Drain or safely return in-flight work, then stop consumers.
4. Stop remaining writers and prevent automatic restart during final backup/restore.
5. Capture and verify the final backups. If the old system resumes writing, repeat the final capture.
6. Restore storage and data, start databases, and verify versions, objects, permissions, extensions, and readiness.
7. Select the prepared release/configuration and start APIs with production writes still restricted.
8. Validate data paths and representative behavior, then start consumers and one scheduler according to the approved queue strategy.
9. Switch approved proxy routes and admit writes. Record the cutover point and backup coverage for newly created data.

Stopping/rebuilding containers must preserve persistent storage. Do not use volume-deleting operations such as `down -v` during routine cutover or rollback.

Do not retire an upstream merely because it is excluded from a redeployment list. Resolve retained services' dependencies first. "Not redeployed" does not authorize deletion of its old data.

## Rollback

- Stop the new writers and preserve post-cutover data before changing the entry point.
- Restore the previous code/configuration only if it remains compatible with current state. A `current` link switch alone cannot reverse schema changes.
- Do not overwrite newer SQLite/database/queue state with an older snapshot. Define reconciliation or compatible recovery when writes have occurred.
- Prevent old and new instances from running simultaneously; re-check listeners, scheduler uniqueness, and restart policies.
- Retain previous artifacts until the agreed acceptance and retention conditions are met. Cleanup is a separate authorized operation.
- If the old OS or host has been replaced, "start the old VM" is not a rollback plan. Identify recoverable compute, system/VM materials when needed, and realistic restoration time before destructive installation.

## Acceptance Evidence

Apply the checks relevant to the deployment change; a full migration needs broader evidence than a route-only edit.

| Area | Evidence |
| --- | --- |
| Runtime contract | Correct UID/GID, code/configuration non-writable, intended writable paths, no personal-HOME dependency |
| Persistence | Correct original volumes/mounts, no accidental empty state, missing storage fails safely |
| Dependencies | Actual consumers reach the intended database/role, Redis DB, storage, and upstream services |
| Business behavior | Representative authorized operation and historical-data/file access; health/readiness alone are insufficient |
| Queue/scheduler | Safe recovery, no duplicate consumption or scheduling, consistent state/results |
| Proxy/static | Correct routes, resources, uploads/streaming where applicable; HTML 200 does not prove browser functionality |
| GPU, if required | Device/framework visibility and real model inference on the intended device, not just a device listing |
| Operations | Useful logs, retention, reconnect after dependency interruption, persistence after restart |
| Recovery | Actual isolated restore and rollback evidence, including post-cutover data handling |
| Unattended boot | Full-machine restart without login restores mounts, dependencies, and required services |

Report omitted checks and residual risks explicitly. A representative sample does not establish all formats, long-running load, or notification delivery. Do not call the deployment fully accepted when its required checks remain unverified.
