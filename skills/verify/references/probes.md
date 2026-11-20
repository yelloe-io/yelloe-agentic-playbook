# Probes

Pick the axes that this diff could plausibly break, and plan one probe per axis. **The oracle comes from the contract**: the issue, the agreed design, and the project's invariants set the expected result. The current implementation is the thing under test, not the oracle. When the contract is silent and the answer changes the verdict, report the question instead of inventing a requirement.

| Axis | What to try |
| --- | --- |
| State transitions | Walk legal transitions forward and backward, including undo, reopen, and repeats. Try an illegal transition. Check state and side effects. |
| Live state and reload | After a mutation, inspect every affected surface, count, badge, and derived value. Compare with the state after a reload. |
| Permissions and flags | Exercise the relevant roles against each operation. Check API enforcement, the UI affordance, both flag states, and no side effects after a denied write. |
| Rendered values | When the change shows data on screen, seed realistic worst-case records and screenshot them, per [worst-case data](worst-case.md). |
| Deleted or inaccessible targets | Follow surviving links, stored references, cached lists, and browser history to a deleted target. Check the designed end state. |
| Input boundaries | Wrong types, malformed values, long strings, Unicode, markup, search metacharacters, large collections, pagination edges, and foreign IDs. Check validation, safe rendering, and edit round trips. |
| Failure and recovery | Interrupt a request or the backend before, during, and after the work. Check timeout, draft preservation, retry, and partial completion. |
| Known regressions | Repeat the reproduction of each bug fixed during this change. |
| Empty and zero states | Empty datasets, zero children, no search matches, an unavailable dependency. Check the designed state and its recovery actions. |
| Concurrency | Double-submit, retry after an uncertain response, edit one record from two sessions. Check conflict, ordering, and idempotency. |
| Pagination under mutation | Insert or delete across a page boundary. |
| Clock boundaries | Cross cutoffs, timezones, and date transitions. |
| Background side effects | Trigger, retry, and re-arm background work. Observe the actual effects and deduplication. |

For a rejected mutation, inspect the layer that can show an unintended effect. An error message or an HTTP rejection alone does not prove that state and queued work stayed unchanged.
