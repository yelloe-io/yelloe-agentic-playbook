---
name: build-spec
description: Build a spec that is already split into issues with parallel builder agents on one integration branch, then test-audit, verify and hand over one pull request for a person to merge. Use when asked to "build this spec", "implement the spec", "run the spec" or "build these issues", or when several related issues should land together.
disable-model-invocation: true
---

# Build spec

You are the **orchestrator**. You build only: planning ended before you start. You start agents, merge their work onto one **integration branch**, and hand over one pull request. A person merges it. You never write feature code, except where the tool cannot start agents (see Build).

Ask the user only for a step that only the user can do, such as a production migration or credentials, or for a decision that can break much more than this run. Put every other question in the run log (see Parking) and continue.

The input is a spec issue or a set of issue numbers (`build-spec #40`, `build-spec 41-48`, `build-spec 41 43 47`). The tracker is GitHub Issues through `gh`, unless the repo's `CLAUDE.md` or `AGENTS.md` names another one. Name branches and worktrees by the conventions in those files. When they have none, use the names in this skill.

## Agents

You start every agent yourself: the architect, builders, fixers, the test auditor and verifiers. Tell each one: "Do not start agents." Start each agent with a fresh context and point it at sources (the spec, the issues, commits, files) instead of pasting them. Do not end your turn while an agent you started still runs: wait for each report (see Waiting).

- **Models.** Where your tool lets you choose, give the architect, the test auditor and the verifiers your strongest model at high effort, and the builders and fixers a strong model at medium effort.
- **Browser sessions.** When the app has a web UI, give each agent that drives it its own browser session. Use the repo's browser harness when it has one, else the Playwright CLI (`playwright-cli -s=<session>`). Name each session `<repo>-<slug>-<task>`, where the task is `issue-<N>`, `fix`, `cross`, `design` or `audit`. Session names can be global on the machine, so the repo and the slug keep two runs apart.
- **Ports.** Give each agent that runs the app its own port. Pick one that no process listens on: `lsof -iTCP:<port> -sTCP:LISTEN` prints nothing on macOS and Linux, and `netstat -ano | findstr :<port>` shows no `LISTENING` line on Windows. Another run can share the machine. Write each port in the run log.
- **Dev servers.** In Claude Code, start a dev server as a background task and stop it with TaskStop. Elsewhere, stop a server by its port, never by its process name. Before you trust a browser check, confirm the server on that port runs from the right worktree.

## Run settings

A comment headed `spec brief` on the spec issue is optional. The user or the caller writes it by hand. When it is missing, every default of this skill applies. Its lines set this run: `Level:`, `Builders:`, `Start:` (the branch to start from), `Order:`, `Checks:`, `Run:`, `Fix:`, test data and safety rules. Each line overrides the default of this skill. A line in the caller's message overrides the same line in the spec brief. A missing line keeps the default. Copy the lines into the run log.

- **Start:** create the integration branch there. When it names a pull request that is not merged, stop and tell the user.
- **Order:** follow it in Plan, on top of the blockers.
- **Checks, test data and safety rules:** put them in every builder, fixer, auditor and verifier brief.

## Levels

`Level:` sets how deep the run checks. The default is `standard`.

| | light | standard | full |
|---|---|---|---|
| Architect | skip | when the spec adds new modules | when the spec adds new modules |
| Test audit | skip, the gates only | run | run |
| Verifiers | one, main flows only | one for all issues, then the cross-issue flows | one per issue, plus one for the cross-issue flows |
| Fix rounds | 1 | 2 | 2, up to 5 for a high-damage failure |

## Checks

A run has three sets of checks. The first two keep the full test suite off the machine while builders work.

- **Narrow checks:** the tests related to the changed files, the type check, and the lint on the changed files. Builders, fixers and the test auditor run them before they report. They never run the gates.
- **Gates:** the full test, lint and type check commands from `CLAUDE.md` or `AGENTS.md`, in one committed gates script. Only you run it, on the integration branch, one run at a time. Start a run when the branch holds a merge that no run covered and no run is in progress. One run covers each merge up to its commit. The gates must pass on the commit the test audit starts from and on the commit the verifiers get.
- **CI run:** the repo's full CI workflow. CI can run tests that the gates leave out, on a smaller machine. The last commit of the integration branch needs one green full run before Hand over. A pull request run counts only when it runs the full workflow. Otherwise start the workflow by hand (`gh workflow run <workflow> --ref <integration branch>`). Treat a red job as a gates failure. When no full run is possible, write the reason in the run log and the report.

Verifiers run none of these. Give each one the commit and the result of your last gates run.

Find the narrow check commands once, in Readiness. Use the related-files mode of the test runner when it has one, else the test files of the changed modules. Write the commands in the run log and in each brief, so that no agent searches again. When the repo cannot run part of its tests, the narrow checks are the gates: write that in the run log and let one agent run them at a time.

Tell each agent to read only the failures of a check, not its full output. When the gates fail, find the merge that broke them from the failing tests, and send the failure to the builder of that issue, or to a fixer when no builder owns it.

## Waiting

A background agent's report arrives between your tool calls. A long foreground command can move to the background and let your turn end. To wait without ending your turn, run `bash <this skill folder>/scripts/wait.sh [file ...]` in the integration worktree, again and again. It ends within 150 seconds, and earlier with the change when a remote branch moves or a named file changes. With local branches only, pass `-r refs/heads` first. When your tool has a native wait for agents or tasks, use it instead.

- A notice that an agent is "waiting on its own background work" is not a report. Wait for the report.
- Start the gates in the background, write their exit code to a file, and wait on that file.

## Steps

### 1. Readiness

1. Collect the issues. For a spec, take its sub-issues or the issues that name it as their parent. Read every issue: body, comments, labels, blockers. Read the `spec brief` comment when there is one; without one, use the defaults.
2. When the spec has no issues, stop and say: "split the spec into issues first". When an issue still has an open question (an unanswered question in it, a `needs-info` label, or a status line such as `needs-info` as the first line of its body, which is where the status goes when the repo has no labels), stop and list the questions. Build nothing.
3. A `Fix:` line or a `Run: r2` line is a rare case: read [rare cases](references/rare-cases.md) and follow it.
4. Look for a run in progress: an open draft pull request whose body holds the run log for these issues. Continue from the state it records. Run `git worktree list` first and use each worktree that exists. Never add a worktree at a path that exists. For each issue the log shows as `building` or `failed`, start a new builder on its existing branch.
5. Set the builder count: `Builders:` from the run settings, else the number in `CLAUDE.md` or `AGENTS.md`, else 3, or 2 when builders must run a dev server and a browser.
6. Find the gates. When `CLAUDE.md` or `AGENTS.md` names none, write "no gates" in the run log. When the repo has no gates script, you commit one in Set up (for example `scripts/gates.sh` at the repo root, a file that starts with `set -e`). Find the narrow checks. Read the CI workflow and write in the run log what a push to the trunk runs, what a pull request runs, the machine size and the time limits. When a push runs less than a pull request, say in the report that the merge is not tested in full.
7. When an issue adds or changes UI, look for a design target: a prototype, screenshots or a page to copy, named in the spec, or a design doc in the repo. When there is none, write "no design target, builders follow the existing pages" in the run log and repeat it in the report.
8. When the app has a web UI, check that the browser tool works (for example `playwright-cli --version`). When it does not, stop and say which tool to install. Build nothing.
9. Find out how to run the app and whether builders or verifiers write to a shared store, such as one local database. When the repo has a recipe that gives each agent its own copy, use it for each agent and put the result in its brief. When it has none, run the agents that write to it one at a time, and write that in the run log.

### 2. Set up

1. Create the integration branch from the start point, else from the trunk, in its own worktree beside the repo: `git worktree add ../<repo>-integrate-<slug> -b integrate/<slug> origin/<start>`. Do all integration work there. Never switch branches in the session checkout. Install the dependencies. Commit the gates script when Readiness asked for one, else an empty commit (`git commit --allow-empty -m "Start build-spec run"`). Push.
2. Open a **draft** pull request from the integration branch to the trunk, with one closing line per issue (`Closes #N` on GitHub) and the run log in its body. CI now runs on each merge you push. When the start point is not the trunk, wait for a green CI run on this first commit. A failure there belongs to the start point: stop and tell the user.
3. When you cannot push, follow "No push" in [rare cases](references/rare-cases.md).

### 3. Architect

Skip this step when the project has no package manifest yet (no stack), or at level `light`, or when the spec adds no new modules. Write "Architect: skipped" and the reason in the run log. When the spec has a scaffold issue, run this step after that issue merges, before the next wave.

Otherwise start one architect agent with [the architect brief](references/architect.md). Give it the spec, its issues, its worktree `../<repo>-architect-<slug>` and a branch `shapes/<slug>` from the integration branch. It commits shared types, interfaces and empty modules, pushes its own branch and reports a module map. Merge its branch and run the gates.

### 4. Plan

Plan the work in **waves**. Take each issue's paths from the module map, or from the issue and the code. An issue can start when its blockers are merged and no running issue touches the same paths. Write the plan into the run log. Nobody approves it. List each step only the user can do in the run log and in your first message to the user.

### 5. Build

Start one builder per issue on the **frontier**: the issues whose blockers are merged and whose paths no running builder holds. Start each as a background agent with the builder brief below, in its own worktree `../<repo>-issue-<N>` with its own port. Copy the untracked files the app needs, such as `.env.local`. Worktrees stay until the hand-over.

Never run more builders than the builder count. Count only builders that are building or fixing. Where the tool cannot start agents, build the issues one after another yourself with the same brief.

A builder cannot wait for an answer. It ends its turn with the question in its report. Then:
- **A technical question:** answer it and resume the builder with the answer (in Claude Code, with SendMessage; elsewhere, start a new builder on the same branch with the answer).
- **A question about what a user sees, or about scope:** park the issue (see Parking). Keep the other builders running.
- **A refactor the feature needs to fit cleanly:** when it stays in that issue's files, decide it as a technical question. When it touches other issues' files, make it a new issue, build it first, and hold the issues that depend on it.

When a builder reports done:
1. Merge its branch into the integration branch, one merge at a time: `git merge --no-ff <branch> && git push`. On a conflict, send the builder back to merge the integration branch into its branch and resolve it.
2. Start a gates run when none is in progress.
3. Update the run log.
4. Keep the builder for its fixes later.
5. Start the next issues the frontier allows.

### 6. Test audit

At level `light`, skip this step and write "Test audit: skipped, level light" in the run log.

When every issue that is not parked is merged and the gates pass, start one fresh agent with the test audit brief below, on a branch `audit/<slug>` from the integration branch, in its own worktree. It proves on the whole branch that the tests can fail, rewrites weak tests, applies the coding standards and checks spec fit. Merge its branch and run the gates. Send its missing work to the builder of that issue and merge the fix before Verify. Keep its survivors and scope creep for the hand-over.

When the user asks for a separate code review, run it here (if you have a code review skill, use it) and send its serious findings to a fixer with the fixer brief in [rare cases](references/rare-cases.md).

### 7. Verify

When the audit branch and its follow-up fixes are merged, or at level `light` when every issue that is not parked is merged:

1. Read the integration commit: `git -C ../<repo>-integrate-<slug> rev-parse HEAD`. Give each verifier its own worktree at that SHA (`git worktree add --detach <path> <SHA>`) and confirm that `git -C <path> rev-parse HEAD` prints it. Start fresh verifiers with the verifier brief below, as the level sets. The cross-issue flows are the places where two or more issues meet. At level `full`, run as many verifiers at once as the builder count.
2. When the spec has a design target, also start one design reviewer with the verifier brief in design review mode. It reviews the whole run, not one issue, and returns a findings file.
3. When an agent reports a mistake that a running agent can repeat, send the lesson to each running agent at once.
4. Send each failure to the builder of that issue, each design finding to the builder of the page where it shows, and each cross-issue failure to the builder that owns the failing path, or to a fixer. From the second failure of one criterion, tell the builder or fixer to find the cause the failures share, not to patch the one case. The fixer reproduces the failure first and captures it in a regression test at a public seam when the tests can express it. Merge each fix as before and run the gates.
5. Run only the failed and blocked checks again, with a fresh verifier at the new integration commit. A check that passed may carry forward only when the fix cannot touch it; the verifier writes why in the record. Stop after the fix rounds of the level and record what still fails. At level `full`, keep going for a failure that can do high damage after release, such as wrong data or a broken main flow, up to 5 rounds in total. A fix after the test audit gets the gates and a verifier, not a second audit. List each such fix in the hand-over.

### 8. Hand over

1. Post the run log as a comment on the pull request, headed `build-spec run log`.
2. Write the pull request body with one section per issue. If you have a pull request skill, use it. Otherwise lead with what changed and how it was proven, then the risk of merging. Keep a closing line only for each issue that is built and verified. When a design reviewer ran, add a design review section: the findings left, and the places where a person must judge the result.
3. Update each issue's acceptance criteria from its record: tick a box only when every check mapped to that criterion passed. Leave failed, blocked and accepted criteria unticked, and untick a box the record does not support. Change only the checkboxes, not the wording or the rest of the body. Use `gh issue edit <N> --body-file <file>`, then read the issue again to confirm. Skip this when the user forbids issue edits.
4. Confirm the full CI run of the last commit is green (see Checks). Then mark the pull request ready for review.
5. You cannot stop another agent's task in every tool. List each agent that still runs in your report, by its id. Close each browser session whose name starts with `<repo>-<slug>-`, and no others. Move each record and its evidence outside the worktrees. Then remove every worktree the run made.
6. Report. **A person merges.** Never merge into the trunk yourself. In under 300 words give: the pull request link, the CI run of the last commit and its result, the state of each issue, the commit of the last browser check per issue and each later change, what still fails, the audit findings left, each parked question, each decision you made, each decision a builder made on its own, each agent that still runs, and each mistake you saw more than once.

## Parking

A question about what a user sees, or about scope, is not yours to answer. Neither is work that can pass only with a changed acceptance line or a weaker test: no agent, you included, makes that change. Park the issue:

1. Park every issue that depends on it too. Stop their builders after they commit.
2. Remove their closing lines from the pull request body.
3. Write the question in the run log, with the issue number.
4. Continue with the other issues.

A parked issue gets its own run and pull request after the answer.

## The builder brief

```
You are a builder in a build-spec run.
Issue: #<N>. Integration branch: integrate/<slug>.
Worktree: <path>. Dev server port: <port>. Browser session: <repo>-<slug>-issue-<N>.
Narrow checks: <commands>.
Test data and safety rules: <from the run settings, or "none">.
Design target: <prototype, screenshots or page to copy, or "none">.
Test rules: <this skill folder>/references/tests.md.

1. In the worktree, create branch issue/<N>-<slug> from origin/integrate/<slug>.
   Install the dependencies.
2. Read the repo's CLAUDE.md or AGENTS.md, the issue with its comments, and the code it touches.
3. Build the issue with tests, by the test rules. Use the project's existing patterns
   and UI controls. With a design target, put a screenshot of your result next to the
   target and fix each difference before you report.
   Skip runtime verification, quality review, issue edits and pull requests:
   they run later on the integration branch.
4. Do not start agents. Other builders work in these paths right now: <paths>.
   Do not edit them. If you must, ask the orchestrator first.
5. Ask the orchestrator, not the user, when you are unsure, or when the work cannot meet
   an acceptance line or a test as it is written. You cannot wait for an answer:
   commit, end your turn, and put the question in your report. The orchestrator resumes you.
6. Commit as you go. Before you report: merge origin/integrate/<slug> into your branch,
   run the narrow checks on the files you changed, and push your branch.
   Do not run the full test suite: the orchestrator runs it. Do not run git fetch:
   the worktrees share one repo, so the orchestrator's push keeps origin/integrate/<slug> current.
7. Stop your dev server and close your browser session. Then report: branch, last commit,
   paths touched, every decision you made, anything left open.
```

## The test audit brief

```
You are the test auditor in a build-spec run. You did not write this code: judge it as a stranger.
Spec: #<N>. Issues: <numbers>. Branch: audit/<slug> from origin/integrate/<slug>.
Base: <trunk>. Worktree: <path>. Narrow checks: <commands>.
Test rules: <this skill folder>/references/tests.md. Do not start agents.

1. Read the spec, its issues, CLAUDE.md or AGENTS.md, and CODING_STANDARDS.md when the
   repo has one. Read git diff <base>...HEAD. List the changed source and test files.
2. Mutants. Source files are frozen: you change tests only. On the changed lines, run the
   project's mutation tool when one is set up (see the test rules). Never install one.
   Otherwise plant 2 or 3 deliberate mutants per changed source file by hand, one at a time:
   flip a comparison, drop a branch, change a constant. Run the tests that cover the file,
   then undo the edit by hand, not with git checkout. Never commit a mutant.
   For each survivor: when no caller can see a difference, list it as equivalent with the
   reason. Otherwise write one test at the seam the spec names, with the expected value
   taken from the spec, that passes on the original code. Plant the mutant again and see
   it die. When it survives one improvement of the test, list it.
3. Weak tests. Check each new or changed test against the weak shapes and the undefined
   rule in the test rules. Rewrite each weak test, or delete it when another test covers
   the behavior. Add the close for each database, server or browser a test leaves open.
4. Standards. Apply CODING_STANDARDS.md and the lint to the changed lines. Fix each break
   in the changed lines. Leave old code as it is.
5. Spec fit. List missing work (an acceptance line with no code) and scope creep
   (a change no part of the spec asks for). Fix neither.
6. Run the narrow checks on the files you changed. Read only the failures. Fix until green.
   Do not run the full test suite.
7. Commit with a message that starts "Test audit:" and push your branch. Report in under
   200 words: mutants killed out of total, tests added, rewritten or deleted, each survivor
   (file, line, mutant, reason), standards fixes, missing work, scope creep, commits.
```

## The verifier brief

```
You are a verifier in a build-spec run. Try to break the feature.
Scope: issues <numbers> | the cross-issue flows: <where the issues meet> | design review.
Depth: adversarial (main flows at level light).
Commit: <SHA>. Worktree: <path, detached at the SHA>. Port: <port>.
Browser session: <repo>-<slug>-<task>. Gates on this commit: <result>.
Open notes from the builders: <notes>. Test data and safety rules: <rules>.
Design target: <for design review, or "none">.
Records and evidence go in: <folder outside the repo>.
Guide: <this skill folder>/references/verification.md.
Do not start agents. Do not change code. Do not edit issues.

1. Confirm git rev-parse HEAD in the worktree prints the commit. Start the app from that
   worktree on your port, the way the repo's CLAUDE.md, AGENTS.md or verify notes say.
2. Read each issue. Split each acceptance criterion into atomic checks: one precondition,
   one action, one observable result. Write one record per issue in the guide's format,
   with every check blocked until it runs.
3. Run each check like a user: UI through real controls in the browser, APIs with real
   auth. At adversarial depth, add a check for each relevant axis in the guide. Expected
   results come from the issue and the project's contracts, not from the code.
4. Inspect the raw evidence of every pass. Missing proof stays blocked. A contradiction is a fail.
5. Stop the app and close your browser session. Return: the record paths, each fail and
   blocked check with its evidence and steps to reproduce, the issue that owns each
   cross-issue failure, and the state you left behind.
```

In design review mode, the verifier follows "Design review" in the guide instead of steps 2 to 4 and returns its findings file.

## The run log

Keep the log in the draft pull request body from the start, or in a file when you cannot push, and update it on every change. It moves to a comment at the hand-over. It is how a new session picks up an interrupted run.

```
<!-- build-spec run log -->
Level: standard (default). Builders: 3 (default). Integration branch: integrate/<slug>.
Phase: Build.
Gates: scripts/gates.sh at the repo root (npm test, npm run lint, npm run typecheck).
Narrow checks: <test command for changed files>, <type check>, <lint on changed files>.
CI workflow: a push runs the unit tests, a pull request adds the browser tests. 2 CPUs, 8 GB, 15 minutes.
Architect: skipped, no new modules.
Shared data: one local database, writers run one at a time.
Ports: #41 4101, #43 4103.

| Issue | Blocked by | Paths | State | Branch |
|---|---|---|---|---|
| #41 | - | src/cart/* | merged | issue/41-cart-totals |
| #42 | #41 | src/cart/* | building | issue/42-cart-discounts |
| #43 | - | src/checkout/* | parked | issue/43-checkout-header |

Parked:
- #43: Which label does the checkout button show?
```

States: `waiting`, `building`, `merged`, `verified`, `failed`, `fixed`, `parked`. Phases: `Readiness`, `Set up`, `Architect`, `Build`, `Test audit`, `Verify`, `Fix round <N>`, `Hand over`.

## Rules

- Commit before you stop a builder. Stopping an agent can lose uncommitted work.
- Review a diff by its branch or pull request. A diff against a stale local trunk shows other builders' work as new.
- When the trunk moves during a long run, merge it into the integration branch before the test audit.
- Base a time estimate on the durations measured in this run. Add one fix round per issue.
- Run one git operation at a time on the integration branch. You own it. No agent pushes to it.
