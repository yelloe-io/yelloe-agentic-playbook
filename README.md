<div align="center">

<img src="assets/duck.png" alt="The yelloe rubber duck" width="160">

# Yelloe Agentic Playbook

**How Yelloe builds software with coding agents.**

</div>

---

This repo holds the skills that Yelloe uses and shares, and the flows that combine them. Some skills are our own. Others build on good work by other people, credited below and in [`third-party/`](third-party/README.md).

Each skill works on its own. A skill can mention another skill as an option, but it never needs it. You combine them, and the flows show how.

Yelloe also runs workshops that teach dev teams to work this way. See [yelloe.io](https://yelloe.io).

## Install

In Claude Code:

```
/plugin marketplace add yelloe-io/yelloe-agentic-playbook
/plugin install yelloe@yelloe-playbook
```

With another agent, or to pick single skills, copy the skill folders you want into your agent's skills folder, such as `~/.claude/skills/` or `~/.agents/skills/`.

## Flows

| Flow | When |
| --- | --- |
| [Implement a big feature from scratch](flows/big-feature.md) | A feature too big for one session, with decisions still open |
| [Work on several issues at once](flows/several-issues.md) | A handful of small, unrelated issues |
| [Ship one issue](flows/one-issue.md) | One issue that one session can finish |
| [Fix a bug](flows/fix-a-bug.md) | Something is broken, throws, fails or is slow |
| [Build UI](flows/build-ui.md) | A new screen or a redesign |
| [Keep the setup sharp](flows/keep-the-setup-sharp.md) | After a bad run, or on a schedule |

## Skills

### Plan

| Skill | What it does | Source |
| --- | --- | --- |
| [`grill-me`](skills/grill-me/SKILL.md) | Interviews you one decision at a time until a plan is sharp. Writes the design point of view for UI work. | Yelloe, from Matt Pocock |
| [`wayfinder`](skills/wayfinder/SKILL.md) | Charts a large, foggy effort as a map of decision tickets and resolves them one at a time. | Yelloe, from Matt Pocock |
| [`to-spec`](skills/to-spec/SKILL.md) | Turns a settled conversation into one spec on the issue tracker. Writes the spec only. | Yelloe, from Matt Pocock |
| [`to-issues`](skills/to-issues/SKILL.md) | Splits a spec or plan into issues that each fit one agent, with the blocking order between them. | Yelloe, from Matt Pocock |
| [`prototype`](skills/prototype/SKILL.md) | Builds a throwaway prototype to answer one design question about logic or UI. | Yelloe, from Matt Pocock |
| [`explain-spec`](skills/explain-spec/SKILL.md) | Quizzes you on a spec before any code exists. | Yelloe |

### Build

| Skill | What it does | Source |
| --- | --- | --- |
| [`implement`](skills/implement/SKILL.md) | Builds one issue or plan with tests that can fail, and checks the result in the running app. | Yelloe, from Matt Pocock |
| [`build-spec`](skills/build-spec/SKILL.md) | Builds a whole spec with parallel agents on one branch, audits the tests, verifies, and hands over one pull request. | Yelloe, from Matt Pocock |
| [`batch`](skills/batch/SKILL.md) | Runs several unrelated issues in parallel, with a blind review of each diff and one pull request per issue. | Yelloe |

### Verify and ship

| Skill | What it does | Source |
| --- | --- | --- |
| [`verify`](skills/verify/SKILL.md) | Proves a change works in the running app with evidence, and probes what it could break. | Yelloe |
| [`test-audit`](skills/test-audit/SKILL.md) | Plants small bugs in the changed lines to prove the tests can fail, and rewrites weak tests. | Yelloe |
| [`before-after`](skills/before-after/SKILL.md) | Captures before and after screenshots or a short video and posts them to the issue or pull request. | Yelloe |
| [`pr`](skills/pr/SKILL.md) | Opens a pull request with a short, picture-first body and a merge-risk call, then watches CI. | Yelloe |

### Fix

| Skill | What it does | Source |
| --- | --- | --- |
| [`diagnosing-bugs`](skills/diagnosing-bugs/SKILL.md) | Finds the cause of a hard bug or a slow path with a fast reproduction, then fixes it with a regression test. | Yelloe, from Matt Pocock |

### Code design

| Skill | What it does | Source |
| --- | --- | --- |
| [`improve-codebase-architecture`](skills/improve-codebase-architecture/SKILL.md) | Finds places where a module can be deeper and reports them as an HTML page. | Yelloe, from Matt Pocock |
| [`codebase-design`](skills/codebase-design/SKILL.md) | Shared vocabulary for designing deep modules and placing seams. | Matt Pocock |
| [`domain-modeling`](skills/domain-modeling/SKILL.md) | Builds the domain glossary and records decisions as ADRs. | Matt Pocock |

### UI

| Skill | What it does | Source |
| --- | --- | --- |
| [`ui-taste`](skills/ui-taste/SKILL.md) | Designs, builds and reviews UI that does not look machine-made. | Yelloe |

### Upkeep

| Skill | What it does | Source |
| --- | --- | --- |
| [`handoff`](skills/handoff/SKILL.md) | Saves the state of a repo for the next session. | Yelloe, from Matt Pocock |
| [`retro`](skills/retro/SKILL.md) | Finds repeated mistakes in past sessions and proposes the strongest fix for each. | Yelloe, from Matt Pocock |
| [`bro`](skills/bro/SKILL.md) | Re-pitches the last message in short, simple words when it did not land. | Yelloe, from Matt Pocock |
| [`wizard`](skills/wizard/SKILL.md) | Writes a bash wizard for steps only a person can do. | Yelloe, from Matt Pocock |
| [`writing-for-agents`](skills/writing-for-agents/SKILL.md) | How to write skills, CLAUDE.md and AGENTS.md for agents. | Matt Pocock |

For deeper UI work, we also recommend [Impeccable](https://github.com/pbakaus/impeccable) by Paul Bakaus and Emil Kowalski's [design engineering skills](https://github.com/emilkowalski/skills).

## What is where

| Path | Contents |
| --- | --- |
| `skills/` | Skills, one folder each, with a `SKILL.md` at its root |
| `flows/` | Scenarios that combine the skills, one page each |
| `tools/` | The tools that we recommend, and how to set them up. Start at [`tools/README.md`](tools/README.md) |
| `third-party/` | Credits and licenses for work by other people |
| `.claude-plugin/` | Plugin and marketplace manifests for Claude Code. The plugin name is `yelloe` |
| `assets/` | Images for the docs |

## Rules

- Do not commit secrets.
- Remove all private data before you commit: client names, customer data, tokens and absolute local paths.
- Keep each skill self-contained. Mention another skill only as an option, with a fallback.
- When you add a skill, add it to the `skills` list in `.claude-plugin/plugin.json` and to the table above.
- When a skill builds on someone else's work, credit it in `third-party/README.md`.

## License

MIT. See [LICENSE](LICENSE). Third-party work keeps its own license, listed in [`third-party/`](third-party/README.md).
