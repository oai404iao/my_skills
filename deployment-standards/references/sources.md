# Sources and Scope

This skill is independently written from a user-provided local deployment archive named `ai_server_info` and the public backup references below, not copied from a third-party deployment framework.

## Source Material

| Original archive material | Contribution |
| --- | --- |
| `README.md`, `04-deployment.md` | Target directory, identity, permission, systemd/Compose, storage, and port conventions |
| `01-services.md`, `02-databases.md` | Artifact recovery, actual dependencies, engine-specific data semantics, and acceptance requirements |
| `03-system.md`, `05-migration.md` | Destructive-installation boundaries, coordinated stop-write, off-machine backups, restore and rollback requirements |
| `normalization/*.md` | Recorded production cutovers, service identities, permission checks, legacy-manager rollback, and privileged/GPU exceptions |
| `rehearsal/README.md`, `rehearsal/hostapps-notes.md`, `rehearsal/nginx-notes.md` | Isolation boundaries, configuration conversion, startup side effects, and limits of health/HTTP checks |

These are provenance labels, not required files in an installed skill. The original archive is not bundled; this skill does not depend on its machine-local path. Credentials, business data, operational scripts, host addresses, and transient service inventories are not included.

## Public Backup Practices

The backup-management addition independently synthesizes these primary sources. Public documentation is evidence, not authorization to run its examples or an endorsement of our chosen paths.

| Source | Adopted principle and limits |
| --- | --- |
| [FHS 3.0: `/var` hierarchy](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch05.html) | Separates mutable state from configuration/code; it does not mandate our `/var/backups` tree |
| [Borg: central repository server](https://borgbackup.readthedocs.io/en/stable/deployment/central-backup-server.html) | Central storage with per-client namespace/access restrictions; its account/HOME paths and Ansible/Salt setup are examples, not our required deployment |
| [Borg: quick start](https://borgbackup.readthedocs.io/en/stable/quickstart.html) | Capture consistency, capacity, key recovery, and tiered retention; the 7 daily / 4 weekly / 6 monthly example is a starting point, not a workload-independent guarantee |
| [restic: repository preparation](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html) | Managed repositories can use local or remote backends; password recovery and repository identity matter; no mandatory tool/vendor adoption |
| [restic: snapshot removal](https://restic.readthedocs.io/en/stable/060_forget.html) | Scoped retention, deletion previews, native maintenance, and append-only retention attack caveats; validate semantics against the installed tool/backend |
| [CISA: StopRansomware guide](https://www.cisa.gov/stopransomware/ransomware-guide) | Offline encrypted backups and actual recovery exercises; path selection alone does not protect against ransomware |
| [CISA and partner agencies: LockBit advisory, mitigation section](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-165a) | 3-2-1 and physically separate, segmented recovery copies; not proof that a specific host meets these goals |

Our exact `/var/backups/<scope>/<environment>/{pre-change,staging}/<backup-id>/` layout, backup-server `/srv/backups/...` example, set/manifest conventions, prohibition on scattered agent-created copies, and proposed pre-change retention floor are local baseline design choices. Existing protected project contracts take precedence; exceptions and recovery gaps must be explicit.

No third-party documentation text or example scripts are bundled by this addition, and it does not extend a third party's license to the original private archive.

## Deliberate Exclusions

- Fixed OS versions, IPs, administrator names/UIDs, SSH settings, and a temporary decision not to configure a firewall are project decisions, not general deployment standards.
- Rehearsal-only networking, proxying, unavailable upstreams, and disabled consumers are not production defaults.
- Legacy Supervisor retention, privileged security tasks, and GPU/device access illustrate documented exceptions, not universal prescriptions.
- Historical migration targets, recorded production state, and rehearsal results are distinct evidence types; none proves current host state.
- Example paths are baseline design choices. Existing confirmed project contracts take precedence.

No third-party license grant was supplied for the local archive; do not infer one or extend it to unrelated material. This skill makes no claim of official systemd, Docker, database-vendor, or agent-host endorsement.

Validation of this skill is static unless separately reported otherwise. Its wording does not establish successful host discovery, model compliance, production restart, business acceptance, or recovery testing.
