---
name: to-issues
description: Break a spec, plan, or the current conversation into tracer-bullet issues, each declaring its blocking edges and a ready-for-agent or needs-info label, published to the repo's issue tracker. Use when the user wants a spec or plan split into issues or tickets.
disable-model-invocation: true
---

# To Issues

Break a plan, spec, or conversation into a set of **issues**: tracer-bullet vertical slices, each declaring the issues that **block** it.

The tracker is GitHub Issues through `gh`, unless `AGENTS.md` or `CLAUDE.md` names another one. If the repo has an issue template, or the conventions file names a rule for issue titles, labels or how to split the work, follow it instead of the defaults in this skill.

## Status labels

This skill gives each issue one status label:

- `ready-for-agent`: the slice is fully decided, and an agent can build it with no questions.
- `needs-info`: a decision is still open. Name it in the issue body.

Default to `needs-info`. An optimistic `ready-for-agent` means a real decision gets guessed instead of asked.

When a label is missing, create it only in the user's own repo: the repo owner is the user's own account (`gh repo view --json owner` against `gh api user --jq .login`). In any other repo, ask the user before you create a label. Without the label, write the status as the first line of the issue body.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Issue titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer bullet** issues.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

</vertical-slice-rules>

Give each issue its **blocking edges**: the other issues that must complete before it can start. An issue with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand-contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own issue blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in an issue blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify issue: green is promised only there.

### 4. Check the coverage

Map each user story and each deliverable of the source to the issue that owns it. Add each one that has no owner to an issue. Compare each acceptance criterion with its item in the source: a criterion asks for no more than the item does. This step is done when each item has one owner.

### 5. Quiz the user

Present the proposed breakdown as a numbered list. For each issue, show:

- **Title**: short descriptive name
- **Blocked by**: which other issues (if any) must complete first
- **Status**: `ready-for-agent` or `needs-info`, and the open decision for `needs-info`
- **What it delivers**: the end-to-end behaviour this issue makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each issue only depend on issues that genuinely gate it?
- Should any issues be merged or split further?

Iterate until the user approves the breakdown.

### 6. Publish the issues

Publish the approved issues.

When the source is an existing issue, list the child issues it already has first. On GitHub, run `gh api repos/{owner}/{repo}/issues/<parent>/sub_issues`. Do not publish an issue that already exists as a child issue.

Run each `gh` call from the repo folder. Stop at the first error and fix it before the next issue. Publish one issue per slice in dependency order (blockers first) so each issue's blocking edges can reference real identifiers. Write each issue's "Blocked by" in its body, and also set the tracker's native blocked-by link where it has one.

When the source is an existing issue, make each new issue its child where the tracker has sub-issues. On GitHub, run `gh api -X POST repos/{owner}/{repo}/issues/<parent>/sub_issues -F sub_issue_id=<id>`, where `<id>` is the child's numeric id (`gh api repos/{owner}/{repo}/issues/<number> --jq .id`), not its number.

Apply one status label to each issue (see [Status labels](#status-labels)).

Do NOT close or modify any parent issue.

<issue-template>

## Parent

A reference to the parent issue on the tracker (if the source was an existing issue, otherwise omit this section).

## What to build

The end-to-end behaviour this issue makes work, from the user's perspective, not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- A reference to each blocking issue, or "None, can start immediately".

</issue-template>

Avoid specific file paths or code snippets: they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts: not a working demo, just the important bits.
