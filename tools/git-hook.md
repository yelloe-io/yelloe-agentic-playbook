# A starter git hook

[`pre-commit`](pre-commit) is a starter, not a finished guard. It blocks a commit that adds a `.env` file or a line that looks like a key. Copy it, then grow it with the mistakes your own agents repeat.

A hook catches a mistake every time, and a written rule in `CLAUDE.md` only asks. When an agent keeps making the same mistake, a hook is often the cheapest strong fix. See [keep the setup sharp](../flows/keep-the-setup-sharp.md).

## Set up

```bash
mkdir -p .githooks
cp pre-commit .githooks/pre-commit
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
```

Commit `.githooks/` so the team shares it. Each clone runs the `git config` line once.

## Grow it

- Add one check per repeated mistake, with an error message that says how to fix it. The agent reads that message and fixes it on its own.
- Keep it fast. A slow hook gets skipped.
- An agent can skip hooks with `--no-verify`. Deny that in your Claude Code permissions, and run the same checks in CI as the real safety net.
