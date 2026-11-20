---
name: improve-codebase-architecture
description: Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. Use when the user wants to improve the architecture, find refactoring or deepening opportunities, or make a codebase easier to test and navigate.
disable-model-invocation: true
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

This command is _informed_ by the project's domain model and built on a shared design vocabulary:

- Use the architecture vocabulary and its principles. If you have the `codebase-design` skill, load it for the full glossary. Otherwise, use these short forms:
  - **Module**: anything with an interface and an implementation, at any scale.
  - **Interface**: everything a caller must know to use the module: types, invariants, ordering, error modes, config.
  - **Depth**: behaviour a caller gets per unit of interface. **Deep** means a lot of behaviour behind a small interface; **shallow** means the interface is nearly as complex as the implementation.
  - **Seam**: the place where a module's interface lives, where behaviour can change without editing in place.
  - **Adapter**: a concrete thing that satisfies an interface at a seam.
  - **Leverage**: what callers get from depth. **Locality**: what maintainers get: change and bugs concentrate in one place.
  - Principles: the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real".

  Use these terms exactly in every suggestion, and don't drift into "component," "service," "API," or "boundary."
- The domain language in `GLOSSARY.md` gives names to good seams; ADRs in `docs/adr/` record decisions this command should not re-litigate.

## Process

### 1. Explore

**Scope before you scan: YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed. Decide *where* to look before you look:

- If the user named a direction (a module, a subsystem, a pain point), take it, and skip the inference below.
- Otherwise, walk back a good stretch of the commit history (`git log --oneline`) to find the codebase's hot spots, the files and areas that keep coming up, and let those paths pull your attention first. If the changes are scattered with no clear hot spot, widen the net.

Read the project's domain glossary (`GLOSSARY.md`) and any ADRs in the area you're touching first.

Then spawn a sub-agent with a fresh context window to walk the codebase (in Claude Code, start it at high effort; without sub-agents, walk it yourself). Don't follow rigid heuristics; explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Ask one question of every pair of pieces: **should these change together?** The code gets the answer wrong in three ways:

- **Hidden links:** pieces that must change together, where the code does not show it. Copied logic or values, a module that reads a global another module sets, one feature split across folders by layer, a call order that callers must just know.
- **Needless links:** pieces tied together that change for different reasons. Callers that depend on internals, stable code that imports more volatile code, a general function with a parameter that only one workflow understands.
- **Surplus:** pieces with no reason of their own to change. Pass-through wrappers, config and extension points for things that never vary, dead code.

Also list each **special case**: an `if` for one value, a parameter for one caller, a swallowed exception, a retry or a sleep, a disabled test. Each one is a requirement the design never took in. Look for the one fix behind several special cases, and count the special cases that each candidate removes.

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory, so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/architecture-review-<YYYY-MM-DD>-<slug>.html`. Open it for the user (`xdg-open <path>` on Linux, `open <path>` on macOS, `start <path>` on Windows) and tell them the absolute path.

The report is a single self-contained HTML file: no CDNs, no external fonts, no network. Inline [assets/report.css](assets/report.css) into its `<style>` tag. Diagrams are hand-built: inline SVG when relationships are graph-shaped (call graphs, dependencies, sequences), positioned divs and SVG when you want something more editorial (mass diagrams, cross-sections, collapse animations). Each candidate gets a **before/after visualisation**. Be visual.

For each candidate, render a card with:

- **Files**: which files/modules are involved
- **Problem**: why the current architecture is causing friction
- **Solution**: plain English description of what would change
- **Benefits**: explained in terms of locality and leverage, and how tests would improve
- **Special cases removed**: the count, with file and line for each
- **Before / After diagram**: side-by-side, custom-drawn, illustrating the shallowness and the deepening
- **Recommendation strength**: one of `Strong`, `Worth exploring`, `Speculative`, rendered as a badge

End the report with a **Top recommendation** section: which candidate you'd tackle first and why.

**Use GLOSSARY.md vocabulary for the domain, and the architecture vocabulary above for the architecture.** If `GLOSSARY.md` defines "Order," talk about "the Order intake module," not "the FooBarHandler," and not "the Order service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the card (e.g. a warning callout: _"contradicts ADR-0007, but worth reopening because…"_). Don't list every theoretical refactor an ADR forbids.

See [HTML-REPORT.md](HTML-REPORT.md) for the full HTML scaffold, diagram patterns, and styling guidance.

Do NOT propose interfaces yet. After the file is written, ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, walk the decision tree with them: constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive. If you have a grilling skill, use it. Otherwise ask one question at a time, give your recommended answer with each, and settle each branch before you open the next.

Side effects happen inline as decisions crystallize. Keep the domain model current as you go (the `domain-modeling` skill, if you have it, holds the glossary and ADR formats):

- **Naming a deepened module after a concept not in `GLOSSARY.md`?** Add the term to `GLOSSARY.md`. Create the file lazily if it doesn't exist.
- **Sharpening a fuzzy term during the conversation?** Update `GLOSSARY.md` right there.
- **User rejects the candidate with a load-bearing reason?** Note it in the report so the next architecture pass does not re-suggest the same thing. Do not write it anywhere durable: recording decisions is not this skill's job.
- **Want to explore alternative interfaces for the deepened module?** Design it twice: dispatch parallel sub-agents to draft radically different interfaces, then compare them on depth, locality and seam placement, and recommend one. In Claude Code, start them at high effort. If you have the `codebase-design` skill, follow its design-it-twice pattern.
