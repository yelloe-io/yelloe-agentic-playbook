# Implement a big feature from scratch

Use this flow when a feature is too big for one session: several issues, new modules, and decisions that are not made yet.

## The steps

1. **Find the way.** Run `wayfinder` when the work is foggy and spans many sessions. It charts the open decisions as tickets and resolves them one at a time. When the way is already clear, run `grill-me` instead. It interviews you until each decision is made.
2. **Write the spec.** Run `to-spec`. It turns the decisions into one spec with acceptance criteria, and does nothing else. Skip this step after `wayfinder`: its last step already writes the spec.
3. **Split the spec.** Run `to-issues`. It breaks the spec into issues that each fit one agent, with the blocking order between them.
4. **Check that you understand it.** Run `explain-spec`. It quizzes you on the spec before any code exists. A wrong answer is a cheap place to find a gap.
5. **Build it.** Run `build-spec`. Parallel agents build the issues on one shared branch. The skill audits the tests, checks each issue in the running app, and hands over one pull request.
6. **Review and merge.** Read the pull request and its report. Answer each parked question. The agent never merges: you do.

## Tips

- Questions about what the user sees, or about scope, get parked, not guessed. Answer them, then run `build-spec` again on the parked issues.
- A bad spec makes a bad build. Most of the time goes into steps 1 to 4.
