# Rare cases

Most runs do not reach these. Read only the part your case needs.

## Reruns

A `Run: r2` line marks a second run, for example for parked issues. It starts from the trunk, not from the old pull request. Add the suffix to each branch and worktree name of the run: `integrate/<slug>-r2`, `issue/<N>-<slug>-r2`, `../<repo>-issue-<N>-r2`.

## Fix run

A `Fix:` list brings findings on a pull request that was already handed over, from a review or from the user. Read the run log in the `build-spec run log` comment of that pull request. Mark the pull request as draft. Add the integration worktree again and install the dependencies. For each finding, follow Verify steps 4 and 5: the builder branch or a fixer, the merge, the gates, and a fresh verifier on the affected checks. Then do Hand over again.

## No push

When you cannot push, work on local branches only. Keep the run log in a file outside the repo and write its path in the report. Tell each agent to use the local branch where its brief says `origin/`, and not to push. Run `wait.sh` with `-r refs/heads`. At the hand-over, write the pull request body to a file beside the log, and skip each step that needs the remote.

## The fixer brief

For a failure that no builder owns, or for code review findings. Same shape as the builder brief, with no issue:

```
You are the fixer in a build-spec run.
Integration branch: integrate/<slug>. Worktree: <path>. Dev server port: <port>.
Browser session: <repo>-<slug>-fix.
Narrow checks: <commands>. Test rules: <this skill folder>/references/tests.md.
To fix: <the failures or findings, with file and line, steps to reproduce and evidence>.

1. In the worktree, create branch fix/<slug>-<topic> from origin/integrate/<slug>.
2. Reproduce each failure first. When it does not reproduce, report the difference
   in environment or timing; do not patch on a guess. Capture each failure in a
   regression test at a public seam when the tests can express it. Fix the cause.
   Ask the orchestrator when a fix would change what a user sees. Do not start agents.
3. Run the narrow checks on the files you changed. Do not run the full test suite.
   After three attempts at one cause with no progress, stop and report it.
4. Close your browser session. Commit, push your branch, and report: branch, last commit,
   what you fixed, what you left and why.
```
