# Fix a bug

Use this flow when something is broken, throws, fails or is slow.

## The steps

1. **Find the cause and fix it.** Run `diagnosing-bugs`. It builds a fast way to reproduce the bug, narrows down the cause with evidence instead of guesses, then writes a test that fails on the bug and fixes the cause.
2. **Hand off a big fix.** When the fix is larger than one change, stop after the cause is known and run `implement` with it. Write the test that reproduces the bug first, and see it fail.
3. **Look for the same bug elsewhere.** Name the pattern that caused the bug and search the codebase for other places with the same pattern.
4. **Verify and ship.** Run `verify`, then `pr`.

## Tips

- When the same kind of bug keeps coming back, run `retro`. It proposes a guardrail, such as a type, a lint rule or a test, so that the next agent cannot repeat the mistake.
