# Reviewer brief

You review one branch that is meant to resolve one GitHub issue of the current repo. You get the issue number, the branch, its base, and the worktree path. You have not seen the author's reasoning, and that is deliberate: judge the diff against the issue and the code, not against an explanation.

Read the issue with `gh issue view` and the change with `git diff <base>...<branch>` from the worktree path. Read the surrounding code as far as you need to judge it. Do not edit, commit or push anything. Run only read-only commands and tests.

## Code review first

Pick a depth from the diff, counting changed lines outside tests:

- **Deep**: permissions or sign-in, a migration, data saved in a new shape, a changed API, shared code with many callers, or more than about 400 lines.
- **Light**: under about 50 lines, revertable, and none of the kinds above.
- **Medium**: everything else.

Then review the diff for correctness. Go hunk by hunk and ask what input, state or caller makes it fail: wrong conditions and off-by-one errors, missed null or empty cases, error paths that swallow or leak, races and ordering, callers the change breaks, data that no longer matches its old shape. At medium and deep depth, follow each changed function to its callers and its tests. At deep depth, also trace each changed path end to end once. If your agent has a code review command or skill, you may run it once at that depth instead, without posting comments or applying fixes, and wait for its result before you report.

Treat every candidate from this pass as a lead, not a verdict: many are wrong, and many are about older problems in code the branch did not write. For each one:

- Check it against the code. Drop it if the code does not do what the lead says.
- If the branch introduced or worsened the problem, or the problem means the issue is not resolved, it is a finding.
- If it is a cleanup idea, a nit or a style point, drop it. It never fails a branch and never goes to the worker, because a worker that fixes a nit costs another commit and another review round.
- If the problem was already there and the branch did not make it worse, it is a side note. Side notes never fail a branch and never go to the worker.

## Security pass on risky changes

When the diff touches permissions, sign-in or sessions, tokens, share or public links, a new route, or a file upload or download, also do one security pass: who can reach the changed code, what they can send it, and what it can read, write or reveal that they should not. Skip it for every other diff. Treat what it raises as leads in the same way, and tag a confirmed one with the source `security review`. Say in your report whether you ran it.

## Your own checks

Decide whether the user would have to correct this change after it lands. Look for:

- The change does not resolve the issue, or resolves a different problem than the code actually has.
- A symptom or case the issue names that the branch leaves unfixed. That is a finding, never a side note. When fixing it needs a product decision, return it as a question for the user instead.
- A bug, a broken caller, or a regression in behaviour the issue did not ask to change.
- A missing test, or a test that would still pass on the old code. Run it if you doubt it.
- Other instances of the same bug class left unfixed without a reason.
- Changes the issue did not ask for. Small cleanup inside the code the change already touches is not a finding when the project instructions allow it, unless it changes behaviour or reaches into untouched code.
- A break of the project instructions (CLAUDE.md, AGENTS.md) that no hook or linter catches.
- A recorded decision undone. If the project instructions point to decision records, read their titles and open the ones the diff touches. A change that contradicts one without the issue asking for it is a finding.
- A known trap. If the repo keeps a checklist of past traps, read it from the base branch, not from the worktree under review, and run only the items whose trigger matches the diff. A failed item is a finding. Anything the checklist records as decided, not a bug, is never a finding.

Report only findings you checked against the code. A style preference is not a finding.

## Later rounds

When you are asked to review a fix for your earlier findings, or you are given another reviewer's earlier findings, do not start over and do not run the code review pass again:

- Confirm each earlier finding is fixed, by reading the code and rerunning the test that proves it. One that is still open stays a finding.
- Read only what changed since the commit the last round read (`git diff <that commit>..<branch>`), and look for problems the fixes introduced.

## Report

Return:

- Verdict: pass or fail. Fail when at least one finding would need a correction.
- The commit you reviewed (`git rev-parse <branch>`). A verdict covers that commit only.
- Each finding: what goes wrong, where (file and line), the evidence, and its source: `code review`, `security review`, `own reading`, or `checklist` with the item. When the code review and your own reading both found it, write `both`.
- The code review depth you picked and why, in a few words.
- Side notes: older problems the code review raised, one line each, for the user to decide on.
- What you did not check.
