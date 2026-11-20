---
name: wayfinder
description: Plan a huge chunk of work, more than one agent session can hold, as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear. Use when an idea is too big and too foggy to spec in one go.
disable-model-invocation: true
---

A loose idea has arrived: too big for one agent session, and wrapped in fog. The way from here to the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the destination. This skill charts the way as a **shared map** on the repo's issue tracker, then works its **decision tickets** (questions whose resolution is a decision, not slices of a build to execute) one at a time until the route is clear.

The destination varies per effort, and naming it is the first act of charting: it shapes every ticket. It might be a spec to hand off and iterate on, or a decision to lock before planning starts. The map is domain-agnostic: engineering work, course content, whatever fits the shape.

## Plan, don't do

Wayfinder is **planning**: each ticket resolves a decision, and the map is done when the way is clear, with nothing left to decide before someone goes and does the thing. The pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off. Produce decisions, not deliverables. The map ends with a spec (see step 6 of [Work through the map](#work-through-the-map)).

## Refer by name

Every map and ticket is an issue, so it has a **name**: its title. In everything the human reads (narration, the map's Decisions-so-far), refer to it by that name, never by a bare id, number, or slug. A wall of `#42, #43, #44` is illegible; names read at a glance. The id and URL don't vanish: a name wraps its link, but they ride _inside_ the name, never stand in for it.

## How to interview

Several steps below grill the user. If you have the `grill-me` skill, use it. Otherwise interview the user one decision at a time: give your recommended answer with each question, wait for the answer, look facts up yourself instead of asking, and stop when no decision is left open and the user confirms.

## The Map

The map is a single issue on this repo's issue tracker, labelled `wayfinder:map`: the canonical artifact. Its tickets are child issues of the map. Create the `wayfinder:*` labels if they are missing. In a repo that is not the user's own, ask first.

The map is an **index**, not a store. It lists the decisions made and points at the tickets that hold their detail; a decision lives in exactly one place, its ticket, so the map never restates it, only gists it and links.

The tracker is **GitHub Issues through `gh`**, unless `AGENTS.md` or `CLAUDE.md` names another one. On GitHub: the map and its tickets are issues, child tickets are sub-issues, claiming is assignment, and the frontier is a `gh issue list` query over open, unassigned, unblocked children.

### The map body

The whole map at low resolution, loaded once per session. Open tickets are **not** listed: they are open child issues, found by query.

```markdown
## Destination

<what reaching the end of this map looks like: the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index: one line per closed ticket, enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link): <one-line gist of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduates -->
```

### Tickets

Each ticket is a **child issue** of the map; the tracker's issue id is its identity. Its body is the question, sized to one 100K token agent session:

```markdown
## Question

<the decision or investigation this ticket resolves>
```

Each ticket carries a `wayfinder:<type>` label: one of `research`, `prototype`, `grill-me`, `task` (see [Ticket Types](#ticket-types)). `wayfinder:` labels are the only labels a map and its tickets carry, never a status label like `ready-for-agent`: they are decisions, not implementation work.

A session **claims** a ticket by assigning it to the dev driving the map, **first**, before any work, so concurrent sessions skip it. That assignee _is_ the claim: an open, unassigned ticket is unclaimed.

Blocking uses GitHub's **native** blocked-by relationship where available: essential because it renders the frontier _visually_ in GitHub's own UI, so the human sees what's takeable without opening the map. Where the repo lacks native blocking, fall back to a `Blocked by: #N` line in the ticket body. A ticket is **unblocked** when every ticket blocking it is closed; the **frontier** is the open, unblocked, unclaimed children: the edge of the known.

The answer isn't part of the body: it's recorded on resolution (see [Work through the map](#work-through-the-map)). Assets created while resolving a ticket are linked from the issue, not pasted in.

## Ticket Types

Every ticket is either **HITL** (human in the loop, worked _with_ a human who speaks for themselves) or **AFK**, driven by the agent alone. A HITL ticket only resolves through that live exchange; the agent never stands in for the human's side of it (a grilling agent that answers its own questions has broken this).

- **Research** (AFK): Reading documentation, third-party APIs, or local resources like knowledge bases to surface a fact a decision waits on. Resolved by a research subagent: a subagent with a fresh context that reads high-trust primary sources, answers the ticket's question, cites each source, and writes its findings to one Markdown file. Use when knowledge outside the current working directory is required.
- **Prototype** (HITL): Raise the fidelity of the discussion by making a cheap, rough, concrete artifact to react to: an outline, a rough take, a stub, or UI or logic code. If you have the `prototype` skill, use it for code. Otherwise build the smallest throwaway thing that answers the question, mark it as a prototype, and keep it out of the main branch. Links the prototype as an asset. Use when "how should it look" or "how should it behave" is the key question.
- **Grill-me** (HITL): Conversation. The default case. Interview the user (see [How to interview](#how-to-interview)).
- **Task** (HITL or AFK): Manual work that must happen before a _decision_ can be made: nothing to decide, prototype, or research, but the discussion is blocked until it's done. Signing up for a service so its API can be judged, provisioning access, moving data so its shape can be seen. This is the one type that _does_ rather than decides, and it earns its place by unblocking a decision, not by delivering the destination. The agent drives it alone where it can (AFK); otherwise it hands the human a precise checklist (HITL). Resolved when the work is done; the answer records what was done and any resulting facts (credentials location, new URLs, row counts) later tickets depend on.

## Fog of war

The map is _deliberately_ incomplete: don't chart what you can't yet see. Beyond the live tickets lies the **fog of war**: the dim view of decisions and investigations you can tell are coming but can't yet pin down, because they hang on questions still open. Resolving a ticket clears the fog ahead of it, graduating whatever's now specifiable into fresh tickets, one at a time, until the way to the destination is clear and no tickets remain.

The map's **Not yet specified** section is where that dim view is written down: the suspected question, the area to revisit later. It's the undiscovered frontier _toward_ the destination: everything here is in scope, just not sharp enough to ticket. Write as loosely or as fully as the view allows; it doubles as a signpost for collaborators reading where the effort is headed.

**Fog or ticket?** The test is whether you can state the question precisely now, _not_ whether you can answer it now.

- **Ticket when** the question is already sharp, even if it's blocked and you can't act on it yet.
- **Not yet specified when** you can't yet phrase it that sharply. Don't pre-slice the fog into ticket-sized pieces: it's coarser than a ticket, and one patch may graduate into several tickets, or none, once the frontier reaches it.

**Not yet specified** excludes what's already decided (Decisions so far), what's already a live ticket, and what's out of scope (the next section).

## Out of scope

Fog only ever gathers _toward_ the destination. The destination fixes the scope, so work beyond it is **out of scope**: it isn't fog, and it doesn't belong in **Not yet specified**. It gets its own **Out of scope** section on the map: work you've consciously ruled out of _this_ effort. Scope, not sharpness, lands it here.

Out-of-scope work never graduates (the frontier stops at the destination), so it returns only if the destination is redrawn, and then as a fresh effort, not a resumption.

Ruling something out of scope is a scoping act, not a step on the route. When a ticket that already exists turns out to sit past the destination (mis-scoped in while charting, or exposed by a resolution), **close it** (a closed ticket is unambiguously off the frontier) and leave one line in the **Out of scope** section: the gist plus why it's out of scope, linking the closed ticket. It stays out of **Decisions so far**, which records the route actually walked; a scope boundary isn't a step on it.

## Invocation

Two modes. Either way, **never resolve more than one ticket per session**, with the exception of research tickets.

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Grill the user to pin down what this map is finding its way to: the spec, decision, or change. The destination fixes the scope, so it's settled first.
2. **Map the frontier.** Grill again, **breadth-first** this time: fan out across the whole space rather than deep on any one thread, surfacing the open decisions and the first steps takeable now. **If this surfaces no fog**, the way to the destination is already clear and the whole journey fits in one session. Then you do not need a map. Stop charting, finish the grill, and write the spec (step 6 of [Work through the map](#work-through-the-map)).
3. **Create the map** (label `wayfinder:map`): Destination and Notes filled in, Decisions-so-far empty, the fog sketched into **Not yet specified**.
4. **Create the tickets you can specify now** as child issues of the map, then wire blocking edges in a **second pass** (issues need ids before they can reference each other). Write cross-references in that pass too, with real ids: a placeholder `#<n>` auto-links to an unrelated issue. Wiring sorts them into the frontier and the blocked; everything you can't yet specify stays in the fog: the **Not yet specified** section.
   When the destination has a UI surface and the project has no `docs/design.md`, put a `grill-me` ticket for the point of view on the frontier: who the users are, what they care about, what the product wants to be to them, and 1 to 3 screens or sites the user likes as references. The ticket resolves when `docs/design.md` holds these answers.
5. **Fire the research subagents.** For each `research` ticket you just created, start a research subagent (see [Ticket Types](#ticket-types)) to resolve it in parallel. In Claude Code, start them at high effort; other agents use their default. Commit each subagent's findings file to a throwaway `research/<name>` branch, push the branch but open no PR (it is never merged), and leave a context pointer on the ticket. If your agent cannot start subagents, leave the research tickets on the frontier for the next sessions.
6. Stop: charting is one session's work; it hand-resolves nothing.

### Work through the map

User invokes with a map (URL or number). A ticket is **optional**: without one, you pick the next decision, not the user.

1. Load the **map**: the low-res view, not every ticket body.
2. Choose the ticket. If the user named one, use it. Otherwise take the first frontier ticket in order. **Claim it**: assign it to yourself before any work.
3. Resolve it as the type its `wayfinder:<type>` label names (see [Ticket Types](#ticket-types)). Read the label, not just the body: the body never states the type. **Zoom as needed**: fetch the full body of any related or closed ticket on demand; use the skills the `## Notes` block names where you have them. If in doubt, grill the user.
4. Record the resolution: post the answer as a **resolution comment**. On a HITL ticket, quote the user's own answer to each decision, and keep the ticket open while a question has no answer. Then **close** the issue, and **append a context pointer** to the map's Decisions-so-far.
5. Add newly-surfaced tickets (create-then-wire); graduate any fog the answer has made specifiable, clearing each graduated patch from **Not yet specified** so it lives only as its new ticket. If the answer reveals that a ticket (this one or another) sits beyond the destination, **rule it out of scope** rather than resolving it on the route. If the decision invalidates other parts of the map, update or delete those tickets.
6. When the map has no open tickets and **Not yet specified** is empty, the way is clear. Write the spec with the map and its closed tickets as input. If the user has the `to-spec` skill, suggest they run it, since only the user can start it. Otherwise write one issue that holds the problem, the solution, the user stories, the implementation and testing decisions, and what is out of scope, and link it from the map.

The user may run unblocked tickets in parallel, so expect other sessions to be editing the tracker concurrently.
