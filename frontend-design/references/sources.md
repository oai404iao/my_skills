# Frontend Design Sources

Retrieved on 2026-09-16. Links are pinned so later updates can be compared against the same inputs.

## Anthropic

- Repository: `anthropics/claude-code`
- Commit: `b782847db9a18667f00918ea341197f201b22bb4`
- [Skill source](https://github.com/anthropics/claude-code/blob/b782847db9a18667f00918ea341197f201b22bb4/plugins/frontend-design/skills/frontend-design/SKILL.md)
- [Repository license](https://github.com/anthropics/claude-code/blob/b782847db9a18667f00918ea341197f201b22bb4/LICENSE.md)

Design inputs: subject-specific direction, deliberate typography, restrained decoration and motion, useful interface copy, and visual self-review.

The upstream frontmatter refers to `LICENSE.txt`, but the pinned skill directory contains only `SKILL.md`. The repository license states that Anthropic reserves rights and use is subject to its Commercial Terms of Service. No missing license file has been reconstructed or assumed to be MIT/Apache.

## Local Adaptation

The skill is rewritten local guidance based on the Anthropic source above, not a copy of its complete prompt. Source attribution does not assign a new license to upstream material.

- Existing project decisions and explicit design requirements take priority over aesthetic defaults.
- Visual preferences are contextual choices, not universal prohibitions.
- Planning and clarification scale with the task; neither novelty reviews nor approval pauses gate every UI change.
- Checks use available tools and match the changed behavior.
- The scope, authorization, and verification safeguards also reflect this repository's maintenance conventions.

The former local `license: Complete terms in LICENSE.txt` field was removed because no such file was supplied. The source statements above preserve the known provenance without inventing replacement terms.
