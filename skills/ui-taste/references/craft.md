# Craft values

Exact values for the craft floor in `SKILL.md`. Read this file before you build or review a surface. Put each value in a token or in a component in `components/ui`. The style lint blocks one-off values in pages.

The brief and the project design system win over this file.

## 1. Lines and grouping

Clean UI has few boundaries. Separate things in this order, and stop at the first step that works:

1. **Space.** Put more space between groups than inside a group. The gap between two groups is at least 2 times the largest gap inside one group.
2. **A background.** Use a surface only for a unit that the user acts on as one thing: a selectable row, a card that moves, a dialog.
3. **A line.** Use a line only for dense data: table rows, a long settings list, columns of a grid.

Then apply these rules:

- One edge per control. A bordered input in a bordered form next to a bordered button draws one control three times. Remove the outer borders.
- Remove horizontal rules first. Keep a vertical rule only where it carries a column grid.
- Never put a line between an element and its label, caption or metadata.
- Never put a line and a large gap in the same place. The gap already separates.
- A section heading uses space and weight: a larger, heavier title with clear space above it. It has no rule above it and no header bar.
- Put a set of stats or facts in one surface, split by 1px vertical hairlines. Do not put each stat in its own card.

## 2. Colour

**Lines and fills.** Make them from the text colour with alpha, so that they work on every surface.

| Token role | Light theme | Dark theme |
|---|---|---|
| Line (all borders and dividers) | text colour at 8 to 12% | white at 10 to 12% |
| Strong line (input and control edges only) | at least 3:1 against the surface | at least 3:1 against the surface |
| Hover fill | text colour at 4 to 6% | white at 4 to 6% |
| Selected or pressed fill | text colour at 8 to 10% | white at 8 to 10% |
| Zebra row fill | text colour at about 3% | white at about 3% |

- Use one line token for every border and divider. A second line colour is a bug.
- Use alpha colours, not the `opacity` property, for text and lines.
- Do not mix black alpha and white alpha on one surface.

**Text ladder.** Three steps: primary, secondary at about 64% of the text colour, tertiary at about 44%. Use the tertiary step only for metadata that a user can skip. Measure every step against its real background. Body text needs 4.5:1. Lift text that a user must read to the secondary step or higher.

**Neutrals.** Keep greys neutral. If the red, green and blue channels of a grey differ by 8 or more, correct it. A spread under 5 is fine.

**Accent and status.**

- The accent marks interactive things only: links, the primary button, focus, the selected item.
- Each status (success, warning, error) has three tokens: text, fill and line. Status colours never fill a button.
- On a Tailwind colour ramp, white text needs the 600 step or darker. White on 500 usually fails 4.5:1.
- Components use semantic tokens (`--surface`, `--line`, `--accent`). Only the theme file uses the raw ramp.

**Dark theme.** Do not invert the light theme. Lower the chroma of colours, put more distance between the dark steps, and measure every text pair again. Show elevation with lighter surfaces, not with shadows: each level is a few percent lighter than the one under it. The sidebar uses the canvas colour. Inputs are a step darker than the surface around them.

## 3. Surfaces and elevation

- Use one elevation level for content. A card has a 1px line, or a soft shadow ring. Never both on one element.
- Light shadow ring: `0 0 0 1px rgb(0 0 0 / .06), 0 1px 2px -1px rgb(0 0 0 / .06), 0 2px 4px 0 rgb(0 0 0 / .04)`.
- Dark shadow ring: `0 0 0 1px rgb(255 255 255 / .08)` and no drop shadow.
- Give a shadowed element `border: 1px solid transparent`, so that forced-colours mode still draws its edge.
- Only overlays (menus, popovers, dialogs, toasts) get a stronger shadow.
- Put a 1px outline at `-1px` offset on images, in black or white at 10%. An outline keeps the image size and radius.

## 4. Radius

- One radius token per role: controls 6 to 8px, cards 10 to 12px, dialogs 12 to 16px. Set them in the theme, so that a page cannot pick another value.
- Nested corners are concentric: outer radius = inner radius + padding. Above 24px padding, the rule stops mattering.
- Pills are for tags, filters and small status chips. Default buttons use the control radius.
- Small elements never get a large radius.

## 5. Type

- One family. Make the hierarchy with size and weight. Use a monospace face only for code.
- In product UI, keep text between 11px and about 30px. Use 3 or 4 sizes on one screen.
- Weights 400 for body, 500 for labels and controls, 600 for headings. Use weights under 400 only at 28px and up.
- Line height, unitless: display 1.1, headings 1.2 to 1.3, body 1.5 to 1.6. Text that wraps to 3 lines or more gets at least 1.4.
- Letter spacing: -0.01 to -0.02em at 24px and up. Small uppercase labels get +0.05em. Use `em`, never `px`.
- `text-wrap: balance` on headings. `text-wrap: pretty` on paragraphs. `overflow-wrap: anywhere` on IDs, URLs and long tokens.

**Numbers are data.**

- `font-variant-numeric: tabular-nums` on every number that changes or aligns: prices, counters, timers, table columns.
- Align numeric columns to the end and text columns to the start.
- Show an empty value as an en dash (U+2013), not as 0 and not as an empty cell.
- Show a currency code or unit in the secondary text step.

## 6. Spacing and layout

- Adjacent steps of the spacing scale differ by 25% or more.
- Each nesting level has about 1.4 times the space of the level inside it, snapped to the scale. Example: label to input 8px, field to field 12px, group to group 16px, content padding 24px, page padding 32px.
- Panels in an Operate surface use 12 to 16px padding.
- Align to a small set of shared edges. One indent step per nesting level, 16px by default. An icon that sits 2px off the text edge is a defect.
- Controls in a row have the same height and radius. The gap between them is smaller than the gap to the things around them.
- Grid tracks use `minmax(0, 1fr)`. Flex children that hold text or tables get `min-width: 0`.
- Use `100%`, not `100vw`. A box that holds text gets `min-height`, not `height`.
- Dialogs, drawers and menus get `overscroll-behavior: contain`.
- Set `scroll-padding-top` to the height of a sticky header.
- A component that must fit different containers uses container queries.

## 7. Tables, forms and actions

**Tables.** Wrap a wide table in a container with `overflow-x: auto`. Pin the head with `position: sticky`. Use a line between rows only when the table is dense. Otherwise use space or a zebra fill.

**Forms.**

- The gap from label to field is smaller than the gap from field to field.
- An error sits directly under its field. The field gets `aria-invalid` and `aria-describedby`. On submit, move focus to the first invalid field.
- Keep the submit button enabled, and validate on submit.
- A pending submit shows a spinner next to the label and sets `aria-disabled`.
- Set `autocomplete` and `inputmode` on each field. Never block paste.
- A full-width button on a phone stays inside the page margins.

**Actions.** One filled primary action per view. One or two secondary actions. Put the rest in a menu.

## 8. States

- A loading skeleton has the layout of the real page: the same heading, the same columns, the same row height.
- An empty state is one area with a short heading, one sentence and one action. Give it `role="status"`.
- Show missing, loading and failed as three different states.

## 9. Focus, targets and icons

- Focus: `:focus-visible` with a 2px outline at `outline-offset: 2px`, at 3:1 against every colour it crosses.
- Make a hit area larger with a pseudo-element, not by making the visible element larger. Decorative layers get `pointer-events: none`.
- Icons use `currentColor`, come from one library and have one stroke width. Use the outline style by default and the filled style for the active item.

## 10. Motion

- Animate `transform` and `opacity` only. For a change of size or position, use a layout animation
  and do not animate `width` or `height`.
- Keep interface transitions between 150 and 300 ms. Make an exit shorter than an entrance.
- For product UI, use springs with little or no bounce.
- Respect `prefers-reduced-motion`. With Motion, wrap the app in
  `<MotionConfig reducedMotion="user">`.
- Give an exit animation to anything that gets an entrance animation. Keep keys stable.
- Reveal on scroll one time only. Keep a stagger under 400 ms in total. Do not stagger a long list.
- Do not animate frequent actions, keyboard-driven actions, data tables or anything that delays
  input.
- Use plain CSS transitions for hover and simple state. Use Motion for layout, exit, gesture and
  shared-element transitions.
- Name the properties in a transition. Never use `transition: all`.
- Use a CSS transition for state that toggles, so that it reverses mid-way. Use keyframes only for a one-time sequence. Turn transitions off while the theme changes.
- Hover feedback takes 100 to 150ms.
- Press feedback: `scale: 0.96` over 150ms with ease-out, on enabled controls only.
- In Motion, set `initial={false}` on `AnimatePresence` for a swap of state. Do not set it on an entrance.
- Add `will-change` only after you see stutter, and never `will-change: all`.

## 11. Before you finish

Search the changed files for each pattern. Fix each hit, or write the reason it is correct.

| Search for | Problem | Fix |
|---|---|---|
| `transition-all`, `transition: all` | Animates every property | Name the properties |
| `rounded-full` on a button | Pill as a default button | The control radius token |
| `border` and `shadow` on one element | Two edges | Keep one |
| `CardHeader` with `border-b`, or a header bar per section | Boxed section heading | Space and a heavier title |
| A row of `Card` components that each hold one number | Stat tiles | One surface split by hairlines |
| `divide-y` or `border-b` between a label and its value | Line next to its own label | Remove the line |
| `font-mono` outside code | Monospace as decoration | `tabular-nums` in the body family |
| `font-bold`, `font-extrabold`, `font-black` | Weight above 600 | 600 |
| `opacity-` on text | Opacity instead of a colour | A text ladder token |
| `100vw` | Horizontal scroll | `100%` |
| `h-` on a box that holds text | Text clips | `min-h-` |
| `disabled={!` on a submit button | Blocked submit | Validate on submit |
| `onPaste` with `preventDefault` | Blocked paste | Remove it |
| `outline-none` without a `focus-visible` style | No focus ring | Add the focus token |
