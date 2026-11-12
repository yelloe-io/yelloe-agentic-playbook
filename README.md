<div align="center">

<img src="assets/logo.svg" alt="yelloe" width="240">

# Yelloe Agentic Playbook

**How yelloe builds software with coding agents.**

</div>

---

This repo is the source of truth for the skills that yelloe shares. It holds the skills, the tools
that we recommend, and the modules that teach the thinking behind both.

The repo is a skeleton. The contents are not in yet.

## What is where

| Path | Contents |
| --- | --- |
| `skills/` | Skills, one folder each, with a `SKILL.md` at its root |
| `modules/` | Training modules on how to work with coding agents |
| `tools/` | The tools that we recommend, and how to set them up |
| `.claude-plugin/` | Plugin and marketplace manifests for Claude Code. The plugin name is `yelloe` |
| `assets/` | Images for the docs |

## Rules

- Do not commit secrets.
- Remove all private data before you commit: client names, customer data, tokens and absolute local paths.
- When you add a skill, add it to the `skills` list in `.claude-plugin/plugin.json`.

## License

MIT. See [LICENSE](LICENSE).
