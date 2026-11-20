# Ship one issue

Use this flow for a single issue that one session can finish.

## The steps

1. **Build it.** Run `implement` on the issue. It reads the code first, builds with the patterns that are already there, tests at the public boundary, and checks the change in the running app.
2. **Audit the tests.** For code with real logic, such as money, permissions or data changes, run `test-audit` in a fresh session. It plants small bugs in the changed lines and checks that a test catches each one. The agent that wrote the code is a poor judge of its own tests.
3. **Verify.** Run `verify`. It proves the change works in the running app with evidence and probes what the change could break.
4. **Show it.** For a visible change, run `before-after` to capture screenshots or a short video.
5. **Open the pull request.** Run `pr`. It writes a short body that shows the change, proves it and calls the merge risk, then watches the CI checks.
