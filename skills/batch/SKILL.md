---
name: batch
description: Run a batch of GitHub issues from the current repo in parallel. One worker per issue in its own worktree, a blind review of each diff, review rounds, one report per round, one PR per issue with CI follow-up. Use when the user asks to run, start or continue a batch of issues.
disable-model-invocation: true
---

# Batch

You are the orchestrator. You decide what runs, brief the workers, judge what returns, and talk to the user. Workers write the code. A reviewer reads each diff blind and runs a code review on it. The user sees one conversation and gets one report per round.

The batch runs on the current repo. Run every git and `gh` command against it.

Two briefs live in this skill's folder:

- [references/worker.md](references/worker.md): the brief for a worker.
- [references/reviewer.md](references/reviewer.md): the brief for a reviewer.

Start each worker and reviewer as a subagent and give it the full text of its brief, plus the details below. In Claude Code, use a strong model for workers (Opus) and reviewers, at high effort; other agents use their own subagent or parallel task feature. Run this session at high effort too where your agent supports it.

A worker costs a full context of its own, so start one per issue and no more. Do the small things yourself: reading an issue, a `gh` call, updating the status file.

**Never**, unless the user's message names that exact action:

- Commit or edit code, tests included. Every code change goes to a worker and then through a later review round, even a one-line format fix.
- Decide a point the issue leaves open, or tell a worker or reviewer that the user decided something they did not. An open point becomes `needs you`.
- Close an issue, merge a PR, or delete a remote branch.
- Open a side PR for follow-up work found during the batch. It becomes a new issue in the batch, with its own worker and review.

## 1. Pick the issues

The user names the issues, or you pick together. To propose, prefer open issues labelled `ready-for-agent` (`gh issue list --label ready-for-agent --state open`), or the user's own (`--assignee @me`) when the repo has no such label, and suggest the ones a worker can finish alone: a clear problem and a known intent. Leave out issues labelled `needs-info`, umbrella and planning issues, blocked issues, and features that need product decisions.

Another session may be running a batch on the same repo at the same time. Before you propose or accept an issue, read every status file (see step 2). An issue listed in one of them belongs to that batch: leave it out, and tell the user if they named it.

Work outside a batch leaves no status file, so also check each candidate for a branch or worktree that names its number (`git worktree list`, `git branch -a`) and for an open pull request (`gh pr list --state open --search "<number>"`). Either one means the issue may be in progress in another session or by hand. Do not propose it. If the user names it, say what you found and start it only after a yes; the worker then continues on the existing branch and worktree.

Wait for the user's pick. A batch holds up to 8 issues.

## 2. Keep the status file

The status file lets parallel sessions see which issues are taken. Keep it inside the repo's shared git folder, which git never commits and every worktree shares: `$(git rev-parse --git-common-dir)/batch/`.

Name the batch by date and letter, such as `2026-11-16-b`, taking the first letter no other status file uses. Write `<name>.json` there as soon as the issues are picked, before any worker starts, and after every change of state. Write only your own file.

```json
{
    "name": "2026-11-16-b",
    "issues": [{ "number": 42, "title": "Saving settings acts on the first user", "state": "working", "needs": "" }]
}
```

`title` is a short plain description. `state` is one of: `queued`, `working`, `live check`, `reviewing`, `needs you`, `ready to push`, `CI running`, `CI red`, `green`. `needs` is empty, or one sentence saying what the user must do.

## 3. Start the workers

Start all workers at once, in the background where your agent supports it. Brief each one with the worker brief, the issue number, and anything the user said about it that the issue does not say. The worker reads the issue and the project instructions itself.

## 4. Handle what returns

- **A question** on intent or product behaviour: set `needs you`, put the question in `needs`, and ask the user. The other issues continue. Send the answer to the same worker.
- **Waiting for a live check**: resume the worker when fewer than 3 app instances are running. Until then the state stays `live check`.
- **Done**: start a reviewer with the reviewer brief, the issue number, branch, base and worktree path. Do not pass the worker's report or your own view.
- **Review failed**: send the findings to the same worker. When the fix returns, send the same reviewer the new commits and ask for a later round, so it builds on what it already found. If that reviewer cannot be continued, start a new one and give it every earlier finding and the commit the last round read. Still do not pass the worker's report.
- **Third failed review**: patching is not converging, so do not send another list of findings. Ask the worker to step back: say in a few sentences why its fixes keep missing, what all the findings so far have in common, and what different approach would remove that cause, then build that approach. Give it every finding from all three rounds, not only the last. Tell the user in one line that the issue is being rethought and why. If the new approach changes what the user would get, or needs a product decision, set `needs you` with the question instead of building it.
- **After the rethink**: review the new approach as a fresh change, with a new reviewer. It gets two more reviews. If the second one fails, set `needs you` and show the user the open findings and the two approaches tried. An issue is rethought once.
- **Fix round on visible behaviour**: when a fix round touched what a user sees, or when users are signed in or out, resume the worker for a repeat live check on the final commit before setting `ready to push`.
- **Review passed**: set `ready to push`. Keep the reviewer's side notes and questions for the round's message.

If your agent cannot resume a finished subagent, start a new worker on the same branch and worktree, and give it the issue, the earlier report and what it must do next.

## 5. Report once per round

A round ends when no issue is `working`, `live check` or `reviewing`.

**Test the round together first.** CI tests each PR alone, so two branches can each pass and still break the base once both are merged. When two or more `ready to push` issues share a base, fetch that base and merge all of them onto `origin/<base>` in a throwaway detached worktree. There, run the checks from the project instructions once for every app the branches touch: lint, type check, tests and build. No worker is running at this point, so the suite starves nobody. Push nothing from that worktree, and remove it afterwards.

- All pass: continue, and say in the round's message that the branches were tested together.
- A merge conflict or a failure: find which issues collide, from the conflict or the failing output. Keep the one that is closer to the base as it is, set the other back to `working`, and send its worker the collision and the other branch's name to build on. Review that fix as a later round, then test the round together again. The issues that do not collide stay `ready to push`.

Then send one message that lists every `ready to push` issue: what changed and why in a sentence, the branch, the commits, the PR title, any flags the worker raised, which roles and screens the live check covered, and every side note and question from the reviewer, one line each. Do not filter or drop any of them, also not when the user asks for a short summary. Then land them as below without waiting; the user reads the report and the PRs before merging, and an item they object to goes back to its worker.

## 6. Land what passed

For each `ready to push` item, push the branch under its own name and open one PR for it, into its base, following the repo's PR conventions in its CLAUDE.md or AGENTS.md. If you have a `pr` skill, use it and skip its review step: the reviewer already reviewed this branch. Otherwise use `gh pr create` with a short body: what changed and why, how it was tested, and the issue it resolves. Set `CI running`.

Watch the checks (`gh pr checks <number> --watch`). On a red run, set `CI red`, send the failing output to the same worker, review the fix, and push the fix commit to the same branch. Never push to the base branch.

When the checks pass, set `green`. Merging and closing issues stay with the user.

## 7. Close the batch

Done when every issue is `green` or has a written reason why it is not. Report in plain sentences: what landed, what is still open and why, and which issues are ready to close. Then delete your status file, so its issues are free again.
