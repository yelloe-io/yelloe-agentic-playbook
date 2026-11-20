---
name: test-audit
description: Audit the tests of a change you did not write. Runs mutation testing on the changed lines, rewrites weak tests, adds tests that kill surviving mutants and commits the fixes. Use after a change is built, when asked to audit tests, check test quality or run mutation testing on a branch or diff.
---

# Test audit

You audit the tests of a change that you did not write. Judge it as a stranger. Your job is to prove that its tests can fail. You fix what you find, commit the fixes, and report what remains.

Run in a fresh agent, not in the session that wrote the change. If you are that session, start a subagent with these instructions when your tool supports it. Otherwise ask the user to run the skill in a new session.

## Input

- A branch or a diff, and its base commit or branch. When the user gives no base, use the merge base with the default branch and say so.
- Whether commits are on hold. The default is to commit.

The user can run this skill directly, or another skill or agent can start it with the same input.

## Steps

1. **Read.** Read `AGENTS.md` and `CLAUDE.md` where they exist for the test, typecheck and lint commands. When the repo has neither, find the commands in `package.json` scripts or `pyproject.toml`, and report the missing file as a gap. Read the diff with `git diff <base>...HEAD`, plus uncommitted and new files. List the changed source files and the changed test files.
2. **Mutation testing.** Follow [Mutation testing](#mutation-testing). The step is done when each mutant on a changed line is killed or is on your survivor list with a reason.
3. **Weak tests.** Check each new or changed test against [the six weak shapes](#weak-tests). Also apply the **undefined** rule: if the test still passes when every function it imports returns `undefined`, it cannot fail. Rewrite each weak test, or delete it when the behavior has another test. Then search the changed test files for a database, a server or a browser that a test opens and does not close, and add the close in the matching `afterEach` or `afterAll`.
4. **Gate.** Run the tests related to your changes, the typecheck and the lint. Read only the failures. Fix until all pass. Then run the full test suite once, unless the caller says it runs the suite itself.
5. **Commit.** Commit your fixes on the branch, with a clear message that says they come from the test audit. Follow the repo's commit conventions. When commits are on hold, leave the fixes uncommitted and list the files.
6. **Report**, under 200 words:
   - The mutation result: killed out of total on changed lines. With no tool, write "no mutation tool set up" and the result of the planted mutants.
   - Each test you added, rewrote or deleted.
   - Each remaining survivor: file, line, the mutant, and a one-line reason.
   - Each unclosed resource you closed.
   - The commits, or the uncommitted files.

## Mutation testing

A **mutant** is a copy of the code with one small change, such as `<` to `<=`. A test **kills** the mutant when it fails on that copy. A **survivor** is a mutant that every test passes. Each survivor on a changed line is a gap in the tests.

In this step, the source files are frozen. You add and change tests only. A mutant dies through a new test, never through a source edit.

1. **Find the tool.** StrykerJS for TypeScript and JavaScript: a `stryker.config.*` file, or `@stryker-mutator/core` in `package.json`. mutmut for Python: `[tool.mutmut]` in `pyproject.toml`, `[mutmut]` in `setup.cfg`, or `mutmut` in the dev dependencies. When the project has no tool set up, do not install one. Plant mutants by hand instead:
   1. In the changed source lines, make 2 or 3 mutants, one at a time. Flip a comparison, drop a branch, or change a constant.
   2. Run the tests that cover the mutated file on each mutant, then undo your edit. Do not use `git checkout` for this, because the file can hold uncommitted work. Never commit a planted mutant.
   3. Treat a mutant that every test passes as a survivor, and go on with step 3 below. Do step 4 by hand: plant the same mutant again, run the tests, and revert.
2. **Run on the changed code only.**
   - StrykerJS: turn each changed hunk into a range, then run `npx stryker run --reporters json,clear-text --mutate "src/a.ts:5-7,src/b.ts:10-22"`. Add `--incremental` when the project uses it. Survivors have `status: "Survived"` in the JSON report.
   - mutmut: run `mutmut run "<module>.<function>*"` for each changed function. List the survivors with `mutmut results`. Print each mutant diff with `mutmut show <name>`.
3. **For each survivor**, read the mutant diff. Then do one of these:
   - When no caller can see a difference, the mutant is **equivalent**. Put it on the survivor list with the reason.
   - Otherwise, write one test at the seam that the spec names, or at the public interface nearest to the change. The test must pass on the original code. Take the expected value from the spec, not from the code.
4. **Rerun only that mutant.** StrykerJS: `npx stryker run --incremental --force --mutate "<file>:<line>"`. mutmut: `mutmut run <name>`. Keep the test when the mutant dies. When it survives again, improve the test once. Then put the mutant on the survivor list with the reason.
5. **Check each new test** with the undefined rule from step 3 of Steps. A test that pins a constant kills a mutant but protects nothing.

## Weak tests

A test with one of these six shapes is weak. Rewrite it so it checks what the caller sees.

1. **Coupled**: it mocks the project's own modules or calls private methods, so a refactor breaks it when the behavior stays the same. Mock only at system boundaries: external APIs, time, randomness.
2. **Side channel**: it reads the result from the database or a file, not through the interface.
3. **Tautological**: the expected value repeats the calculation of the code, so the test always passes.
4. **Call counting**: it asserts which internal calls occur, or their order, not what the caller sees.
5. **Horizontal**: many tests written before any code, so none of them was seen to fail on its own. Check that each one fails when the code it guards breaks.
6. **Weak assertion**: its only check is `toBeDefined`, `toBeTruthy` or `not.toThrow`, so almost any result passes. Assert the exact value that the caller sees.
