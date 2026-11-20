---
name: verify
description: Prove a change works in the running app with evidence, probe what it could break, and fix what fails. Use after implementing a change, before a PR, or when asked to verify, test, or check a change.
---

# Verify

Run everything in the repo the change lives in, and follow that repo's `CLAUDE.md` or `AGENTS.md`.

Prove the change works by running it, not by reading it. Every claim ends **PASS** with evidence seen in this run, **FAIL** with an observed contradiction, or **BLOCKED** when it was not run or could not be observed. A result you can only phrase with "should" or "seems" is BLOCKED.

Arguments: `--no-fix` reports without fixing. `--headed` shows the browser.

Keep screenshots, saved sessions and other scratch files in a folder in the OS temp directory, never in the repo.

## 1. Charter

Collect the claims. When the branch name or the session names an issue, read that issue and use its acceptance criteria as the claims, worded as written. Otherwise derive the claims from the diff against the merge base with the repo's default branch, including uncommitted and new files, and from the intent agreed in this session.

Map the changed files to the user flows they feed: that is the **blast radius**. When shared code changed (helpers, state, middleware, shared components, handlers with other callers), add one neighbouring flow that also uses it.

Read [probes](references/probes.md) and pick 2 to 4 axes that this diff could plausibly break. Plan one probe per axis. If the repo keeps a checklist of past traps, read it and add the items whose trigger matches the diff.

Post the charter as one short message (claims, flows, probes), then continue without waiting.

## 2. Run the app

Find how the project starts, in this order: the repo's `CLAUDE.md` or `AGENTS.md`, the README, then the scripts in the package manifest, `Makefile` or `docker-compose` file. If you have a skill that launches the app (such as `run`), use it. When none of these says how, ask the user once.

When backend code changed, restart a backend process that is older than the newest changed file. Use safe test data, and keep a list of everything you create.

For a change with no UI (a CLI, a library, an API), run the real entry point with real inputs and capture its output. The browser parts of step 3 do not apply.

## 3. Check

Run each claim and probe as: precondition, action through real controls, expected result.

Drive the browser with `playwright-cli` when it is installed, headless unless `--headed`. Sign in once, `state-save` the session to a file in the scratch folder, and `state-load` it on later runs. With another browser tool (a Playwright MCP server, a browser extension), do the same steps with its equivalents. With no browser tool at all, check what you can through HTTP requests and the API, mark each claim that needs a screen BLOCKED, and say in the report that installing `playwright-cli` (`npm install -g @playwright/cli`) would cover them.

A direct URL visit does not prove that a link works, and an API success does not prove that a form submits.

- Assert on snapshot text and elements. Take a screenshot for each visual claim and for each flow's end state, save it in the scratch folder, and look at every screenshot you take. Shoot visual claims at three sizes: the component's real container width, 1280×720, and 200% zoom. For a layout break, read [layout breaks](references/layout-breaks.md).
- After each flow, read the console errors and the network requests (`playwright-cli console error` and `playwright-cli requests`). New errors, 4xx or 5xx on touched endpoints, and requests still pending are FAIL unless the claim expects them.
- After a mutation, confirm the stored value with an API read or a database query, then reload once and confirm that the reloaded screen matches the live one.

## 4. Fix

Skip with `--no-fix`. Fix bugs inside the code this change touched, and every other instance of the same bug class. Report the fixes that fall outside the change or need a product decision.

After each fix, restart as in step 2, then rerun the failed check and the happy path. Stop after 3 fix rounds and report what still fails.

## 5. Clean up and report

Remove the data you created through normal app actions or the API. Close the browser and stop what you started. Leave staging and commits to the user.

Report in chat, short and plain:

- **Verdict**: FAIL if any check failed, else BLOCKED if any check is blocked, else PASS.
- One line per claim and probe: status, what you observed, and the evidence path.
- Fragile spots: fine now, one realistic step from breaking.
- Fixes made, described by behavior.
- What was not covered, and why.
- State left behind.
