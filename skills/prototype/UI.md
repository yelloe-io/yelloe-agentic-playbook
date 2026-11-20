# UI Prototype

Build **several different versions** of a screen in the real app. The user flicks through them with the arrow keys, picks one or steals bits from each, and says why. The pick becomes the design target of the spec.

If the question is about logic or state, not about what something looks like, use [LOGIC.md](LOGIC.md).

## 1. Load the ground

1. Read `docs/design.md` if the project has one, and the design tokens (colours, type scale, spacing). They set the look. If you have a design skill, use it to read the look of the app.
2. Pick the page to copy: the existing page closest to the new screen. Read its layout, its shared components, its density and its words. Every version uses these components and tokens, so it looks like the app on the first look.
3. With no app yet, set up the project first. The prototype routes are its first code.

## 2. Pick the place

- **Sub-shape A, the default.** The page exists, or the new part lives inside a page that exists. Render the versions on that route, gated by a `?variant=` search param. Keep the data loading of the page. Only the rendering changes.
- **Sub-shape B.** The thing is a new top-level page or site with no home. Make a throwaway route that has `prototype` in its path, in the routing convention of the project.

A version is much easier to judge next to the rest of the app: real header, real sidebar, real data, real density. On an empty route every version looks fine. Before you pick sub-shape B, check that no existing page could host the versions.

Where the real data does not exist yet, read it from a fixture file next to the prototype, with plausible, uneven values: 8,412, not 10,000. Never wire a version to a real write. A button that would save does nothing, or writes to a stub.

## 3. Build the versions

Build 3 to 6 versions. Each round changes **one axis** on purpose, and each version takes a different position on it. The idea comes from `variant` by Jakub Krehel (github.com/jakubkrehel/skills).

| Axis | What changes |
|---|---|
| Structure | Grouping, order, column count, what collapses |
| Density | The spacing step and how much fits. Lean means fewer elements at the normal density of the app, not smaller rows |
| Emphasis | Where the filled colour goes, what recedes |
| Type | Scale steps, weight contrast, measure |
| Voice | Labels, tone, how much copy |

The size of a round follows the change:

- **A small change inside a page that already has its look:** no versions. When the user asks for options on one element, build 3 versions of that element.
- **A screen people work in or read** (a dashboard, a form, a list): whole screens.
- **A page that has to persuade or impress** (a landing page, a launch page): the hero first. Then one section at a time.

Give each version a short name that says its position, for example `B · Dense table`. Mark your pick on one version, with one line on why.

When the question is about the states of one component, add a **States** switch to the bar: normal, empty, loading, error, lots of data, long text. The idea comes from `state-machine` by Jakub Krehel.

## 4. The flick bar

A small fixed bar at the bottom centre of the screen:

- **← and →** cycle through the versions and wrap around. The arrow keys do the same, except when an input, a textarea or a `[contenteditable]` has focus.
- **The label** shows the key and the name: `B · Dense table`.
- **Pick this**, a note field for each version, and **Copy answers**. Copy answers copies the pick and every note as Markdown. Keep the picks and notes in `localStorage` under the name of the prototype.
- The bar updates the URL with the router of the framework, so a version is shareable and survives a reload.
- The bar looks different from the page, so nobody mistakes it for the design. Hide it in production builds, so a stray merge cannot ship it to users.

Put the bar in one shared component, where the shared UI of the project lives.

## 5. Check it yourself

Before the user sees a round, open each version yourself:

1. Click the main path of each version with the mouse, at 1440px and 390px.
2. Confirm that the switch shows each version, that the real fonts load, and that text is legible at real size.
3. Look at each screenshot. Compare it with the page to copy. Fix what is off.

A round is ready when every version passes all three checks. If you have no browser tool, tell the user that you could not check the round, and what they should look at first.

## 6. Hand over

Start the hand-over with:

1. The address of each version and the test login.
2. **Look at these:** the 2 or 3 things to judge in this round.
3. A click path: "Try: Plan → Annual → Save".
4. What is already decided and what is out of scope.

## 7. The next round

The user ends the rounds. Never propose to stop.

- Take the pasted picks and notes. Build the next round on the same route.
- After 3 rounds of small changes to one element, show 3 versions of that element in place of a fourth change.
- When a round makes the result worse, go back to the last version the user liked and say so.

## 8. Capture the pick

When the user approves a version:

1. Take a screenshot of it at 1440px and 390px.
2. Commit the prototype to a throwaway branch.
3. Write the design target for the spec: the branch, the route with its `?variant=` key, and the screenshot paths. The spec's Design Target section takes it.

The build rewrites the winner properly. The versions and the bar stay on the throwaway branch, not on the main branch.

## Anti-patterns

- **Versions that differ only in colour or copy,** unless the axis of the round is emphasis or voice.
- **A shared layout component between versions.** Each version is free to change the layout.
- **A look that the app does not have.** A version that the user cannot imagine in the real app tells them nothing.
- **Promoting a version straight to production.** It was written under prototype rules (no tests, little error handling). Rewrite it properly when you fold it in.
