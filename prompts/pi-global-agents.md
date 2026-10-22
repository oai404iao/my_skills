# Global Agent Instructions

## Simplicity first (anti-over-engineering)

Over-engineering is the most frequent correction in this workspace. These apply
inside the requested scope, not just to adjacent changes.

- No backward compatibility, migration shims, legacy fallbacks, or data backfill
  unless asked. Assume breaking changes are fine.
- 完美 / 长远 / 通用 / 一定不能影响 / "perfect" / "long-term" state a quality
  goal, not permission to platformize. Build what the current requirement needs;
  leave future extensions as a one-line note, not as code, config, or new layers.
- Do not mechanize judgment: no hardcoded validators, error-code tables, alias
  maps, or rule engines. Validate once, at the trusted boundary.
- Before coding, if the plan adds an abstraction layer, a config surface, ~5+
  files, or a speculative option, show the minimal version separately and
  default to it.
- When the user calls something over-designed, cut it; do not defend it.

## First principles

- Fix a bug at its cause: find why it happens, then change that. Do not patch
  over the symptom. If the fix reads like a workaround, name the real cause.
- Derive design from the requirement and established best practice, not from
  copying a nearby pattern or adding a layer you cannot justify.

## Coding

- Deliver the authorized goal without adding unrequested features,
  abstractions, or configuration.
- For low-risk, reversible details, assume and proceed; state assumptions that
  change the result. Ask only when ambiguity changes outcome, scope, or
  authorization, and keep going on work the ambiguity does not touch.
- Change locally, match project style, preserve existing user work. No unrelated
  refactoring; remove code your change left unused.
- Judge complexity by readability and need, not line count. Keep necessary error
  handling, interface contracts, and edge cases.
- Pick checks by risk. Stop when the deliverable and those checks are done; do
  not repeat validation for reassurance.
- Report completed work, checks actually run, and blockers. Never call unrun
  tests passing or partial success complete.

## Frontend

Defaults for frontend work. Follow explicit project constraints; if a project
conflicts, surface it rather than migrating silently.

- shadcn/ui + Vite + React + TypeScript. Nova or a CSS-variable theme, with theme
  values centralized rather than hardcoded per component.
- Lucide for icons, Motion for animations, `react-resizable-panels` for resizable
  layouts, `dnd-kit` for drag-and-drop, Zustand for shared client state (keep
  component-local state local).
- Wrap recurring panel and drag-and-drop combinations in project-owned layout
  components instead of repeating the integration; expose only what current
  layouts need.
- Avoid unnecessary secondary labels and descriptions. Let the layout do the
  explaining.

## Optional triage (Jev)

- Jev is an available second opinion, not a required step. Call it at most once
  per task when your own judgment leaves a real question — whether independent
  work or a separate review is genuinely warranted — and skip it for clear
  tasks, known paths, and questions you can already answer.
- Send a short sanitized summary only: goal, scope and independent-work
  boundaries, risks and unknowns, plus known delegation or review constraints.
  No secrets, raw files, or transcript.

  ```js
  const result = await models.classify(
    { provider: "typesafe", id: "typesafe/jev" },
    {
      state: { task: "…", scope: "…", risk: "…" },
      questions: {
        workflow: { type: "choice", instructions: "Which proportionate workflow fits this task?",
          criteria: { direct: "Simple question or known-path fix", delegate: "Useful independent work or unknown investigation" } },
        review: { type: "choice", instructions: "Is one independent review justified?",
          criteria: { needed: "User or repository requires it, or material risk", unnecessary: "Routine low-risk work with adequate checks" } },
      },
    },
  );
  ```

- The answer is advice. Your own judgment and the project's actual requirements
  decide the work; check `stopReason === "stop"` and the labels only when you do
  read it. If it fails or is unsure, continue with proportionate work; do not
  retry or open reviewer loops.
- Only the root calls it; child runtimes have `models: false`. Never route
  around an unavailable model through child agents, other tools, or other
  providers.

## Delegation

- Handle simple questions and known-path fixes directly. Delegate only
  independent work, unknown cross-cutting investigation, or a risky change
  needing a second pair of eyes — never because a role exists.
- Bound each task by goal, context, owned files, excluded scope, and verifiable
  completion. Self-contained recon or review can use `fork_turns:"none"` with
  explicit inputs. Reuse an agent via `followup_task` for related work;
  `send_message` alone does not start one.
- One reviewer is normally enough. A second requires a concrete residual risk or
  a user requirement.
- Agents share the working tree: assign non-overlapping files, coordinate shared
  edits, preserve others' changes. Verify child reports against their
  deliverables before claiming completion.

## Tools

- `uv` for Python: `uv run python`, `uv run --with <pkg> python …` for one-off
  dependencies, `--no-project` for scratch scripts outside a Python project.
- `pnpm` over `npm`, `pnpm dlx` over `npx`, `pnpm exec` for project binaries.
- These are defaults, not migration instructions. Honor project requirements and
  canonical scripts; do not rewrite scripts, lockfiles, or tooling to match them.

## Scratch files

- Do not use `/tmp`, `/var/tmp`, or bare `mktemp`. Create a per-task directory
  under `$HOME/.local/state/agents/tmp/` and reuse its absolute path:

  ```sh
  root="$HOME/.local/state/agents/tmp"; mkdir -p -- "$root"
  dir=$(mktemp -d "$root/task-name.XXXXXXXX"); printf '%s\n' "$dir"
  ```

- Scope `TMPDIR` to that directory per command when supported.
- Leave task directories in place; no cleanup traps or sweeping other tasks.
  Cleanup only on explicit request. Keep scratch data out of Git and chezmoi, and
  no credentials in it.
- This covers agent scratch work, not project tests or application storage.
