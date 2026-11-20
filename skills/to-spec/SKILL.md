---
name: to-spec
description: Turn the current conversation into a spec and publish it to the project issue tracker, with no new interview, just synthesis of what was already discussed. Use when a plan or grilling session is settled and the user wants it written down as a spec.
disable-model-invocation: true
---

This skill takes the current conversation context and codebase understanding and produces a spec. Do not interview the user: write the spec from what you already know. The only question is the check on test seams in step 2.

**Existing spec.** When the spec issue already exists, edit it in place. Never publish a second spec for the same work.

## Process

1. Read each function, table, check and screen that the spec will name. For each stored value that the spec changes, find every writer and every entry point. This step is done when you have read each one in this session. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better: the ideal number is one.

   Check with the user that these seams match their expectations.

   When the spec adds or changes UI, the spec needs a design target. The target is either a prototype the user approved (its branch, its route and its screenshots at desktop and phone width) or an existing page to match. When the conversation named no target, ask the user which page to match, or suggest a prototype round first. Builders build to the target.

3. Write the spec using the template below. Then publish it to the project issue tracker: GitHub Issues through `gh`, unless `AGENTS.md` or `CLAUDE.md` names another one. Follow the repo's conventions for issue titles and labels. Apply one status label where the label exists: `ready-for-agent` when the spec is fully decided, `needs-info` when a decision is still open. Default to `needs-info`. Name each open decision under Further Notes.

4. Give the user the link to the spec. Then suggest the optional next steps, in one line each:
   - Split the spec into issues with blocking edges (the `to-issues` skill does this).
   - Take a short quiz on the spec before anyone builds it (the `explain-spec` skill does this).

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions
- Every writer and entry point of each stored value that the spec changes

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts: not a working demo, just the important bits.

## Design Target

Only when the spec adds or changes UI. The target: the prototype branch, route and screenshots, or the existing page to match. Name each change to the prototype that the user approved after the prototype round.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature, and each decision that is still open.

</spec-template>
