# Frontend Design Sources and Import Notes

## Current Upstream: Ikaleio / ikadesign3

Retrieved on 2026-10-10.

- Repository: `Ikaleio/skills`
- Commit: `5276d6ee1cf0f50cf913e1c8f09dfc7471341c61`
- [Skill entry](https://github.com/Ikaleio/skills/blob/5276d6ee1cf0f50cf913e1c8f09dfc7471341c61/ikadesign3/SKILL.md)
- [design.md contract](https://github.com/Ikaleio/skills/blob/5276d6ee1cf0f50cf913e1c8f09dfc7471341c61/ikadesign3/references/design-contract.md)
- [Build workflow](https://github.com/Ikaleio/skills/blob/5276d6ee1cf0f50cf913e1c8f09dfc7471341c61/ikadesign3/references/build-workflow.md)
- [Review and rule update](https://github.com/Ikaleio/skills/blob/5276d6ee1cf0f50cf913e1c8f09dfc7471341c61/ikadesign3/references/review-loop.md)
- [Repository notice](https://github.com/Ikaleio/skills/blob/5276d6ee1cf0f50cf913e1c8f09dfc7471341c61/README.md#许可)

The entry and all three references were imported in full at the user's request. This is a direct import, not an independently rewritten version of the upstream workflow.

The pinned repository has no license file. Its README says that some skills include or adapt third-party material and that the repository grants no unified license for all content. The pinned `ikadesign3` files do not state a separate reuse grant. Public access and attribution do not establish permission to redistribute. No MIT, Apache, or other license is inferred or added. Clarify the applicable rights before publishing or redistributing this import; this local change does not claim that those rights have been obtained.

### Local Changes to the Import

- Rename the frontmatter `name` and the Build workflow's skill reference from `ikadesign3` to `frontend-design`.
- Add the import notice and this source reference.
- Add the user's reader-facing copy constraint to the design.md contract, with Build and review references: use statistical-scope explanations, footnotes, and bottom-of-page explanations sparingly; remove redundant notes while retaining necessary context and required disclosures. This is a local addition, not an upstream rule.
- Add local default stack and implementation guidance in the Build workflow (centralized CSS-variable themes instead of per-component hardcoded values, component-local vs. Zustand shared state, and wrapping recurring `react-resizable-panels` and `dnd-kit` combinations in minimal project-owned layout components). This is a local addition, not an upstream rule.
- Preserve the upstream design.md prerequisite, required chapters, rule tags, measurement tables, implementation bindings, review record, mechanical checks, issue classes, and single-recheck stop rule.

### Known Upstream Rule Conflict

The imported [review procedure](review-loop.md) contains a conflict:

- **Stop Rule** permits fixes only for `[MUST]`/universal-invariant violations and main-reader-task blockers. Other findings must be recorded without fixing them.
- **Mechanical Checks → Result Levels** says to fix an unintentional `[SHOULD]` deviation, without the same restriction.

Both statements are retained to preserve the requested import. No local precedence rule has been invented. If a task reaches this conflict, report it rather than claiming that the two instructions agree.

The one-recheck limit and the listed universal invariants are also retained as upstream workflow requirements. Their presence is not a claim that they are universal web standards or that one successful review proves stable generation.

## Upstream Method Sources

Ikaleio credits the layered method of design judgment, implementation primitives, and feedback to:

- [Vercel: How our agents build on-brand pages with design.md](https://vercel.com/blog/how-our-agents-build-on-brand-pages-with-design-md)
- [Vercel design.md](https://vercel.com/design.md)

These are the upstream method references, not a license grant for Ikaleio's text. Keep the distinction between the method and Vercel's own brand rules.

## Previous Local Version: Anthropic-Informed Guidance

The replaced local entry was rewritten guidance informed by Anthropic's frontend-design skill, not a verbatim copy. Its source was recorded on 2026-09-16:

- Repository: `anthropics/claude-code`
- Commit: `b782847db9a18667f00918ea341197f201b22bb4`
- [Previous skill source](https://github.com/anthropics/claude-code/blob/b782847db9a18667f00918ea341197f201b22bb4/plugins/frontend-design/skills/frontend-design/SKILL.md)
- [Repository license](https://github.com/anthropics/claude-code/blob/b782847db9a18667f00918ea341197f201b22bb4/LICENSE.md)

That upstream frontmatter referred to `LICENSE.txt`, but the pinned skill directory contained only `SKILL.md`. The repository license reserved rights and referred to Anthropic's Commercial Terms of Service. The former local `license: Complete terms in LICENSE.txt` field was removed because no such file was supplied.

These notes preserve the previous provenance. They do not apply Anthropic's terms to the Ikaleio import or assign new terms to either source.
