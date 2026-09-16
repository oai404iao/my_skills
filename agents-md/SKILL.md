---
name: agents-md
description: Create, update, or review AGENTS.md and equivalent repository instructions using verified project evidence. Use when the user requests work on agent instructions, not for ordinary code changes or repository exploration.
---

# Repository Instructions Guide

Help agents make correct changes by documenting project-specific commands, sources of truth, constraints, and relevant verification paths. The target is an operational guide, not a README or a collection of generic coding advice.

## Scope and Authority

- Match the requested action: a review produces findings; creation or updating produces document changes. Do not edit files when the user asks only for a review.
- Treat this skill's structure and examples as defaults, not policies to impose on a project. Follow applicable higher-priority instructions and the user's authorized task.
- Include a project rule only when supported by explicit user requirements or authoritative project evidence. Do not turn personal preferences, conventions from another repository, or skill examples into mandatory project policy.
- Do not automatically add instructions about comments, TODOs, commit formats, branch strategy, or coding style. Document them only when they are actual project requirements.
- Preserve useful project-specific guidance. Keep unrelated policy changes out of a targeted update.
- Do not create AGENTS.md merely because a repository is unfamiliar. Do not add requirements to read an entire repository map before every task.

## Gather Relevant Evidence

For creation, inspect enough of the repository to identify its working structure. For a targeted update, inspect the current instructions and evidence for the affected sections rather than inventorying the whole repository again.

Useful sources include:

- Existing root and nested agent instructions, README, CONTRIBUTING, and architecture documentation
- Package manifests, workspace configuration, lockfiles, Makefile, justfile, and task scripts
- CI workflows and test, lint, build, and format configuration
- Schemas, generated-file headers, code-generation inputs, and nearby implementation
- Test fixtures and representative tests that establish verification paths

Prefer canonical project wrappers over incidental commands. Verify the working directory, arguments, and environment requirements of each documented command. A command found in a manifest is not proof that it has been run successfully.

Resolve contradictions using explicit requirements and authoritative project sources. If an important policy remains genuinely ambiguous, identify the conflict and ask a focused question. Omit nonessential unverified content rather than blocking the whole task or inventing a rule.

## Select Only Useful Sections

Choose sections that help an agent make decisions in this repository:

| Section | Include when it answers |
| --- | --- |
| Project overview | What does this project do, and what runtime or workspace boundaries matter? |
| Repository layout | Where should a particular kind of change go? |
| Commands | Which build, test, lint, format, or development commands are canonical? |
| Sources of truth | Which schema, config, generator, or registry owns a fact? |
| Architecture and patterns | Which flows, contracts, or existing helpers constrain changes? |
| Gotchas | Which evidenced failure modes require special handling? |
| Verification | Which checks cover a change, and which need services, credentials, or substantial time? |
| Common workflows | Which real multi-file changes have a required update order? |
| Local conventions | Which established conventions materially affect work? |

This is a menu, not a required outline. Small repositories may need only a few sections. Do not add empty headings, repeat README content, enumerate every file, or fabricate design patterns to fill a template.

Keep long architecture maps and examples in supporting documents when useful. Link them with a clear reading condition instead of making every task load them.

## Write Actionable Guidance

- Name exact paths and source-of-truth files.
- Explain directory responsibilities rather than restating directory names.
- Use commands verified against scripts or CI, including their working directory.
- Mark checks that access live services, change external state, need credentials, or are slow.
- Describe a gotcha with its cause, affected area, and correct handling.
- Distinguish mandatory project constraints from optional recommendations.
- Scope verification to the affected behavior while preserving required project checks.

Examples of specificity, not commands to copy into another project:

- `make test-core PROVIDER=openai` instead of "run the tests," if that target exists.
- `cd ui && npm run build` when the UI package owns that script.
- `transports/config.schema.json` as the config source of truth, only if verified.

Do not add generic comment rules or bans on TODO/FIXME. If the project has an explicit comment policy, document its actual scope rather than replacing it with this skill's preferences.

## Update Existing Instructions

1. Read the target document and applicable parent or nested instructions.
2. Identify the requested changes and the evidence needed to support them.
3. Patch affected sections. Restructure the whole document only when requested or necessary to make it usable.
4. Remove or correct stale facts within scope; flag unrelated suspected policies rather than silently replacing them.
5. Update affected links and command examples.
6. Review the result for contradictions, invented requirements, and unnecessary duplication.

## Verify and Report

Check that modified paths and links resolve, command examples match authoritative configuration, and new rules have a clear basis. Use targeted checks for the changed content; do not run builds, live-service tests, or network operations merely because they appear in the document.

For behavior changes to agent instructions, review representative cases:

- A review-only request yields findings without edits.
- A one-command update does not add comment, branch, or commit policies.
- Missing evidence causes an omission or an explicit uncertainty, not a fabricated requirement.
- Existing project conventions are preserved instead of replaced by example preferences.

Report the sections changed or findings discovered, the evidence checked, and any remaining uncertainty. Distinguish commands inspected from commands actually executed. Do not imply that documentation review proves the project's implementation or tests pass.
