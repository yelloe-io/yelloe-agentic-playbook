# Third-party work

Some skills in this repo build on the work of other people. This file names each source and its license. The license files are in this folder.

## Matt Pocock

Source: <https://github.com/mattpocock/skills>, MIT. License: `mattpocock-skills-LICENSE`.

| Skill | Status |
| --- | --- |
| `codebase-design`, `domain-modeling`, `writing-for-agents` | Verbatim, with a small fallback for agents that cannot start subagents in `codebase-design` |
| `grill-me`, `wayfinder`, `to-spec`, `to-issues`, `prototype`, `diagnosing-bugs`, `improve-codebase-architecture`, `handoff`, `wizard`, `retro`, `bro` | Adapted |
| `implement` | Adapted. The short shape comes from his `implement`. The test rules are our own |
| `build-spec` | Our own. The integration branch, the task frontier and the parallel builders come from his `implement-spec` |

`prototype/LOGIC.md` is his text unchanged.

## Emil Kowalski

Source: <https://github.com/emilkowalski/skills>, MIT. License: `emilkowalski-skills-LICENSE`.

`verify/references/layout-breaks.md` and `verify/references/worst-case.md` are adapted from his `break-ui` skill.

## Dex Horthy

Source: the `show-me` skill in <https://github.com/humanlayer/humanlayer>, Apache 2.0. License: `humanlayer-LICENSE`.

The menu of small diagrams in the `pr` skill, for changes with no screen, comes from `show-me`. We changed it to describe a diff instead of a live conversation.

## Ideas without copied text

- `explain-spec` follows an idea by Geoffrey Litt: quiz yourself on a change before it ships.
- `ui-taste` is our own text. Its ideas build on Anthropic `frontend-design` (Apache 2.0, <https://github.com/anthropics/skills>), Impeccable by Paul Bakaus (Apache 2.0, <https://github.com/pbakaus/impeccable>) and the Taste skill by Leonxlnx (MIT, <https://github.com/Leonxlnx/taste-skill>).
- The values in `ui-taste/references/craft.md` are rewritten in our own words from Jakub Krehel's `better-*` skills (MIT, <https://github.com/jakubkrehel/skills>), `scandinavian-design` by Eric Zakariasson, `interface-design` by Dammyjay93, `rad-spacing` by Nolan Perkins, `refactoring-ui` by s0xDk and `smooth-shadow-ring` by flornkm (all on <https://www.ui-skills.com>), and `distill` and `quieter` from Impeccable.
- The teardown method in `ui-taste/references/teardown.md` follows Jakub Krehel's `explain-interface`.
