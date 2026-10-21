# Global Agent Instructions

## Design simplicity (anti-over-engineering)

Over-engineering is the most frequent correction in this workspace. These are
hard defaults and they apply INSIDE the requested scope, not just to adjacent
changes:

- No backward compatibility, migration shims, legacy fallbacks, or old-data
  backfill unless the user explicitly asks for them. Assume breaking changes
  are acceptable by default.
- Words like 完美 / 长远 / 通用 / 一定不能影响 / "perfect" / "long-term"
  describe quality goals, not authorization to platformize. Implement only
  what the current stated requirement needs; mention future extensions as
  one-line notes in the final message, never as extra code, schemas, tiers,
  modes, or config surfaces.
- Do not mechanize judgment: no hardcoded validators, closed error-code sets,
  alias tables, or rule engines...
- Validate once at the trusted boundary. Do not duplicate the same check
  across layers.
- Design-size checkpoint: before writing code, if the plan adds a new
  abstraction layer, a new config surface, more than ~5 new files, or any
  speculative option, present the minimal version and the additions as
  separate items and default to the minimal version.
- When the user says something is over-designed: cut it, do not defend it.

## Coding principles

- Deliver the authorized goal without adding unrequested features,
  abstractions, or configuration.
- Proceed with reasonable assumptions for low-risk, reversible details;
  state assumptions that affect results. Ask when ambiguity materially changes
  the outcome, scope, or authorization; continue unaffected authorized work.
- Make local changes in the project's style and preserve existing user work.
  Avoid unrelated refactoring; remove unused code introduced by your changes.
- Judge complexity by readability and actual needs, not line count. Preserve
  necessary error handling, interface contracts, and edge-case behavior.
- Define verifiable outcomes and choose checks according to risk and project
  requirements. Stop when requested deliverables and required, risk-appropriate
  checks are complete; do not expand or repeat validation merely for reassurance.
- Keep reports proportionate to the task: completed work, checks actually run,
  and remaining blockers. Never claim unrun tests passed or present partial
  success as full completion.

## Mandatory frontend standards

These are mandatory, unified constraints for frontend work, not optional
preferences. Do not substitute alternative stacks or libraries without explicit
user approval. If an existing project conflicts with these requirements, surface
the conflict and confirm migration scope rather than silently making an exception
or performing an unrelated migration. Add feature-specific dependencies only
when their capabilities are needed.

- Use shadcn/ui (oneUI) + Vite + React + TypeScript as the frontend stack.
- Use Nova or a custom CSS-variable-based theme consistently across the UI.
  Keep theme values centralized rather than hardcoding competing styles in
  individual components.
- Use Lucide for icons.
- Use Motion for animations.
- Use `react-resizable-panels` for resizable panel layouts and `dnd-kit` for
  drag-and-drop interactions.
- Use Zustand for shared client-side state; keep component-local state local.
- Encapsulate recurring resizable-panel and drag-and-drop combinations in
  project-owned layout components. Reuse those components instead of repeating
  integration logic; expose only what current layouts need, not a speculative
  general-purpose layout framework.

## Task workflow

- At the start of every new user task, the root agent must call Jev once through
  codemode's `models.classify` before task work, when that API is exposed and the
  call is permitted. This includes simple fixes and questions, not just borderline
  cases. Use already available context; mark unknowns rather than exploring first.
  Continuations, status replies, tool results, and child messages within the same
  task do not trigger another call.
- Use provider `typesafe`, model ID `typesafe/jev` (the configured System One
  endpoint via Command Code). Send only a short sanitized task, scope/independent
  work boundaries, and risk/unknowns summary, including any user or repository
  delegation/review constraints already known. Never send secrets, raw files,
  or the full transcript. Replace the example summaries below for the actual task;
  ask both questions in the same call:

  ```js
  if (typeof models === "undefined") return { fallback: true };
  const result = await models.classify(
    { provider: "typesafe", id: "typesafe/jev" },
    {
      state: { task: "Sanitized goal", scope: "Known boundaries", risk: "Risks and unknowns" },
      questions: {
        workflow: {
          type: "choice",
          instructions: "Which proportionate workflow fits this task?",
          criteria: {
            direct: "Simple question or known-path fix; delegation adds little",
            delegate: "Useful independent work or unknown cross-cutting investigation",
          },
        },
        review: {
          type: "choice",
          instructions: "Is one independent review justified?",
          criteria: {
            needed: "User/repository requires it, or material risk needs a second pair of eyes",
            unnecessary: "Routine low-risk work with adequate relevant checks",
          },
        },
      },
    },
  );
  return result;
  ```

- Treat the result as advisory, not authorization, a correctness guarantee, a
  waiver of required checks, or a replacement for user decisions. Check
  `stopReason === "stop"` and correctly typed answers with the defined labels.
  If the API is unavailable, the call fails, or an answer is invalid or uncertain,
  choose proportionate work using the task and evidence; do not retry classification
  or start reviewer loops. Apply user restrictions and actual project requirements
  regardless of the result.
- Only the root classifies. Delegated agents do not repeat this step; their
  codemode runtime has `models: false`. Do not bypass unavailable models through
  child proxies, other tools, or alternate providers.

## Agent delegation

- Handle simple questions and known-path fixes directly. There is no fixed
  scout → worker → reviewer pipeline. Delegate only useful independent work,
  unknown cross-cutting investigation, or a risky change needing a second pair
  of eyes, never merely because roles exist.
- Keep delegation bounded: give the goal, necessary context, owned files,
  excluded scope, and verifiable completion criteria. Use one bounded reviewer
  when justified or requested, address findings, and run relevant regression
  checks. Another reviewer requires a concrete residual high-risk issue or a
  user/repository requirement, not confirmation that the first review was right.
- For self-contained reconnaissance or review, consider `fork_turns:"none"`
  and supply the necessary paths, decisions, and constraints explicitly.
  Use inherited history when the task genuinely depends on it.
- Reuse an existing agent for related follow-up work. Include the new task and
  current decisions in `followup_task`; `send_message` alone does not start an
  idle agent. Confirm receipt only when a changed decision materially affects
  scope or correctness, not for routine messages; tool acceptance alone is not
  evidence it was applied.
- Let the main agent coordinate parallel work by default. Delegate further only
  for a distinct need; avoid occupying every slot with parents waiting for
  children. At capacity, continue independent work or wait for active work
  rather than repeatedly retrying or interrupting unrelated agents.
- Agents share the working tree. Assign non-overlapping files where practical;
  coordinate shared-file edits before making them and preserve others' changes.
- Check child reports against their deliverables and required checks before
  claiming completion; an agent's completed status alone is not evidence.

## Tool selection

- Prefer `uv` for running Python, especially when dependencies are needed.
  Use `uv run python` or `uv run script.py`; for one-off dependencies, use
  `uv run --with <package> python ...` rather than installing into system Python.
  For scratch scripts unrelated to a Python project, add `--no-project` to
  avoid installing or syncing that project's dependencies.
- Prefer `pnpm` over `npm`, and `pnpm dlx <package>` over `npx <package>` for
  one-off package execution. Use `pnpm exec <command>` for project-installed
  binaries rather than downloading a separate copy.
- These are defaults, not package-manager migration instructions. Honor explicit
  project requirements and canonical scripts; do not rewrite scripts, replace
  lockfiles, or add tooling dependencies merely to enforce these preferences.

## Temporary workspace

- Avoid `/tmp`, `/var/tmp`, and bare `mktemp` for agent-created scratch files.
  Use `$HOME/.local/state/agents/tmp/` as the shared agent scratch root.
- Create a fresh task directory before writing temporary scripts, downloads,
  logs, or intermediate output. Use a descriptive task prefix and `mktemp`'s
  random suffix to avoid collisions between sessions and subagents:

  ```sh
  (
      set -eu
      umask 077
      scratch_root="$HOME/.local/state/agents/tmp"
      mkdir -p -- "$scratch_root"
      task_dir=$(mktemp -d "$scratch_root/task-name.XXXXXXXX")
      printf '%s\n' "$task_dir"
  )
  ```

- Capture the printed absolute path and reuse it in later tool calls; shell
  variables do not persist between calls. Resolve it before temporarily
  changing `HOME` or XDG variables, and never reconstruct it from rebound
  environment variables.
- When a command supports `TMPDIR`, scope `TMPDIR` to that task directory for
  that command only. Do not change the login environment or assume every tool
  honors `TMPDIR`.
- Leave task directories and their contents in place after use. Do not add
  cleanup traps, delete them automatically, or sweep other tasks' directories.
  Cleanup requires an explicit user request for a specific path.
- Scratch data is machine-local mutable state, not configuration: keep it out
  of Git and chezmoi. Do not store credentials in retained scratch files.
- This policy governs agent-created scratch work; it does not require rewriting
  existing project tests or application-managed temporary storage. Preserve
  documented test isolation and cleanup contracts.
