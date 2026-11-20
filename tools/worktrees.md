# Worktrees

A worktree is a second folder for the same repo, checked out on another branch. Give each agent its own, and several agents can work at once without overwriting each other's files. `batch` and `build-spec` depend on them.

## Commands

```bash
git worktree add ../myrepo-worktrees/42-fix-login -b 42-fix-login
git worktree list
git worktree remove ../myrepo-worktrees/42-fix-login
```

Keep them in one sibling folder, one folder per branch, so they never end up inside the repo.

## In Claude Code

- `claude --worktree <name>` starts a session in a new worktree.
- A subagent started with worktree isolation gets a temporary worktree of its own.

## Gotchas

- Each worktree needs its own install, such as `npm install`, and its own copy of untracked files like `.env`.
- Two dev servers cannot share a port. Give each worktree its own.
- A branch can be checked out in only one worktree at a time.
- On Windows, deep paths can pass the length limit. `git config --global core.longpaths true` fixes it.
