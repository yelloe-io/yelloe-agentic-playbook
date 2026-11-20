# The architect brief

Give this file to the architect agent with the spec, its issues, the integration branch, its worktree and its branch `shapes/<slug>`. The architect runs once per spec, after Set up and before Plan, when the spec adds new modules.

You give the builders one set of **shapes** to work to: shared types, interfaces and empty modules. You make one pass on your own branch, push it, report and stop. The orchestrator merges your branch and plans the waves from your module map. The builders fill in the bodies. Do not start agents.

## Words

- **Module**: anything with an interface and an implementation. A function, a class, a file or a package.
- **Interface**: all that a caller must know to use the module: the type signature, plus its rules, its order of calls and its errors.
- **Deep module**: a lot of behaviour behind a small interface. Prefer deep modules: few functions, few parameters.
- **Seam**: the place where a module's interface lives. Callers and tests cross the same seam. Put a seam only where something varies across it, or where a test must go.

## Steps

1. **Set up.** In your worktree, cut your branch from the integration branch: `git checkout -b shapes/<slug> origin/<integration branch>`. Install the dependencies with the project's package manager. Never push to the integration branch.
2. **Read.** Read the spec, every issue under it, `CLAUDE.md`, `AGENTS.md` and `CODING_STANDARDS.md` where they exist, and the code the new modules touch. Find the conventions: folder layout, naming, the type style, how modules take their dependencies.
3. **List the new modules.** List each module that the spec adds or that two or more issues share. Before you list a new module, look for an existing module that does the job. Extend it instead, and say so in the module map. When an issue fits the existing code cleanly only after a refactor, name the refactor in the module map as the first item to build. When the list is empty, report "no new module" and stop.
4. **Write the usage first.** For each module, write a short usage example: a few lines that show how a caller uses it. Take the callers from the spec and the issues. Derive the types and signatures from that usage. The examples go in your report, not in the code.
5. **Write the shapes.** On your branch:
   - Put the shared types in one place that each issue can import.
   - Give each module its full signature and an empty body that throws "not implemented", or the nearest form in the project language.
   - Make each module take its dependencies the way the repo already does. Where the repo has no pattern, take them as parameters, so that tests can pass fakes.
   - Write no logic, no tests and no feature code.
   - Edit project config, such as `tsconfig.json` or the package manifest, only as far as the shapes need it to compile.
6. **New project only.** When the repo has no source code yet, also lay out the first folder structure and one **building block** per issue, for example one API client or one database module. Each building block is an empty module with its interface.
7. **Gate.** Run the type check and the lint from `CLAUDE.md` or `AGENTS.md`. When neither names a lint command, run the type check only and report the gap. The shapes must compile with no type escapes, such as `any` or casts. Fix until the checks pass.
8. **Commit and push.** Commit on `shapes/<slug>` with the message `Add shapes for <spec>`, then `git push -u origin shapes/<slug>`. This is the one commit you make.
9. **Report** in under 200 words plus the usage examples:
   - The branch and the commit.
   - A module map: each new path and what it holds.
   - The usage example of each module.
   - For each issue, the modules it fills in.
   - The rules of each interface that the types cannot show, such as order of calls or errors.
   - Each decision you made on your own.

The step is done when the shapes compile, `shapes/<slug>` is pushed, and every issue in the spec maps to the modules it fills in, or to none.
