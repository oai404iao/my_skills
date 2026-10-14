# Sources and Scope

This skill is independently written from a user-provided local deployment archive named `ai_server_info`, not copied from a third-party deployment framework.

## Source Material

| Original archive material | Contribution |
| --- | --- |
| `README.md`, `04-deployment.md` | Target directory, identity, permission, systemd/Compose, storage, and port conventions |
| `01-services.md`, `02-databases.md` | Artifact recovery, actual dependencies, engine-specific data semantics, and acceptance requirements |
| `03-system.md`, `05-migration.md` | Destructive-installation boundaries, coordinated stop-write, off-machine backups, restore and rollback requirements |
| `normalization/*.md` | Recorded production cutovers, service identities, permission checks, legacy-manager rollback, and privileged/GPU exceptions |
| `rehearsal/README.md`, `rehearsal/hostapps-notes.md`, `rehearsal/nginx-notes.md` | Isolation boundaries, configuration conversion, startup side effects, and limits of health/HTTP checks |

These are provenance labels, not required files in an installed skill. The original archive is not bundled; this skill does not depend on its machine-local path. Credentials, business data, operational scripts, host addresses, and transient service inventories are not included.

## Deliberate Exclusions

- Fixed OS versions, IPs, administrator names/UIDs, SSH settings, and a temporary decision not to configure a firewall are project decisions, not general deployment standards.
- Rehearsal-only networking, proxying, unavailable upstreams, and disabled consumers are not production defaults.
- Legacy Supervisor retention, privileged security tasks, and GPU/device access illustrate documented exceptions, not universal prescriptions.
- Historical migration targets, recorded production state, and rehearsal results are distinct evidence types; none proves current host state.
- Example paths are baseline design choices. Existing confirmed project contracts take precedence.

No third-party license grant was supplied for the local archive; do not infer one or extend it to unrelated material. This skill makes no claim of official systemd, Docker, database-vendor, or agent-host endorsement.

Validation of this skill is static unless separately reported otherwise. Its wording does not establish successful host discovery, model compliance, production restart, business acceptance, or recovery testing.
