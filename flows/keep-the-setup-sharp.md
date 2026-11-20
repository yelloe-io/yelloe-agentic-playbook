# Keep the setup sharp

Use this flow after a run that went badly, or on a regular schedule. Agents repeat the mistakes that their environment allows. Fix the environment, not the agent.

## The steps

1. **Look back.** Run `retro` on a session or a run. It finds the mistakes that happened more than once.
2. **Pick the strongest fix.** For each repeated mistake, `retro` proposes a fix at the strongest level that works. In order, that is a change to the code structure, a type, a lint rule or hook, a test, and last a written rule. A written rule is the weakest, because an agent can skip it.
3. **Approve and build.** You approve each fix. Build each one as its own small pull request.
4. **Keep the instructions lean.** When a check now catches a mistake every time, remove the written rule for it from `CLAUDE.md` or `AGENTS.md`. Use `writing-for-agents` when you edit those files or a skill.

## Tips

- Run `handoff` before you end a long session, so that the next session starts from the real state.
