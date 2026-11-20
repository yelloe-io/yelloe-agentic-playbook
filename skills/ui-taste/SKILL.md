---
name: ui-taste
description: Design, build and review frontend UI so that it does not look machine-made. Use when the work creates or restyles a page, a component, a dashboard or a landing page, when the user asks to rework, restyle or review UI, or when a plan includes a new UI surface. Do not use for work that has no UI.
---

# UI Taste

Generic UI comes from defaults. A model that gets no direction produces the average of everything it
has seen. This skill makes you choose a direction before you write code, and then check the result
against that direction.

**The brief always wins.** If the user, the spec or the project gives a design system, brand rules
or an explicit instruction, follow it. Everything below applies only where the brief is silent.

## 1. Read the surface

**Find the stack.** Use the first of these that applies:

1. The repo already has a stack and a design system. Use them and extend what is there. Do not
   bring in a second visual language.
2. The user or the spec names a stack. Use that stack.
3. There is no stack and none is named. Use React, Tailwind and shadcn. With no repo, run
   one up first.

**Say what it is.** One line: what the surface does and who uses it. If a plan or spec already
says this, take it from there.

**Check the base.** The base is a `docs/design.md`, the tokens in one place and a `components/ui`
folder. A base is good when new work can copy it and look right. Name 1 or 2 real pages that new
work copies, for example "copy the Orders page".

**Propose the level** in one line, and let the user confirm or change it: "Level: Shape, because
this is a new screen. OK?" With no user in the session, take the level from the spec.

| Level | When | What happens |
|---|---|---|
| **Match** | A change inside a good base: a filter, a field, a dialog | Copy the named page. No variants. One screenshot check |
| **Shape** | A new screen, flow, page or site, or a redesign | Variants in the app, then the user picks |

**Variants.** If you have a `prototype` skill, use it to build them. Otherwise build each variant
as its own route, or behind a switch on one route, in the running app, so the user compares them
in the real product.

**Pick the mode** of the surface. It sets how far the look may go.

| Mode | The visitor wants to | What matters most |
|---|---|---|
| **Operate** | Do a task again and again: a dashboard, an admin tool, a form | Density, speed, scan paths, keyboard use. Very little motion |
| **Read** | Take in content: docs, an article, a report | Measure, type scale, rhythm, contrast |
| **Persuade** | Decide: a landing page, a pricing page | One clear message, real proof, one action |
| **Experience** | Feel something: a portfolio, a showcase | One bold idea, carried through everything |

Most product work is Operate. Persuade and Experience surfaces get the hero first, then one section
at a time, and a motion pass (section 5).

**In a build session from an issue,** the spec names the approved prototype as the design target:
its branch, route and screenshot. Build to it. Do not stop for taste.

## 2. Foundation

Run Foundation when the base is missing or weak, on the first UI task of a project or on any task
that finds the base weak. A project with very little UI skips the component library. With no user in
the session, do not run Foundation: report the weak base as an open decision.

1. **Find the references.** Take the sites or screens that the user names. With none, pick 3
   entries from the project taste library in `docs/taste/` that fit the product and its mode. With
   no library or no fit, write 3 directions from the point of view below. For each new reference
   site, follow [teardown](references/teardown.md) and add the result to `docs/taste/`. The
   [taste example](references/taste-example.md) shows what an entry looks like.
2. **Write the point of view** in `docs/design.md`, under 12 lines. When `docs/design.md` exists
   but lacks some of these fields (for example it holds only users, what they care about, what the
   product wants to be and references), fill in the missing fields with the user before you design:

   ```
   # Design

   Users         Who uses it, where and on what device
   They care     What matters most to them
   We are        What the product wants to be to them
   Principles    2 or 3 rules that follow from that
   References    The 1 to 3 sites or taste library entries
   Care details  1 or 2 details that show the product knows their situation
   Our moves     The patterns from section 3 that this look uses on purpose
   ```

   A care detail is specific to these users, for example the order number in the tab title. Test it:
   "Would I add this to any app?" If yes, choose again.
3. **Show 3 looks** as variants (section 1), each built from one reference. Each look has a palette of 4 to
   6 named tokens with one accent, one type family with its roles, the layout, and one bold move.
   Test each look: "Would I produce this for any similar prompt?" If yes, change the generic part.
4. **The user picks.** Write the pick into `docs/design.md`, the tokens and `components/ui`: the 5
   to 8 components that the app uses most, from section 7. In an existing app, take them from its
   best page. Old pages move to the base only when a task touches them.

The user approves each change to `docs/design.md`.

## 3. The default-no list

These patterns mark a page as machine-made. Avoid them by default. A pattern that `docs/design.md`
names under "Our moves" is part of the look: use it, and do not report it.

You can use one when it is truly right for the content. State the reason to the user, for example
"three equal cards, because the content is three pricing tiers". With the user in the session, wait
for approval. In a build session with no user, do not take the exception. Build the default, and
name the exception that you wanted in your report. An exception that the spec already approved is
fine.

**Layout**
- A centered hero, then three equal feature cards, then a call-to-action band.
- Cards inside cards. A card around everything. Use a card only when the content is a separate
  object that a user can act on.
- A colored left border on a card as decoration.
- Numbered section markers (01, 02, 03) where the content is not a sequence.
- A small uppercase label above a heading.
- A border, a rule or a header bar around each section. Separate sections with space and a
  heavier title.
- A row of cards that each hold one number. Put the numbers in one surface, split by hairlines.
- A pill-shaped default button. Keep pills for tags and filters.

**Color**
- A purple-to-blue gradient. Gradient text. A gradient behind every section.
- Cream background, serif display and a terracotta accent as the "tasteful" default.
- Gray text on a colored surface. Tint the secondary text from the surface hue.
- More than one accent color. An accent on one word of a headline.

**Type**
- The reflex font of the year as the display face. If the family is the first one you thought of,
  choose again, or use a system stack with intent.
- Monospace as a costume for "technical". Use it for code only. Numbers align with `tabular-nums`.
- Body lines longer than 75 characters or shorter than 45.

**Decoration and motion**
- Emoji as icons. Glow, particles and beams as background decoration. Glass blur on a card or a
  section background.
- A shadow on everything. Use shadow only where elevation carries meaning.
- A fade-and-slide-up entrance on every section. A hover effect on every card.

**Content**
- Filler verbs: elevate, seamless, unleash, supercharge, empower, revolutionize.
- Placeholder people and perfect numbers: "Jane Doe", "Acme", 99.99%, 10,000+ users. Use plausible,
  uneven data: 8,412 and not 10,000.
- A fake screenshot built from gray boxes. Use the real UI or leave it out.
- Em dashes.

## 4. The craft floor

Check these before you call the work done. These are not defaults. They always apply. The exact
values and a search table are in [craft values](references/craft.md). Read it before you build or
review a surface.

- **Lines:** separate with space first, then a background, then a line. Use lines only for dense
  data. Give each control one edge. Use one line token for every border and divider.
- **Surfaces:** one elevation level. A card has a line or a shadow ring, never both.
- **Radius:** one token per role (control, card, dialog). Nested corners are concentric.

- **Tokens:** keep every color, the spacing scale and the type scale in tokens (CSS variables or the
  token system of the stack). Do not write a raw hex value in a component.
- **Theme:** choose light or dark from the place where the product is used. If that does not decide
  it, choose dark. Build both only if the project supports both or the spec asks for it. Tokens make
  the second theme cheap to add later.
- **Measure:** body text 45 to 75 characters per line.
- **Scale:** a type scale with a clear ratio. Display text at most 6rem. Letter-spacing on large
  display text at most -0.04em. In product UI, keep text between 11px and about 30px, use 3 or 4
  sizes on one screen and weights 400, 500 and 600.
- **Numbers:** `tabular-nums` on numbers that change or align. Align numeric columns to the end.
  Show an empty value as a dash.
- **Spacing:** one spacing scale, used everywhere. Group related items with less space and
  separate groups with more. Do not give every gap the same value.
- **Contrast:** body text at least 4.5:1. Large text and interface marks at least 3:1.
- **Targets:** interactive targets at least 24px, and 44px on touch surfaces.
- **States:** every interactive element has hover, focus-visible, active and disabled states. Every
  view that loads data has loading, empty and error states.
- **Browser surfaces:** set the focus ring, the text selection, the caret and the scrollbar from the
  palette. These details show that someone made decisions.
- **Phones:** use `dvh` or `svh`, not `100vh`. Inputs use at least 16px text, so focus does not zoom
  the page. Put hover styles behind `@media (hover: hover)`. Respect the safe areas with `env(safe-area-inset-*)`.

## 5. Motion

Motion explains a change. If it explains nothing, remove it.

Read the motion rules in [craft values](references/craft.md) section 10 before you add motion.

**The motion set.** Scroll motion comes from a few shared components in `components/ui`, for example
`Reveal`, `Stagger`, `StickyStack` and `Marquee`, built on Motion. Their duration, distance and
easing are tokens, so every page moves the same way. A page uses the set. It does not animate by
itself.

**Persuade and Experience surfaces** get one motion pass after the layout is approved:

- One reveal for the whole site: a rise of 16 to 24px over 0.5 to 0.8s with a custom easing, once.
  Use it on the content that needs an entrance, not on every section.
- One signature moment, for example a sticky hero that the content scrolls over, or a scroll-linked
  hero exit with CSS `animation-timeline: view()`.
- Smooth page scroll with Lenis only when the user approves it. Drive Lenis from the GSAP ticker or
  from Motion's frame loop, so that scroll triggers stay in sync. Turn it off for reduced motion.
  Operate surfaces never get it.
- Glass (a translucent fill with `backdrop-filter: blur()`) only on a layer that floats over content:
  the nav, a toolbar, a popover. Only when `docs/design.md` names it.

## 6. Interface copy

- A button says what happens: "Save changes", not "Submit". "Delete project", not "OK".
- An error says what happened and what to do next. It does not apologize, and it does not blame.
- An empty state says what will appear here and gives the first action.
- Use sentence case. Use one name for one thing on every screen.
- Write numbers and dates the way the user's locale writes them.

## 7. Components and libraries

**The components folder.** All UI comes from one `components/ui` folder. Its base is shadcn, set to
the project tokens. A project with its own design system keeps it (section 1).

- Pages only combine components from `components/ui`. They add layout, and nothing visual.
- A new visual pattern becomes a component in `components/ui` first. Then the page uses it.
- Outside `components/ui`, the [style lint](references/style-lint.md) blocks raw colors and one-off
  style values. Fix a lint error with a token or a component. Do not suppress it.

**Libraries.**

- Never leave a library component in its default state. Set its radius, spacing, type and color
  from the direction. This applies to shadcn most of all.
- Every component comes in through the `shadcn` CLI, or the shadcn MCP server when the project
  has it: from shadcn or from a registry such as Magic UI or 21st.dev. It lands in `components/ui`.
  Restyle it to the tokens before a page uses it. Pages never import from a collection.
- For charts in a shadcn and Tailwind 4 project, Bklit UI (`@bklit/*`) is a good start. Add the
  accessible labels and a table fallback yourself.
- Decorative components (beams, particle buttons) are for one deliberate moment on a Persuade or
  Experience surface. They count as an exception under section 3, unless "Our moves" names them.

## 8. Verify

If your environment can take a screenshot, take one at a desktop width and one at a phone width, and
look at them. If it cannot, read the rendered markup and the styles.

Check, in this order:

1. Does the result match the approved prototype, or the named page for Match work? Put the two
   screenshots side by side. Does it match the point of view in `docs/design.md`?
2. Is anything from the default-no list present without an approved reason?
3. Does the craft floor hold? Run the search table in [craft values](references/craft.md).
4. Does each new visual pattern live in `components/ui`, and does the style lint pass?
5. Squint test: is the most important thing the most visible thing?

Fix what you find, then check again. Stop after two rounds and report what is left. Say what the
direction was, where the bold move is, what you chose not to do, and each exception that you wanted
and did not take.

## Design edit

Built is not the same as good. After the pull request is merged, the user can walk the flows for
design tweaks. This step is optional, and the user starts it, for example with "design edit".

1. Start the app and give the user the address and a test login. If the project has a skill or a
   script that starts the app, use it.
2. The user walks the main flows as a user and gives a list of tweaks.
3. Make the tweaks in one round on a new branch, check them as in section 8, and open one pull
   request.
4. When a tweak changes the point of view, propose the change to `docs/design.md`.

## Review mode

When the user asks you to review existing UI, do not redesign it. Report against sections 3 to 7 and [craft values](references/craft.md). Give each finding a location, the pattern, and a specific fix. Order the findings by how much
each one makes the page look generic.
