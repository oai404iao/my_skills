# `gen_image`: Organize prompts around visual goals

This page is only for **generating or editing images**; for answering textual questions about images, use [Non-image-generation tasks](non-gen-image.md). First determine the purpose, aspect ratio, whether input/reference images exist, content to preserve, and acceptance method. Image models vary in adherence to text, exact positioning, identity, and local edits; actual testing matters more than adjective stacking. See [OpenAI image prompting](https://developers.openai.com/api/docs/guides/image-prompting) and [Google Gemini image generation](https://ai.google.dev/gemini-api/docs/image-generation).

## The formula is a slot checklist, not an incantation to fill completely

```text
[Subject + Action/Details] + [Setting/Environment] + [Lighting]
+ [Composition/Angle] + [Style/Medium] + [Camera/Film/Technical] + [Parameters]
```

| Slot | What it addresses | When it can be omitted |
| --- | --- | --- |
| Subject + action/details | Who or what, quantity, material, pose | The subject is usually essential; uncertain details can be left for model exploration |
| Setting/environment | Foreground/background and relationships among objects | A solid background or transparent cutout can be described briefly |
| Lighting | Shadows, mood, material appearance | Do not impose it when irrelevant to the purpose |
| Composition/angle | Subject placement, whitespace, shot scale | Can be omitted for exploratory drafts where composition is not critical |
| Style/medium | Photography, printmaking, pastel, illustration, etc. | Can be simplified when a reference image already establishes it consistently |
| Camera/film/technical language | Appearance cues such as shallow depth of field, overhead view, macro | Usually unnecessary for illustrations/diagrams; camera models and focal lengths do not promise exact simulation |
| Parameters | Dimensions, aspect ratio, quality, transparency, etc. supported by the target platform | **Do not write them as a universal prompt suffix**; prefer API/tool configuration and check model capabilities |

Start with a short "subject + purpose + composition" baseline, then add slots for what results lack; conflicting styles, irrelevant lens parameters, and long strings of "high-definition masterpiece" are not universal improvements. If the platform provides dedicated negative prompt, mask, seed, or reference-image interfaces, follow its documentation; do not assume every model supports identically named parameters or full reproducibility. Prose may also describe visible elements to exclude when necessary.

## Strategy selection and task examples

### 1. Product photography: From generic attractiveness to a specified layout

**Baseline:** "Take a nice picture of a cup."

**Improved prompt:**

```text
Generate a realistic product photo of a matte white ceramic cup for an e-commerce banner. Place the cup on the right,
leaving clean, warm-gray whitespace on the left half for text added later; use a light-gray tabletop, soft side-window light,
and a three-quarter view showing the rim and handle. Include only one cup, with no text or logos.
```

**Choice/expected effects:** Subject, material, quantity, and whitespace make fitness for purpose easier to judge than listing camera brands. Set landscape dimensions separately when supported; exact pixel layouts cannot be guaranteed. Check cup count, handle, usable whitespace, and defects; for a transparent cutout, also check for a real alpha channel rather than a drawn checkerboard.

### 2. Stylized illustration: Emphasize the medium without mechanically filling photography slots

```text
A single illustration for a children's picture book: an orange cat waits at a bus stop after rain, holding an oversized blue umbrella.
Gouache paper texture, soft blue-gray contrasted with warm orange, a clear gaze direction and umbrella outline,
simplified background streetscape, no text.
```

**Choice/expected effects:** Medium, colors, and visual emphasis help keep a series aligned; lens focal lengths are unnecessary. If a character reference image exists, specify that it supplies character appearance only, not the background. Check subject identity, umbrella count, outline, and series consistency; overly narrow color/action requirements may reduce unexpected creativity.

### 3. Posters and image text: Specify placement, but proofread independently

```text
Create a portrait poster for a community open day: write "Saturday Open Day" in large, clear text at the top,
place a simple neighborhood garden illustration in the middle, and leave whitespace at the bottom for an address added later.
Include only the quoted title and no other text.
```

**Choice/expected effects:** Quotes, text hierarchy, placement, and restrictions on extra text make requirements testable; text may still be misspelled, distorted, or omitted. For event information or logos that must be exact, prefer generating a text-free background and overlaying text in layout software; check every character rather than treating "as accurate as possible" as a guarantee.

### 4. Reference-image editing: Separate changes from preservation

```text
Input image A is the product photo to edit. Change only the background to a warm-gray seamless studio backdrop,
preserving the product's shape, label text, position, viewing angle, and existing highlights; add no accessories or watermarks.
```

**Choice/expected effects:** Assign a role to the reference image and separate "background only" from the preservation list, with the expectation of reducing subject drift. The image must actually be supplied; fine local changes can use platform-supported masks. Check label text character by character, edges, lighting, and background; if the model cannot preserve these consistently, use a layer-based/image-editing workflow instead.

### 5. Infographics/diagrams: Validate facts before visuals

```text
Draw a three-step plant-watering diagram, left to right: "Check soil," "Water appropriately,"
"Observe drainage"; one simple icon per step, arrows connecting only adjacent steps, and ample text space.
```

**Choice/expected effects:** Count, order, and connections are more verifiable than "professional infographic"; the model may still get text/arrows or facts wrong. For specialized processes, verify content first, then check icon correspondence and text item by item; use editable layout/vector tools for precise charts rather than relying solely on generation.

## Iteration and interface boundaries

Change only one or two things per round: inspect subject/composition first, then text and details; save comparable prompts, input-image roles, the actual model, and supported dimension/quality settings. Generation and editing are different invocation scenarios; "preserve the original" does not mean the model received the original. Output selection can consider composition compliance, text accuracy, edit preservation, and human acceptance rates; see [Evaluation](../engineering/evaluation.md). For which layer owns parameters, see [Platform differences](../engineering/provider-compatibility.md); the formula is this skill's organizational tool and is not claimed to originate in any official documentation.
