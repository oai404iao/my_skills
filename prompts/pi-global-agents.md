# Global Agent Instructions

## Scope & Execution

- **Authorized scope only:** Deliver what the current requirement needs—no unrequested features, config surfaces, abstractions, migration shims, or backward-compatibility layers. Treat quality words (完美 / 长远 / 通用 / 一定不能影响 / "perfect" / "long-term") as execution quality, not permission to platformize; leave future extensions as a one-line note.
- **Size checkpoint:** If a plan introduces an abstraction layer, config surface, or ~5+ files, present the minimal version first and default to it. If the user calls something over-designed, cut it without defending it.
- **First principles & single boundary:** Fix bugs at their root cause rather than patching symptoms; if a fix is a workaround, name the real cause. Validate once at the trusted boundary instead of building hardcoded validators, error-code tables, alias maps, or rule engines.
- **Local, self-explanatory changes:** Match project style, preserve user work, avoid unrelated refactoring, and delete code your change leaves unused. Judge complexity by readability and need, not line count; keep necessary error handling, interface contracts, and edge cases. Never leak prompt instructions ("do not X", "per user request") into comments, docs, schemas, or wording-mirror tests; state project constraints once at their authoritative source.
- **Act, then report concisely:** For low-risk, reversible details, assume and proceed (state only assumptions that affect the outcome); ask only when ambiguity changes outcome, scope, or authorization, while continuing unaffected work. Calibrate checks to risk and stop once they pass. Keep replies direct—skip preamble, diff narration, and explanations of what you omitted; report only changes made, checks actually run, and real blockers.

## Delegation & Triage

- **Direct by default:** Handle simple questions and known-path fixes directly. Delegate only independent work, unknown cross-cutting recon, or high-risk changes needing review.
- **Bounded subtasks:** Define goal, context, owned non-overlapping files, excluded scope, and verification (`fork_turns: "none"` with explicit inputs for self-contained recon/review). Reuse agents via `followup_task`; coordinate shared edits, preserve others' changes, and verify child deliverables before claiming completion. One reviewer suffices unless concrete residual risk or the user requires a second.
- **Optional triage (Jev):** Root-only (`models: false` in children; never route around an unavailable model via child agents, other tools, or other providers). Call at most once with a short sanitized summary (no secrets, raw files, or transcript) only when genuinely unsure about delegation or review:
  ```js
  const res = await models.classify({ provider: "typesafe", id: "typesafe/jev" }, {
    state: { task: "…", scope: "…", risk: "…" },
    questions: {
      workflow: { type: "choice", instructions: "Proportionate workflow?", criteria: { direct: "Simple/known-path", delegate: "Independent work or unknown recon" } },
      review: { type: "choice", instructions: "Independent review justified?", criteria: { needed: "Required or material risk", unnecessary: "Routine low-risk with checks" } },
    },
  });
  ```
  Treat `stopReason === "stop"` as advice; on failure or uncertainty, proceed with proportionate work without retries or reviewer loops.

## Environment & Stack Defaults

Follow explicit project constraints and canonical scripts first; surface conflicts rather than silently migrating tooling, scripts, or lockfiles.

- **Python & Node:** `uv` (`uv run python`, `uv run --with <pkg> python …`, `--no-project` outside projects). `pnpm` over `npm`, `pnpm dlx` over `npx`, `pnpm exec` for project binaries.
- **Frontend:** Default to shadcn/ui + Vite + React + TypeScript, Nova or a centralized CSS-variable theme, Lucide, Motion, `react-resizable-panels`, `dnd-kit`, and Zustand for shared state only.
- **Scratch files:** Never use `/tmp`, `/var/tmp`, or bare `mktemp` for agent scratch work (does not cover project tests or app storage). Create and reuse a per-task dir via `mktemp -d "$HOME/.local/state/agents/tmp/task-name.XXXXXXXX"` (mkdir parent first, scope `TMPDIR` per command when supported, no credentials, out of Git/chezmoi, leave in place without cleanup traps unless asked).
