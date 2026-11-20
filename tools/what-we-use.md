# What we use

Our picks as of November 2026. Tools in this space change fast, so check the date before you copy a pick.

| For | We use | Why |
| --- | --- | --- |
| Agent | Claude Code | The skills are written and tested in it. They also work in other agents that read skills. |
| Everyday model | Opus at medium effort | Good enough for most work, and fast. |
| Hard problems | Fable at high effort | Worth the cost for a big plan, a nasty bug or a design decision. |
| Permission mode | Auto | The agent runs routine steps on its own and asks before risky ones. |
| GitHub | The `gh` CLI | Agents already know it, and it costs less context than an MCP server. |
| Browser | `playwright-cli` | The agent reads a page snapshot only when it asks for one, so long runs stay cheap. |
| MCP servers | None by default | We reach for a CLI first and add a server only when no CLI does the job. |
| Parallel work | Git worktrees | Each agent gets its own folder and branch, so they never trip over each other. |
| More skills | [Matt Pocock's skills](https://github.com/mattpocock/skills), [Impeccable](https://github.com/pbakaus/impeccable), [Emil Kowalski's skills](https://github.com/emilkowalski/skills) | Planning and code design, UI design, and UI polish. |
