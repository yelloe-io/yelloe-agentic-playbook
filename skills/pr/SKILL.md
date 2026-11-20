---
name: pr
description: Open a pull request from the current branch into the repo's default branch, with a short, picture-first body that shows the change, proves it and calls its merge risk, then watch its CI checks. Use when asked to open or update a PR, or to land a finished branch.
---

# Open a pull request

A reviewer should get the change, believe it, and know what a merge risks, without checking out the branch. The PR is also where CI runs the lint, type check, tests and build of what the change touches.

Follow the repo's `CLAUDE.md` or `AGENTS.md` conventions for titles, issue links and footers. If the repo has a pull request template, fill it in, and use the steps below for what goes in each part.

## 1. Ready

The task's checks have passed and the work is committed. Read the issue number off the branch name or the session, if there is one. Find the base, the repo's default branch:

```bash
gh repo view --json defaultBranchRef -q .defaultBranchRef.name
```

Confirm the branch contains it: `git fetch origin <base> && git merge-base --is-ancestor origin/<base> HEAD`. If it does not, bring the base in the way the repo's conventions say (rebase or merge) and rerun the checks. Done when the issue, the base and the list of commits are known.

## 2. Review

A branch gets one full review before it opens. Skip this step when the head commit was already reviewed in this session, or when a review covered an earlier commit and you checked the commits since as the "after fixes" paragraph below describes.

Review the branch once against its base, findings in chat only. If you have a code review skill or tool, use it. Otherwise read the whole diff yourself against the issue, looking for bugs and for what the issue asked that the diff does not do. Pick the depth from the change, counting changed lines outside tests:

- Deep: permissions or sign-in, a migration, data saved in a new shape, a changed API, money or totals, shared code with many callers, or more than about 400 lines.
- Light: under about 50 lines, revertable, and none of the kinds above.
- Normal: everything else.

When the change touches permissions, sign-in or sessions, tokens, a connection to an outside system, share links, a new route, or a file upload or download, also review it once for security, with a security review skill or tool if you have one.

Sort the findings before you act on them:

- A bug the branch introduced or made worse, or a reason the issue is not resolved: fix it on the branch, rerun the checks that cover the fix, and commit; or answer it with a reason.
- A cleanup idea, a nit or a style point: do not fix it. List it once for the user.
- A problem that was already in the code before the branch: do not fix it. Give it to the user as a side note.

After fixes, do not run the review again. Confirm each fixed finding is closed, and read `git diff <reviewed commit>..HEAD` for problems the fixes introduced. If that still turns up bugs after three rounds of fixing, stop and tell the user what keeps failing.

## 3. Evidence

Every PR opens on a picture: a screenshot, a table or a small diagram. Test output is proof, not a picture; it goes in the fold. Each claim the body makes gets its proof:

- A visible change: a before and after screenshot of the same spot, cropped tight to the part of the screen that changes. If you have the `before-after` skill, use it. Otherwise take both shots yourself, the before one with the fix undone in the working tree, and look at each.
- A logic change: the test that goes red on the old code and green on the fix, with the two outputs. The picture is a table with one row per case: `Situation | Before | After`, in the product's terms.
- A change to figures or totals: a small table of the figures before and after on test data, next to the figure an independent source gives.
- Logic over several steps or requests: also a Mermaid `sequenceDiagram` or `flowchart` of the new flow, from what the code and a run show.
- A changed API reply, a migration, or data saved in a new shape: a `diff` code block with a real sample before and after.
- A change with no screen and no clear cases (a refactor, a new module): the smallest view that makes the point. A `diff` of pseudocode for changed control flow, a call tree for changed runtime flow, a component tree for UI structure, or a shallow file tree for moved responsibilities. Keep only the calls, files and states the point needs.
- Neither fits (a rename, a dependency bump): one line on why the diff is the proof.

## 4. Body

Write it to `pr-<issue>.md` in a scratch folder in the OS temp directory, next to the evidence files. No section headings, no paragraph longer than one sentence above the fold. Plain English, in the terms of the repo's glossary if it has one. In this order:

1. **Tag line**: the areas as code spans, then the risk word and the size, such as `` `billing` · revertable · 30 lines ``. Use `one-way door` instead of `revertable` for a migration, data written in a new shape, a changed API, or anything else a revert cannot undo.
2. **One sentence**: what was wrong or missing, and what it does now.
3. **The picture**, with one line that sets the scene.
4. **A closed fold**, `<details><summary>Where and why</summary>`: every screen or caller the change reaches, the cause in one or two sentences, `**Risk:**` in one line, then the red and green test outputs in a code block.

The last line links the issue, such as `Closes #<issue>`, in the form the repo uses. Add no footer after it unless the repo's conventions ask for one. The title follows the repo's commit subject format.

## 5. Open

Push the branch under its own name and open the PR from the scratch folder so the `./` references resolve:

```bash
git push -u origin <branch>
gh pr create --base <base> --head <branch> --title "<title>" --body-file pr-<issue>.md --assignee @me --attach ./<file>.png
```

`--attach` uploads the images and rewrites `./<file>.png` references in the body. It needs a recent `gh`. Without it, open the PR, then drag the images into the body in the browser.

Done when `gh` prints the PR's address.

## 6. Checks

Watch them with `gh pr checks <pr> --watch`. For a failure, read `gh run view <run> --log-failed`, reproduce it locally, fix it on the branch, commit and push. Done when every check is green, or the user has the failing output.

Report the PR's address and the check results. Merging is the user's call.

## Updating a PR

New commits get the review in step 2 first, then go up with `git push origin <branch>`. A changed body goes up with `gh pr edit <pr> --body-file pr-<issue>.md`.
