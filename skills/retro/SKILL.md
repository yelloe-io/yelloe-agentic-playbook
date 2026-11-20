---
name: retro
description: Conduct a retrospective on one or more coding sessions, and propose a fix for each repeated mistake. Use when the user asks for a retro or retrospective, or wants to learn from past sessions.
disable-model-invocation: true
---

The user has asked for a **retrospective**. You are suggesting improvements to the coding agent's **environment** to improve future runs. You propose; the user approves; you build only what the user approves.

## Steps

1. If you have the `writing-for-agents` skill, load it for the writing style guide. Otherwise, keep every line you propose short, and put it where an agent reads it only when it needs it.

2. Read the primary sources for the sessions the user specifies. If the user doesn't specify, default to the current session. The user can ask for a wider scope, such as "the last 10 sessions and 50 commits". Read these sources:
   - **Session logs.** Claude Code keeps transcripts in `~/.claude/projects/<slug>/*.jsonl`, where the slug is the absolute repo path with each `/` and `.` changed to `-`. Codex keeps them in `~/.codex/sessions/`. For other agents, ask the user where the logs are. For a wide scope, give each transcript to its own sub-agent, so the raw transcripts stay out of your context.
   - **Commits.** For a wide scope, run `git log --oneline -<N>` and read the full message of each commit that reverts, fixes or redoes earlier work. If the repo has a GitHub remote, read the review comments of recent merged pull requests.

   A **mistake** is anything the user corrected, anything a check failed on, anything the agent redid, and any long search for a file or a fact. Note each with one line of evidence: what went wrong, where, and what fixed it.

3. Look for candidates for improvement in these categories.

- **Navigation**: how easy was it for the agent to find the right files? Are there hidden dependencies between files? Would a **navigation pointer** make it easier? _Use when_ the session took a long time to find a piece of information.
- **Automated checks**: are there automated checks that could catch errors the agent made? Linting, typing, tests, filesystem linters? Read the repo's own check command first (its `package.json`/build-tool `lint`/`check` scripts, its CI workflow), so a check that already exists but sits unwired or silently broken is the finding, not a reinvention. A repo with no **guardrail** (no pre-commit hook and no CI job running its lint/typecheck/test command) is itself a finding: an un-linted repo is a standing missed opportunity, not a neutral default. _Use when_ the agent made a mistake an automated check could have caught, or the repo has no guardrail at all.
- **Coding standards**: should the **reviewer agent** be given a new rule to enforce? Should an existing rule be removed or clarified? Classify the violation first: a **mechanical** one (a fixed syntactic pattern, a banned API, an import shape, a file-location rule) gets a deterministic check, full stop: a custom rule in the repo's own linter, a new pre-commit hook, or a new CI job, whichever the repo's language and existing guardrail make cheapest. Default to building the check over writing the rule. Reserve `CODING_STANDARDS.md` for genuine **judgement calls** (cross-file consistency, "matches the surrounding style," anything no guardrail could ever substitute for). _Use when_ the reviewer agent failed to catch a mistake.
- **Global AGENTS.md**: are there any steering instructions that should be moved to coding standards (or automated checks) instead? _Use when_ the AGENTS.md or CLAUDE.md file is particularly large, in the repo OR the user's global scope.
- **Tool economy**: did the agent make expensive tool calls that could be streamlined? Is there any custom tooling (CLIs, MCPs) that is particularly token-inefficient? _Use when_ the agent made an expensive tool call.
- **No-ops**: look for instructions in steering files that don't modify the agent's behavior. _Use when_ the steering files are large and unwieldy.
- **Information access**: look for opportunities to increase the agent's access to information. Teeing dev server logs, readonly access to third-party services. _Use when_ a crucial piece of information was not available to the agent.

4. Group the mistakes into **classes**: one class is one cause, however many times it showed up. A class is **repeated** when it happened at least twice, in this scope or against a rule that already exists. A mistake that an existing written rule already covers is a repeat by definition: the rule does not work, and the fix is a stronger level, not a reworded rule.

5. Propose one fix for each repeated class, at the **strongest level that works**. The levels, strongest first:
   1. **Code structure**: make the mistake impossible. One source of truth, one place to change, a deep module that hides the trap.
   2. **Types**: make the mistake fail to compile.
   3. **Lint rule or hook**: make the mistake fail a deterministic check, locally or in CI.
   4. **Test**: make the mistake fail a test.
   5. **Written rule**: a line in `CODING_STANDARDS.md`, or as a last resort in `AGENTS.md`/`CLAUDE.md`. Use it only for judgement calls that no level above can catch.

   For each proposal, say why the levels above it do not work. Propose at most 3 new written rules in one retro: keep the classes with the most damage, and list the others as watched. A class that happened once goes on the watch list, not into a proposal.

   Check the existing rules too. A written rule that did not catch or prevent anything across the scope, while its mistake still happened, needs a stronger level. A rule whose mistake never shows up anymore because a check now catches it is a candidate to remove. Keep every security rule.

6. Present the candidates from step 3 and the proposals from step 5 to the user, in order of severity. For each: the class, the evidence, the level, and the exact change. Then stop. Build nothing until the user approves a proposal by name. Build each approved proposal as its own small change, following the repo's conventions for branches and pull requests.

## Reference

### Implementation vs Review

Remember that all work goes through two stages: implementation and review. The implementation agent has the most **context pressure**. They are responsible for exploration, writing code, and debugging failures.

The review agent has the least context pressure: it receives a diff, so no exploration needed. It often does not need to write code or debug.

This means that the review agent should be responsible for imposing coding standards, not the implementation agent.

### Files

You have access to several files in the repo:

- `CLAUDE.md`/`AGENTS.md`: these files are pushed to the context window of any agent working in this repo. They should be used incredibly sparingly, usually only for **navigation pointers** to other files.
- `CODING_STANDARDS.md`: this file is read during review, not implementation. Add **navigation pointers** to docs folders if the standards file gets more than 1,000 lines long.
- Docs: use docs as references files, pointed to by other files. Look for existing docs before writing new ones.
- Skills: use skills for docs (since their description goes into the agent's context window), or for user-invoked commands.
