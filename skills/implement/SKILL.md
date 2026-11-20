---
name: implement
description: Implement a piece of work from an issue, a plan or a spec. Reads the code it touches, builds with the project's patterns, tests as it goes, checks the result in the running app and commits. Use when the user asks to implement, build or pick up an issue or plan.
disable-model-invocation: true
---

# Implement

Implement the work that the user describes in the issue, plan or spec.

If the user passes an issue reference, fetch it from the issue tracker and state its title before you start. If the reference is ambiguous, ask.

## Steps

1. **Read.** Read the issue or plan, then the code it touches. Note the acceptance criteria and any seams the plan names. Ask the user only about an open decision that changes the work. Decide the technical details yourself.
2. **Build.** Use the existing patterns of the project: its modules, helpers, UI components and naming. Write tests by the rules in [Tests](#tests). Honor the user's test choice first, then the project's test policy.
3. **Check as you go.** Run the typecheck often, and run the single test files you touch. Run the full test suite once, at the end.
4. **Check the running app.** When the change has runtime behavior, prove it in the running app with direct evidence. Start the app, open the page, endpoint or command, drive the flow that the change affects, and look at the result: the screen, the response or the output. A passing test is not this evidence. When the change has no runtime behavior (types, docs, a refactor that tests cover), skip this step and say why.
5. **Commit** the work to the current branch. Follow the commit conventions in the repo's `CLAUDE.md` or `AGENTS.md`.

Report what you built, the checks you ran with their results, and the runtime evidence.

## When a check fails

**Reproduce first.** Run the smallest reproduction that keeps the failure before you change code. A failure that does not reproduce is not a pass: find what differs in environment, inputs or timing. Fix the cause, not the symptom. Then rerun the reproduction and every check the fix can affect.

After three attempts at the same cause without progress, stop and report: what fails, what you tried, and what you think the cause is.

## Tests

- **Seams.** Test at the seams that the spec names. A seam is a public boundary where you see the behavior from outside. When the spec names no seam, use the public interface nearest to the change and say which one you chose.
- **Shape first.** For a new module, write the types and signatures first.
- **Test first when cheap.** When a test at the seam is cheap, write it first and see it fail. Then write only the code that makes it pass. Before you change code that has no test, write a test that pins the current behavior.
- **Every test can fail.** If you did not see a test fail, break the code it guards for a moment and see the test go red. Take expected values from the spec or a worked example, not from the code under test.
- **Close what you open.** A test that starts a database, a server or a browser stops it in the matching `afterEach` or `afterAll`. Open resources pass on a large machine and stop a small CI machine.
- **Property tests.** When a function has a rule that must hold for every input, such as a round trip or a total that is never negative, add a property test with the property test library of the project. When the project has none, test the edge cases of the rule and report the missing library.

Rewrite a test that has one of the six weak shapes:

1. **Coupled**: it mocks your own modules or calls private methods, so a refactor breaks it when the behavior stays the same. Mock only at system boundaries: external APIs, time, randomness.
2. **Side channel**: it reads the result from the database or a file, not through the interface.
3. **Tautological**: the expected value repeats the calculation of the code, so the test always passes.
4. **Call counting**: it asserts which internal calls occur, or their order, not what the caller sees.
5. **Horizontal**: many tests written before any code. Write one test, then its code, then the next test.
6. **Weak assertion**: its only check is `toBeDefined`, `toBeTruthy` or `not.toThrow`, so almost any result passes. Assert the exact value that the caller sees.

## Optional follow-ups

These are not part of this skill. Offer them when they fit.

- If you have the `test-audit` skill, a fresh agent can use it to prove the new tests can fail.
- If you have the `verify` skill, it can probe the change further in the running app.
