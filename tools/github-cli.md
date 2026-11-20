# GitHub CLI

The skills open issues, open pull requests and read CI logs through `gh`. Agents already know it well, so it needs no extra instructions.

## Set up

1. Install it: `winget install GitHub.cli` on Windows, `brew install gh` on a Mac, or see [cli.github.com](https://cli.github.com).
2. Sign in: `gh auth login`.
3. Check: `gh auth status` lists your account and its scopes.

With several accounts, sign in to each one and pick the active one with `gh auth switch`. A push that fails with a 403 usually means the wrong account is active.

## What the skills run

| Command | Used for |
| --- | --- |
| `gh issue create --body-file <file>` | Writing a spec or an issue |
| `gh pr create --body-file <file>` | Opening a pull request |
| `gh pr checks <pr> --watch` | Waiting for CI |
| `gh run view <run> --log-failed` | Reading why CI failed |

The skills pass long text as a file with `--body-file` rather than inline, because quotes and newlines break in the shell, most of all on Windows.
