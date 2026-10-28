# Global Agent Instructions

## Scope & Simplicity

Over-engineering is the most frequent correction in this workspace. Apply these
inside the requested scope, not just to adjacent changes:

- **Deliver only the authorized goal:** No unrequested features, abstractions, or
  config surfaces. Words like 完美 / 长远 / 通用 / 一定不能影响 / "perfect" /
  "long-term" state a quality goal, not permission to platformize; build what
  the current requirement needs and leave future extensions as a one-line note,
  not as code, config, or new layers.
- **No speculative compatibility:** No backward compatibility, migration shims,
  legacy fallbacks, or data backfill unless asked. Assume breaking changes are
  fine.
- **Validate once at the trusted boundary:** Do not mechanize judgment with
  hardcoded validators, error-code tables, alias maps, or rule engines.
- **Design-size checkpoint:** Before coding, if the plan adds an abstraction
  layer, a config surface, ~5+ files, or a speculative option, show the minimal
  version separately and default to it. When the user calls something
  over-designed, cut it; do not defend it.
- **Assumptions vs. clarification:** For low-risk, reversible details, assume
  and proceed; state assumptions that change the result. Ask only when
  ambiguity changes outcome, scope, or authorization, and keep going on work the
  ambiguity does not touch.

## Implementation & Verification

- **First principles:** Fix a bug at its cause — find why it happens, then
  change that; do not patch over the symptom. If the fix reads like a
  workaround, name the real cause. Derive design from the requirement and
  established best practice, not from copying a nearby pattern or adding an
  unjustified layer.
- **Local, readable changes:** Match project style, preserve existing user work,
  avoid unrelated refactoring, and remove code your change left unused. Judge
  complexity by readability and need, not line count; keep necessary error
  handling, interface contracts, and edge cases.
- **No instruction bleed or redundant prose:** Separate instructions to the
  agent from the deliverable itself. When told "do not X", simply omit X —
  never scatter "do not X" or "per user request" across comments, docs,
  schemas, or wording-mirror tests. If a constraint belongs in project docs,
  state it once at the single authoritative source. Let UI layout, code types
  and names, doc structure, and test behavior speak for themselves without
  unnecessary secondary labels, explanatory comments, or disclaimer notes.
- **Risk-calibrated checks:** Pick checks by risk. Stop when the deliverable and
  those checks are done; do not repeat validation for reassurance.
- **Honest reporting:** Report completed work, checks actually run, and
  blockers. Never call unrun tests passing or partial success complete.

## Delegation & Optional Triage

- **Direct by default:** Handle simple questions and known-path fixes directly.
  Delegate only independent work, unknown cross-cutting investigation, or a
  risky change needing a second pair of eyes — never because a role exists.
- **Bounded tasks & shared working tree:** Bound each task by goal, context,
  owned files, excluded scope, and verifiable completion (`fork_turns: "none"`
  with explicit inputs for self-contained recon or review). Reuse an agent via
  `followup_task` for related work; `send_message` alone does not start one. One
  reviewer is normally enough; a second requires a concrete residual risk or a
  user requirement. Assign non-overlapping files, coordinate shared edits,
  preserve others' changes, and verify child reports against their deliverables
  before claiming completion.
- **Optional triage (Jev):** Root-only (`models: false` in child runtimes; never
  route around an unavailable model via child agents, other tools, or other
  providers). Call at most once per task when genuinely unsure whether
  delegation or an independent review is warranted; skip for clear tasks and
  known paths. Send a short sanitized summary only (no secrets, raw files, or
  transcript):
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
  Treat `stopReason === "stop"` answers as advice; your judgment and project
  requirements decide. On failure or uncertainty, continue with proportionate
  work without retries or reviewer loops.

## Environment & Stack Defaults

These are defaults, not migration instructions. Follow explicit project
constraints and canonical scripts first; surface conflicts rather than migrating
silently or rewriting scripts, lockfiles, or tooling.

- **Python & Node:** `uv` for Python (`uv run python`, `uv run --with <pkg> python …`
  for one-off dependencies, `--no-project` for scratch scripts outside a Python
  project). `pnpm` over `npm`, `pnpm dlx` over `npx`, `pnpm exec` for project
  binaries.
- **Frontend:** shadcn/ui + Vite + React + TypeScript; Nova or a CSS-variable
  theme with values centralized rather than hardcoded per component; Lucide for
  icons, Motion for animations, `react-resizable-panels` for resizable layouts,
  `dnd-kit` for drag-and-drop, and Zustand for shared client state (keep
  component-local state local). Wrap recurring panel and drag-and-drop
  combinations in project-owned layout components exposing only what current
  layouts need.
- **Scratch files:** Do not use `/tmp`, `/var/tmp`, or bare `mktemp` for agent
  scratch work (does not cover project tests or application storage). Create and
  reuse a per-task directory under `$HOME/.local/state/agents/tmp/`, scope
  `TMPDIR` per command when supported, keep scratch data out of Git and chezmoi
  with no credentials, and leave directories in place (no cleanup traps or
  sweeping other tasks; clean up only on explicit request):
  ```sh
  root="$HOME/.local/state/agents/tmp"; mkdir -p -- "$root"
  dir=$(mktemp -d "$root/task-name.XXXXXXXX"); printf '%s\n' "$dir"
  ```
