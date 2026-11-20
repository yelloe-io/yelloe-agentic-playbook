# Claude Code

Install it with the steps in the [Claude Code docs](https://code.claude.com/docs). The rest of this page is what to set once it runs.

## Settings files

| File | Scope |
| --- | --- |
| `~/.claude/settings.json` | You, in every project |
| `.claude/settings.json` | The project, committed and shared with the team |
| `.claude/settings.local.json` | You, in this project only, kept out of git |

Put team rules in the project file and personal taste in your own, so a teammate's preferences never surprise you.

## Instruction files

| File | Scope |
| --- | --- |
| `~/.claude/CLAUDE.md` | You, in every project |
| `CLAUDE.md` at the repo root | The project, committed |
| `CLAUDE.local.md` at the repo root | You, in this project only, kept out of git |

Keep them short. Every line costs context in every session, and a rule that a test or a hook can enforce belongs there instead. The [keep the setup sharp](../flows/keep-the-setup-sharp.md) flow shows how to move rules out. Use `writing-for-agents` when you edit them.

## Permissions

Allow the commands you run all day and deny the ones you never want an agent to run:

```json
{
  "permissions": {
    "allow": ["Bash(npm test:*)", "Bash(npm run lint:*)", "Bash(git status)", "Bash(gh pr view:*)"],
    "deny": ["Bash(git push --force:*)", "Read(./.env)"]
  }
}
```

A short allow list saves you from clicking yes all day. A deny list is a hard stop that no prompt can talk the agent past.

## Modes

Shift+Tab cycles through them during a session, and `permissions.defaultMode` sets the one a session starts in.

| Mode | When |
| --- | --- |
| `default` | You want to approve each new kind of action |
| `acceptEdits` | You trust file edits but still want to approve commands |
| `plan` | The agent should read and propose, not change anything |
| `auto` | Everyday work: routine steps run, risky ones still ask |
| `bypassPermissions` | Only inside a throwaway container or VM |

## Model and effort

Set them for a session with `/model` and `/effort`, or as defaults with `model` and `effortLevel` in your settings. Start at medium effort and raise it for a hard plan or a stubborn bug. Higher effort is slower and costs more, so it does not pay off on routine work.

## Status line

A status line shows the model, the repo and how full the context window is, so you see a long session filling up before quality drops. Claude Code runs a command of your choice and passes it the session as JSON:

```json
{
  "statusLine": { "type": "command", "command": "bash ~/.claude/statusline.sh" }
}
```

```bash
#!/usr/bin/env bash
input=$(cat)
model=$(echo "$input" | jq -r '.model.display_name')
dir=$(basename "$(echo "$input" | jq -r '.workspace.current_dir')")
ctx=$(echo "$input" | jq -r '.context_window.used_percentage // 0 | floor')
echo "$model | $dir | context $ctx%"
```

It needs `jq`. Run `/statusline` to have Claude Code write one for you instead.

## Other agents

Codex reads `AGENTS.md` instead of `CLAUDE.md`, and keeps its settings, approval policy and sandbox in `~/.codex/config.toml`. The same advice holds: short instructions, a few allowed commands, and the riskiest actions blocked.
