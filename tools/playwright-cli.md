# Playwright CLI

`verify` and `before-after` drive a real browser to prove a change works. They use `playwright-cli`, a command-line browser that agents call one step at a time.

## Set up

```bash
npm install -g @playwright/cli@latest
playwright-cli open https://example.com
playwright-cli snapshot
playwright-cli close
```

If the project already has Playwright, `npx playwright cli` works without a global install.

## Why a CLI and not an MCP server

The agent asks for a page snapshot only when it needs one, so a long check does not fill the context with every page. A browser MCP server works too, and the skills say how to use one, but it tends to cost more context per step.

## Tips

- Sign in once and save it: `playwright-cli state-save auth.json`, then `state-load` it on later runs. Keep that file out of git.
- Give each agent its own session with `-s=<name>`, so parallel agents do not share a browser.
- Read errors after each flow with `playwright-cli console error` and `playwright-cli requests`. A page can look right and still throw.
