# Verification guide

Verifiers read this file. It gives the record format, the adversarial axes, the evidence rules for UI and APIs, and design review mode.

## The record

Write one JSON record per issue, and one for the cross-issue flows. Create it before you run anything, with every planned check `blocked`, so no check can drop out of coverage. Update each check as evidence arrives. Keep the record and its evidence outside the repo.

```json
{
  "title": "Saved values verification",
  "repo": "example/app",
  "commit": "abc123",
  "issue_url": "https://github.com/example/app/issues/7",
  "criteria": [
    {"id": "AC1", "text": "A saved value survives reload.", "check_ids": ["AC1.reload"]}
  ],
  "checks": [
    {
      "id": "AC1.reload",
      "name": "Reload the saved value",
      "category": "ui",
      "precondition": "A member has saved a changed value",
      "action": "Reload the page",
      "expected": "The saved value remains visible",
      "actual": "Not executed yet",
      "status": "blocked",
      "commit": "abc123",
      "evidence": []
    }
  ],
  "coverage_notes": "Paths walked, combinations chosen, axes that do not apply and why.",
  "observations": "Defects outside the issue, and their relevance.",
  "state_left_behind": "Fixtures, settings, processes, and how to restore them."
}
```

- **Criteria.** Copy every acceptance criterion with its exact wording, including ones already ticked and ones outside the diff. Keep each criterion's planned `check_ids`, even before they run.
- **Checks.** Each check has one precondition, one action and one expected result. Give every named variant its own check. `category` is `ui`, `api`, `database` or `behavior`. `actual` holds the observation or the reason it is blocked. `evidence` holds paths to retained artifacts (screenshots, console and network logs, responses, query output), relative to the record. Adversarial checks can stand alone in `checks`; they still count in the verdict.
- **Statuses.** `pass`: inspected runtime evidence shows the expected result. `fail`: observed behavior contradicts the contract. `blocked`: not run, or evidence, access or a prerequisite is missing. `accepted`: an explicit decision in the spec or issue accepts a limitation; name it in a `decision` field. Pass and fail need nonempty evidence.
- **Derived results.** A criterion takes the worst status of its checks: fail, then blocked, then accepted, then pass. A criterion counts as met, and its box gets ticked, only when all its checks pass. The record's overall result follows the same order over all checks. Never set an overall status by hand.
- **Reuse after a fix.** Rerun the failed checks and every check the fix can affect. Evidence from an earlier commit carries forward only when its code, inputs, fixtures and runtime stay the same. Keep its old `commit` and add `reuse`: the current commit and why the claim is unaffected. Changing a commit label is not verification.

## Adversarial axes

Apply every relevant axis at adversarial depth. Each one generates concrete checks. Note the axes that do not apply in `coverage_notes`; do not invent tests for them. Expected results come from the issue, the agreed design and the project's invariants. When behavior is unspecified and it changes the verdict, report it as a question; do not invent a requirement.

Bound the matrix: walk every relevant axis and every named variant, and add combinations only where the code or the domain couples two axes. Record which combinations you chose and why the others cannot fail on their own.

| Axis | What to try |
| --- | --- |
| State transitions | Legal transitions forward and back, including undo, reopen and repeats. Illegal transitions. Check state and side effects. |
| Live state and reload | Every affected surface, count, badge and derived value after a change. Compare with the state after a reload. |
| Permissions and flags | Each relevant role and tenant on each operation. API enforcement, the intended UI affordance, both flag states, no side effect after a denied write. |
| Deleted or inaccessible targets | Old links, stored references, cached lists, browser history. The designed end state. Honor intended concealment of whether a target exists. |
| Input boundaries | Wrong types, malformed values, long strings, Unicode, markup, search metacharacters, large collections, page boundaries, foreign IDs. Safe rendering and edit round trips. |
| Failure and recovery | Interrupt requests or the backend before, during and after a commit where feasible. Timeouts, kept drafts, retry, partial completion, restart. |
| Known regressions | Each bug fixed during this run, from the issues, commits and builder reports. Repeat its reproduction. |
| Empty and zero states | Empty data, zero children, no search match, a dependency that is down. The designed state and its recovery actions. |
| Concurrency | Double submit, retry after an uncertain response, the same record edited in two sessions. The declared conflict, order and idempotency behavior. |
| Pagination under change | Insert or delete across page boundaries. Check against the declared consistency model. |
| Clock boundaries | Cutoffs, time zones, date changes, in the project's time semantics. |
| Background side effects | Trigger, retry, reset and re-arm work. Observe the real effect and its deduplication. |

For a rejected change, inspect the layer that can reveal an unintended effect. A toast or an error status alone is not enough when state or queued work could still change. Inject faults only with safe fixtures in the test environment. A required probe that cannot run is blocked. A defect outside the issue is an observation, not a reason to widen the work.

## UI paths and evidence

The unit of coverage is a distinct user path, not a screenshot. Walk every control and distinct reachable path in the feature: entry routes, roles, flag states, navigation, submit, cancel, back, undo, retry, reload and reopen. Include loading, empty, validation, permission, error and success states where they apply. Repeat a check on an intermittent symptom at least 10 times and record the count.

- Drive real user interactions in your own browser session. A direct URL visit does not prove a link works. An API success does not prove a form submits.
- Set the expected end state and a timeout before each flow. An endless spinner, a timeout or a handled error in a success case is a fail.
- Capture and inspect screenshots of the relevant states and viewports: layout, clipping, overflow, type, spacing, usable controls. Try worst-case data: very long and one-letter names, long labels, huge counts, empty lists. Text wraps or truncates on purpose, and never pushes controls off screen.
- When the app is used on phones, check a phone viewport: no layout jump, no zoom on input focus, no hover state stuck after a tap, content clear of the notch and the home bar.
- Capture console and network events from before the action to its end state. A new unexplained error, an unhandled rejection, a failed request or a request still pending past the timeout is a fail. Missing observability is blocked.

## API and persistence

- Call the feature endpoints with real authentication and the relevant roles, flags and tenants. Record the request, the status and the fields that prove the result. Try invalid inputs too, not only what the UI can send.
- Compare state before and after the action. Use API reads when they prove the claim, and database, queue or outbox queries for what they cannot show. A denied write leaves no record and no side effect.
- Reload or restart when persistence is the claim. For a migration or backfill, compare snapshots after a first and a second run.
- Keep a ledger of the fixtures, flags, settings and processes you change, with how to restore them. Restore task-owned fixtures at the end. Keep secrets and personal data out of evidence.

## Design review

In design review mode you review the look and feel of the whole change, not the acceptance lines.

1. Read the design target and the repo's design doc, if it has one. Find the pages the change reaches: a changed file reaches each page that renders it, and a changed token or shared component reaches every page that uses it. Review up to 8 and name the ones you left out.
2. Load realistic data: as many rows as real use has, long and one-letter names, long labels, big numbers, empty lists.
3. Walk each page with the mouse at a desktop width and a phone width. Open and close each menu, dialog and dropdown. For each page, check: the target (put your screenshot next to the target; each difference in layout, order, density, words or emphasis is a finding unless the spec approves it), the eye (the most important thing is the most visible), one app (each component looks the same on every page), sync (a value shown in two places updates in both), and states (loading, empty, error and lots of data look intended).
4. Read the removed lines of the diff. A removed style, state or label that nothing replaces is a regression.
5. Write the findings to one Markdown file outside the repo. Mark each finding `Introduced`, `Regression` or `Pre-existing`. Give each Introduced and Regression finding its page, a screenshot pair and a specific fix. List at most 3 Pre-existing ones. End with the 2 or 3 places where a person must judge the result, each with its address and click path.
