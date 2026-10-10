# Host Compatibility

Use this reference when discovery, inheritance, or sharing files affects the result. This is a documentation snapshot, not a promise about every installed version. Recheck the target host, launch directory, trust settings, and configuration; verification dates and sources are recorded in [Sources](sources.md).

## Format Is Not a Loader

The [AGENTS.md site](https://agents.md/) describes plain Markdown with no required fields or headings. Its examples are not policies for other repositories. The host decides which files enter context and how they interact.

A Markdown link is navigational guidance, not an automatic import. Claude's `@path` syntax, Codex's override filenames, and other tools' configuration are not interchangeable. Repository instructions do not grant tool permissions or replace CI, approvals, sandboxing, or deterministic enforcement.

## Codex

The [official discovery guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md) documents:

- Startup discovery: global guidance under `CODEX_HOME` (default `~/.codex`), then the project-root-to-current-directory chain. Globally, AGENTS.override.md is preferred over AGENTS.md; only the first nonempty file is used.
- At each project directory: `AGENTS.override.md`, then `AGENTS.md`, then configured `project_doc_fallback_filenames`; at most one instruction file is selected per directory. Empty files are skipped.
- Root-to-current-directory concatenation, with more local guidance later. Do not describe an override as additive to the same directory's AGENTS.md.
- A default `project_doc_max_bytes` of 32 KiB. Treat the active project chain as budgeted; splitting files does not by itself guarantee all their content loads.

The [advanced configuration page](https://learn.chatgpt.com/docs/config-file/config-advanced#project-instructions-discovery) calls the byte limit per-file, while the guide describes combined size. The [pinned loader implementation](https://github.com/openai/codex/blob/c3d3b142d10f4316b46e35aad7e5317e7e506cb7/codex-rs/core/src/agents_md.rs) uses a shared remaining project-document budget and truncates oversized content. For size-dependent work, verify the installed implementation rather than assuming the wording mismatch is resolved for all versions.

Initial discovery stops at the launch directory. Do not claim that starting at the repository root preloads every descendant file; check applicable local guidance when work moves into a subtree. Restart or start a fresh run to check changed startup guidance.

## Claude Code

The [official memory documentation](https://code.claude.com/docs/en/memory) describes:

- CLAUDE.md (including `.claude/CLAUDE.md`) and CLAUDE.local.md files above and at the current directory concatenate at startup. Descendant Claude files load on relevant reads, writes, or edits. Do not rely on contradictory files overriding each other deterministically.
- Direct AGENTS.md support requires v2.1.277+ and an enabled feature. By default, a project-path CLAUDE.md, `.claude/CLAUDE.md`, or CLAUDE.local.md suppresses direct AGENTS.md loading. User-level and managed CLAUDE.md do not count for that check.
- When eligible, startup discovery includes AGENTS.md and `.claude/AGENTS.md` above and at the current directory. A descendant AGENTS.md loads through the Read tool when that directory has none of the competing Claude files.
- The **Project instructions** setting changes this behavior. Verify it before claiming AGENTS.md alone works; some older-version sessions have additional availability restrictions.
- This repository-instruction discovery does not read AGENTS.override.md or AGENTS.local.md, or search `.agents/`; that is separate from skill discovery.
- `@path` expands imports relative to the importing file, up to four hops. Imports organize content but do not reduce loaded context.
- `.claude/rules/` supports path-scoped rules. The recommendation to keep CLAUDE.md under 200 lines is not a universal AGENTS.md limit or the separate auto-memory truncation rule.

## Share a Source Without Duplicating Policy

Preserve a working setup unless migration is requested:

| Choice | Use when | Check |
| --- | --- | --- |
| AGENTS.md directly | Target hosts actually discover it | Claude version, feature availability, and competing files/settings |
| CLAUDE.md imports `@AGENTS.md` | Claude needs an adapter or its own small additions | Keep both files adjacent; check existing content and import resolution |
| CLAUDE.md symlinks to AGENTS.md | No Claude-only content and the checkout supports symlinks | Windows/Git behavior; edit the target, not an independent copy |
| Conditional Markdown reference | Detailed material is relevant only to some tasks | State when to read it; do not call it guaranteed eager loading |

The import and symlink choices are supported in [Claude's sharing guidance](https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools). Prefer an import over a symlink for Windows consumers; Claude's Edit/Write tools refuse writes through a symlink. Do not replace an existing CLAUDE.md with a one-line adapter without preserving its distinct guidance.

## Verify Discovery Separately

When authorized to run the target host, inspect loaded instruction sources at the repository root and a relevant subtree, including override/competing-file cases. Codex's guide suggests summarizing active instructions and inspecting logs; Claude documents `/context` and `/doctor prompt-audit`. These are optional host observations, not commands to run automatically during document editing.

Record the host version, launch directory, relevant settings, and observed files. A model's assertion that it read a file is weaker evidence than host discovery output or logs, and neither proves behavioral compliance.
