---
name: frontend-design
description: Design and implement web interfaces with subject-specific visual direction and usable interactions. Use for new pages, applications, or explicit UI redesigns; preserve existing design systems and keep small UI fixes scoped.
---

# Frontend Design

Deliver a working interface suited to its audience and task. Visual distinction should make the product clearer, not compete with using it.

## Establish Scope

- Follow the requested deliverable: design advice does not authorize code changes.
- Inspect the existing framework, components, tokens, assets, and relevant screens before changing UI. Reuse the project's component APIs and conventions.
- Preserve established branding and interaction patterns unless a redesign is requested. A local fix does not authorize a new visual system.
- Infer routine details from context. Ask only when missing information materially changes the product, audience, scope, or implementation; otherwise proceed with a reasonable assumption.

## Choose a Direction

For a new page or substantial redesign, briefly identify:

- The subject, intended audience, and primary user action.
- A visual idea grounded in that subject rather than a reusable aesthetic preset.
- A compact set of color roles, type roles, spacing, and layout decisions. Reuse existing tokens; define new values only where needed.

Use a small sketch when it helps resolve layout choices. Reconsider choices that could fit any unrelated product, then build. Small fixes do not need a design proposal or approval cycle.

Give a distinctive design one focal point and let supporting elements stay restrained. Familiar fonts, flat backgrounds, cards, or gradients remain valid when the brief calls for them; none is automatically a sign of poor design.

## Express the Subject

- Let the subject and audience guide the visual language. A playful product and an analytical workspace should not inherit the same treatment by default.
- Where an opening hero is appropriate, choose the form that best introduces the subject: typography, imagery, a demonstration, or an interaction. Follow the brief rather than prescribing one layout for every page.
- Use real content where available. Draft missing copy to support the user's task, not to fill a generic template.

## Typography, Copy, and Motion

- Establish a readable type hierarchy with deliberate measure, spacing, and contrast. Use display-scale text where space and purpose justify it.
- Labels, borders, and numbering should explain structure. Number items when their order matters, not as decoration.
- Write concrete action labels and consistent terminology. Errors should explain recovery; empty states should offer a next step.
- Keep necessary instructions and accessibility text. Remove filler and descriptions of the design itself.
- Animate state changes to clarify feedback. Use ambient animation sparingly, respect reduced-motion preferences, and retain usability without motion.

## Implement and Check

- Implement the requested interactions and relevant loading, empty, error, and success states; do not invent unrelated features to make the app feel complete.
- Check responsive layouts and text readability on both large and small screens.
- Use semantic elements, keyboard access, visible focus, and accessible contrast.
- Keep CSS scoped and predictable; avoid competing selectors and unnecessary overrides.
- Choose assets and implementation tools that serve the brief and are available in the environment.
- When rendering tools are available, inspect representative desktop and narrow-screen views and exercise the changed interactions.
- Run the checks appropriate to the change and project. Fix concrete defects; do not repeat visual redesign or testing without a new reason.
- Report what changed, what was actually verified, and any remaining limitations. Do not claim screenshot or interaction verification unless performed.

## Provenance

This is locally maintained guidance informed by Anthropic's frontend-design skill, with task-scope and verification safeguards from this repository. It is not a verbatim upstream replacement.

Read [source notes](references/sources.md) when checking provenance, licensing metadata, or updating these rules; ordinary UI tasks do not need to load them.
