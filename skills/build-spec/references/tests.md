# Test rules

Builders write tests by these rules. The test auditor checks the whole branch against them.

## Writing tests

- **Seams.** Test at the seams that the spec names. A seam is a public boundary where you see the behavior from outside. When the spec names no seam, use the public interface nearest to the change and say which one you chose.
- **Shape first.** For a new module, write the types and signatures first.
- **Test first when cheap.** When a test at the seam is cheap, write it first and see it fail. Then write only the code that makes it pass. Before you change code that has no test, write a test that pins the current behavior.
- **Every test can fail.** When you did not see a test fail, break the code it guards for a moment and see the test go red. Take expected values from the spec or a worked example, not from the code under test.
- **Close what you open.** A test that starts a database, a server or a browser stops it in the matching `afterEach` or `afterAll`, or the project's equivalent. Open resources pass on a large machine and stall a small CI machine.
- **Property tests.** When a function has a rule that must hold for every input, such as a round trip or a total that is never negative, add a property test with the project's property test library. When the project has none, test the edge cases of the rule and report the missing library.

## Weak tests

Rewrite a test that has one of these six shapes:

1. **Coupled:** it mocks your own modules or calls private methods, so a refactor breaks it while the behavior stays the same. Mock only at system boundaries: external APIs, time, randomness.
2. **Side channel:** it reads the result from the database or a file, not through the interface.
3. **Tautological:** the expected value repeats the calculation of the code, so the test always passes.
4. **Call counting:** it asserts which internal calls occur, or their order, not what the caller sees.
5. **Horizontal:** many tests written before any code. Write one test, then its code, then the next test.
6. **Weak assertion:** its only check is `toBeDefined`, `toBeTruthy`, `not.toThrow` or the like, so almost any result passes. Assert the exact value the caller sees.

**The undefined rule:** when a test still passes with every function it imports returning `undefined` (or the language's empty value), it cannot fail. A test that pins a constant can kill a mutant and still protect nothing.

## Mutation testing

A **mutant** is a copy of the code with one small change, such as `<` to `<=`. A test **kills** the mutant when it fails on that copy. A **survivor** is a mutant that every test passes. Each survivor on a changed line is a gap in the tests. During mutation testing the source files are frozen: a mutant dies through a new test, never through a source edit.

1. **Find the tool.** StrykerJS for TypeScript and JavaScript: a `stryker.config.*` file, or `@stryker-mutator/core` in `package.json`. mutmut for Python: `[tool.mutmut]` in `pyproject.toml`, `[mutmut]` in `setup.cfg`, or `mutmut` in the dev dependencies. When the project has no tool set up, do not install one. Plant 2 or 3 mutants per changed source file by hand, as the test audit brief says.
2. **Run on the changed code only.**
   - StrykerJS: turn each changed hunk into a range, then run `npx stryker run --reporters json,clear-text --mutate "src/a.ts:5-7,src/b.ts:10-22"`. Add `--incremental` when the project uses it. Survivors have `status: "Survived"` in the JSON report.
   - mutmut: run `mutmut run "<module>.<function>*"` for each changed function. List the survivors with `mutmut results` and print each diff with `mutmut show <name>`.
3. **For each survivor**, read the mutant diff. When no caller can see a difference, the mutant is **equivalent**: list it with the reason. Otherwise write one test at the seam the spec names, or at the public interface nearest to the change. It must pass on the original code. Take the expected value from the spec, not from the code.
4. **Rerun only that mutant.** StrykerJS: `npx stryker run --incremental --force --mutate "<file>:<line>"`. mutmut: `mutmut run <name>`. By hand: plant the same mutant again, run the tests, and undo it. Keep the test when the mutant dies. When it survives, improve the test once, then list the mutant with the reason.
5. **Check each new test** with the undefined rule.

Report the result as killed out of total on changed lines. With no tool, write "no mutation tool set up" and the result of the planted mutants.
