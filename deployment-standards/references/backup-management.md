# Backup Management

Read when creating, locating, reviewing, retaining, or restoring deployment backups, including a single configuration file copied before an edit. This reference governs storage and lifecycle; use [Release and recovery](release-and-recovery.md#backup-contract) for capture consistency and engine-specific procedures.

These are this skill's baseline conventions, not a universal Linux standard or proof of an existing project's policy. Use an established, protected backup root when confirmed; record its mapping to the roles below rather than creating a competing hierarchy. Examples contain placeholders, not commands or authorized resources.

## Choose the Destination Before Writing

1. Identify the source host, environment, service or shared-system scope, backup purpose, sensitivity, and intended recovery point.
2. Resolve an **absolute local destination or explicit repository endpoint** from the project's backup contract. Without an existing contract, propose the baseline below and create only resources within the authorized task.
3. Verify destination ownership/access, available capacity, and required storage mounts. If a dedicated filesystem or remote mount is required, verify its identity and fail closed when absent; do not fill the root filesystem underneath an unmounted directory.
4. Create a new, restricted backup set, capture it with the appropriate method, and record verification and restore instructions before the dependent change proceeds.

Do not use the current working directory, source-file siblings (`.bak`, `.old`, timestamp suffixes), Git/worktrees, release directories, web roots, configuration include directories, application data directories, personal HOME, `/tmp`, or `/var/tmp` as ad hoc deployment backup destinations. A Git commit is useful for tracked non-secret configuration, but does not replace backup of untracked state or secrets.

If the destination is unavailable, permission is denied, or capacity is insufficient, report the blocker and request an approved destination/access change. Do not silently fall back to another location, escalate privileges, overwrite a previous backup, or delete older sets to make room. Continue work that does not depend on that backup. Preserve documented application/package-managed backup locations; this prohibition targets new agent-created copies, not permission to relocate existing files.

## Unified Storage Roles

Use one configured local backup root per host, defaulting to `/var/backups`. Separate environments and scopes beneath it:

| Role / backup type | Default destination | Required distinction |
| --- | --- | --- |
| Before-edit copies of configuration, units, proxy settings, Compose files, or necessary secrets | `/var/backups/<scope>/<environment>/pre-change/<backup-id>/config/` | Short-term rollback aid; preserve original source paths and metadata; never leave copies in active include directories |
| Database exports, supported physical backups, SQLite backups, required Redis persistence files | `/var/backups/<scope>/<environment>/staging/<backup-id>/database/` | Engine-supported capture, not a copy of a live data directory |
| Uploads, business outputs, unique models, required file logs | `/var/backups/<scope>/<environment>/staging/<backup-id>/files/` | Preserve database/file relationships and required metadata; exclude only verified rebuildable data |
| Effective configuration and secrets captured with a scheduled backup or migration | `/var/backups/<scope>/<environment>/staging/<backup-id>/config/` | Keep with the corresponding data recovery point; protect even if the live file was publicly readable |
| Host-wide recovery materials, package/service inventory, disk/VM images | `/var/backups/host/<environment>/staging/<backup-id>/system/` | Check image consistency and size; stream large images to approved independent storage rather than exhausting local space |
| Retained disaster-recovery backups | Approved backup server, NAS, removable storage, or object-storage repository; filesystem baseline on a backup server: `/srv/backups/<site>/<source-host>/<environment>/<scope>/` | Must survive loss of the source machine; a local directory or second partition alone does not satisfy this |
| Prior releases, container images, reproducible build artifacts | Existing release directory or artifact/image registry | Release retention is not a database/file backup; export irreplaceable artifacts to an approved backup set when needed |
| Scratch output or extracted restore/rehearsal copies | Host-approved task workspace or explicitly provisioned isolated restore volume | Not a retained backup; no production restore into the live source path without authorization |

`<scope>` is a verified service/stack name or `host` for shared system material; do not guess ownership of shared databases. The local host is implicit in the root but must be recorded in the manifest. The central repository identifies the source host explicitly. Prevent identifier collisions and path traversal; do not use unsanitized user input as path components.

`pre-change` and `staging` distinguish purposes, not levels of disaster protection. A pre-change set containing data uses the same `database/` and `files/` children. A coordinated backup uses one set ID for all required components, with a consistency window recorded; shared-instance material may use a shared scope with consumer mappings.

Choose one retained repository arrangement according to access boundaries. For Borg/restic or another managed format, use repository/snapshot IDs, labels, and manifests to express these identities; **do not impose this loose-file tree inside the tool's internal repository**. Isolate hosts, environments, and tenants by access control or separate repositories where required. Centralization is a naming and management contract, not authorization to provision a server, bucket, paid service, or transfer sensitive data.

Avoid redundant full local copies when the approved workflow streams directly to a repository. Record the repository endpoint and snapshot ID instead of inventing a staging file. Use an existing local repository if contracted, but keep its role separate from export staging and do not count it as off-machine storage.

## Set Identity and Inventory

For loose-file sets, use a collision-resistant ID such as `<UTC-YYYYMMDDTHHMMSSZ>-<purpose>-<unique-suffix>`; purposes include `pre-edit`, `scheduled`, and `pre-migration`. Create it exclusively, never reuse `backup`, `latest`, or a timestamp-only name as an overwrite target. Partial output stays identifiable as incomplete and must not be presented as recoverable.

Each set has a protected manifest (for example, `manifest.json` or `manifest.md`) containing:

- Source host, environment, scope, purpose/change reference, set ID, capture start/end time, and responsible owner.
- Original absolute paths, actual volume/database identities and consumers, included components, and exclusions with reasons.
- Tool/engine versions, capture/stop-write semantics, required ownership/ACLs/xattrs/symlink targets, and compatible restore prerequisites.
- Artifact sizes and checksums (or tool-native snapshot ID and integrity evidence); completed, incomplete, or failed capture status.
- Local location, retained repository reference, transfer/verification status, encryption method, and protected key references.
- Restore steps and destination mapping, retention/hold conditions, checks actually run, and restore-test date/result or explicitly `not tested`.

Keep passwords, connection strings with credentials, and business record samples out of manifests and reports. Protect the manifest itself: paths and inventory can be sensitive. Retain it with the artifacts or in the managed repository, not only on the source machine.

Exclude backup destinations and restore workspaces from recursive source capture to avoid backing up backups. Do not blanket-exclude `/var/backups` when staged database exports are deliberately the inputs to the retained backup job; list those inputs explicitly.

## Protection and Failure Domains

- Backups are controlled by the backup administrator or a dedicated backup identity, not writable by the application's runtime user. Grant only the source-read and destination-write access actually required.
- For loose artifacts, start with restrictive creation permissions, such as `umask 077`, directories `0700`, and files `0600`; use a narrowly scoped group only when necessary. Store original source permissions inside an archive or manifest for restoration rather than exposing the backup with those same permissions.
- Encrypt retained backups containing secrets or sensitive data, protect local plaintext staging, and use authenticated encrypted transport. Compression and filesystem modes are not encryption. Keep recovery keys/passphrases independently recoverable in approved secret storage; encryption key files embedded by a backup tool do not replace separate protection of the unlock secret.
- For critical production data, target 3-2-1: production plus two backup copies, across two distinct storage media/types, with one off-site. Also require an offline or enforced immutable/append-only recovery copy. Record actual failure domains and any accepted gaps; another directory, RAID, replication, or snapshots on the source disk are not independent disaster recovery.
- Verify the chosen tool/backend supports the protection promised. Separate routine backup credentials from destructive maintenance privileges where supported; an append-only label alone does not prove enforcement. Do not give the application backup repository credentials.

These storage arrangements do not replace database consistency, cross-service capture coordination, or isolated restore testing.

## Retention, Cleanup, and Recovery

Record an owner, maximum acceptable data loss (RPO), target recovery time (RTO), capture/transfer cadence, retention, capacity limits, failure alerts, and restore-test cadence in the deployment contract. Daily backups are insufficient if the accepted RPO is shorter.

When proposing a new policy, start with the following defaults and adapt them to the confirmed workload; these are recommendations, not permission to enable jobs or delete data:

| Category | Proposed retention |
| --- | --- |
| Pre-change rollback sets | Keep through acceptance and the agreed rollback window; propose at least 7 days after acceptance, longer if unresolved |
| Local staging | Eligible for cleanup only after retained-copy verification and any local rollback hold have both cleared |
| Retained recurring sets | Start with 7 daily, 4 weekly, and 6 monthly recovery points; account for the selected tool's selection/grouping semantics |
| Final pre-migration / destructive-operation sets | Explicit hold until recovery is verified, acceptance is complete, and the owner approves retirement |
| Failed/incomplete sets and restore workspaces | Track separately; cleanup requires the approved task/policy scope and must preserve needed diagnostic evidence |

Retention sampling is not proof of successful capture on every day. For append-only repositories, account for forged/empty snapshots in maintenance policy; do not blindly apply count-based thinning that could displace known-good copies. Use the tool's recommended protected time window and preserve known-good held points.

Before deletion, identify the exact host/environment/scope and sets, check holds and dependency chains (including base backups and required WAL/incrementals), and preview the deletion list where supported. Delete only under explicit authorization or an already approved retention job. Use tool-native maintenance for managed repositories; no manual deletion of chunks, indexes, or bucket objects to simulate pruning. A successful new capture does not authorize removing the previous known-good recovery point.

For authorized scheduled operations, alert on capture or transfer failure, stale recovery points, integrity problems, and insufficient capacity. Verify retained-copy readability and integrity before calling transfer complete. Do not change cleanup policy during an outage merely to recover disk space.

Restore into a provisioned, protected, isolated target; record actual data/service checks and measured recovery time. Integrity checks, archive listings, and successful transfer are not restore tests. For a new backup procedure or format/destination change, verify an isolated restore before claiming recoverability; recurring tests follow the approved cadence. Read the isolation and post-cutover data rules in [Release and recovery](release-and-recovery.md).

When an agent finishes a backup-related change, report: **what was captured, absolute location or repository/snapshot reference, capture consistency, checks actually run, off-machine status, retention/cleanup owner, and remaining recovery gaps**. Do not report “backed up” when only an incomplete export or unverified copy exists.
