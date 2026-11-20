# Work on several issues at once

Use this flow when you have a handful of unrelated issues, each small and clear enough for one agent to finish alone.

## The steps

1. **Make the issues ready.** Each issue needs a clear problem and a known intent. Run `to-issues` when the work is still one plan, or `grill-me` on an issue that still has an open question.
2. **Run the batch.** Run `batch` with the issues. It starts one worker per issue, each in its own copy of the repo. A separate reviewer reads each diff without the worker's reasoning. After three failed reviews, the worker steps back and rethinks its approach instead of patching.
3. **Read the round report.** Once a round ends, the batch tests the finished branches together, because two branches can each pass and still break the main branch once both are merged. You get one report per round, then one pull request per issue.
4. **Review and merge each pull request.** Answer each question the batch raises. The agent never merges.

## Tips

- Leave out umbrella issues and features that still need a product decision. They stall a worker.
- For one big feature, use the big-feature flow instead: its issues share code and land as one pull request.
