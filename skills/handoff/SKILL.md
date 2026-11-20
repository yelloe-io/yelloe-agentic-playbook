---
name: handoff
description: Save the state of a repo for the next session in a lean handoff file and a session ledger. Use when the user says "handoff", "update the docs" or "wrap up", when a milestone lands, or when the context window is about 40% full.
argument-hint: "What will the next session be used for?"
---

# Handoff

You write the state of the repo so that a fresh agent can continue the work. The next session starts by reading what you write. Every line you write costs every next session, so the files stay **lean**: they hold only what the next session needs, and they point to everything else.

You write three things: `docs/handoff.md`, one entry in `docs/ledger.md`, and fixes to project docs that drifted. Take the extra minute for step 1. A lean file comes from a careful review, not from a fast summary.

If the user passed an argument, it names the focus of the next session. Keep what bears on that focus and drop the rest.

## When to run it

- The user asks for it.
- A milestone landed: a feature done, a decision settled, a phase closed.
- The context window is about 40% full. Past that point the agent starts to lose track. Pause the work, tell the user that you save the state, run this skill, and tell the user to start a fresh session and ask it to read `docs/handoff.md`.

## 1. Review before you write

Read the current `docs/handoff.md` and `docs/ledger.md`. Then sort every line of the old handoff into one of these groups:

| The line | What you do |
|---|---|
| Work done in this session | Put it in the ledger entry. The handoff gets it only when the next step depends on it. |
| Work done in an earlier session | Drop it. The ledger and git already hold it. |
| An open problem | Check it against git, `gh` and the code. Keep it only when it is still open. Write which problems you dropped as fixed. |
| A fact that stays true next month | Move it to its home: `AGENTS.md` or `CLAUDE.md`, `GLOSSARY.md` or an ADR. Leave a one-line pointer in the handoff, or nothing. |
| A plan or a next step | Keep it when it is still the plan. Drop it when the user dropped it. |
| Text that a spec, issue, PR, commit or file already holds | Replace it with the path or the URL. |

A claim that you did not check is a belief. Write it as a belief ("not verified: ..."), so that the next agent checks it.

Step 1 is done when each line of the old handoff has a group and each kept problem has a check.

## 2. Write the handoff

Write `docs/handoff.md` again from the start, with the template below. Do not append to the old file. The file stays under 60 lines. When it does not fit, go back to step 1 and move more lines to their homes.

```markdown
# Handoff: YYYY-MM-DD

## Now
- [Where the work stands, 3 to 5 bullets]

## Open problems
- [Problem, what was tried, the current guess. Only problems you checked in step 1.]

## Decisions to keep in mind
- [Only decisions that the next session can break by accident. Point to the home of each one.]

## Next
1. [The first action]
2. [Then]

## Suggested skills
- [The skills the next agent should call, and why]
```

Leave out a section that has no content. Write no secrets: no keys, tokens or passwords.

## 3. Add the ledger entry

Add one entry at the top of "Recent sessions" in `docs/ledger.md`. When the file does not exist, create it with this skeleton:

```markdown
# Ledger

Last updated: YYYY-MM-DD

## Key details
- [Facts every session needs: where things run, who owns what, the main links]

## Recent sessions

## Archive
```

The entry has at most 10 lines:

```markdown
### YYYY-MM-DD: [goal in a few words]
- Done: [results, with PR numbers]
- Learned: [only what changes future work, or leave out the line]
- Open: [what waits, or leave out the line]
```

Keep 5 entries in "Recent sessions". Move the oldest entry to "Archive" as one line. Keep 20 lines in "Archive" and delete older lines. Git holds the full history. Update the "Last updated" date.

Change "Key details" only when a fact in it changed. Name each change in your reply.

## 4. Fix the project docs that drifted

Compare what the work did with the docs that describe it. List each mismatch. Do not sweep all of `docs/`.

| Mismatch | Home |
|---|---|
| A new convention or a changed convention | `AGENTS.md` or `CLAUDE.md` |
| A new or sharper domain term | `GLOSSARY.md` at the repo root |
| A decision that is hard to reverse, surprising without context and a real trade-off | A new ADR in `docs/adr/`. Read the ADR titles first, and skip it when an ADR covers it. |
| A change to the system design | `docs/architecture.md`, only when the repo already has it |

Make the smallest edit that removes each mismatch. Create no new kind of doc unless the user asks.

## Reply

Tell the user:

- The handoff length in lines, and what you dropped or moved, by group.
- The ledger entry date, and any entries you archived.
- Each project doc you changed, and the mismatch it fixed.
