---
name: grill-me
description: A relentless interview to sharpen a plan or design, one decision at a time, each with a recommended answer. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrase.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree **one question at a time**. The **frontier** is every decision whose prerequisites are already settled: the questions you could ask _now_ without guessing at answers you haven't heard yet. From the frontier, take the question the most hangs on, give your recommended answer, and wait.

Sort each question:

- A **big** question changes the plan or is hard to undo. Ask it alone, in at most 3 short sentences.
- A **small** question has a clear default and is cheap to change. Ask up to 5 small questions in one message, so that the user can answer them fast.

Each question should be formatted like so:

```
[■■■■■□□□□□] 7/14

❓ **Q8** - **<question title>**: <where this lives on the screen>. <question body, including multiple choices>

➡️ <your recommended answer>
```

Put the progress bar once at the top of every message. It has 10 cells. The first number counts the answered questions. The second number is the answered questions plus your estimate of the questions left, so it can grow.

Start each question with the place on the screen where the user meets it. When it has no screen, start with a concrete example.

An answer names a choice. `all` takes every recommendation in the message, and `1 yes, 3 no` answers those questions. A skipped question stays open, and so does a reply that asks something back. Ask an open question again. A yes covers only what the question named.

Each answer reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next question. Number the questions as one running count across the session (Q1, Q2, ...), so any decision can be referred back to by number.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a subagent with a fresh context to find it. If your agent cannot start subagents, look it up yourself between questions. Don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the result. Carry on with a question that doesn't depend on it. The _decisions_ are the user's: put each to them and wait.

## Point of view for UI work

When the plan has a UI surface and the project has no `docs/design.md`, the tree also holds the point of view:

- Who the users are.
- What they care about.
- What the product wants to be to them.
- 1 to 3 screens or sites the user likes as references, and what to take from each.

When these branches are settled, write `docs/design.md` with one section per point above, in the user's own words where you can. Show it to the user and fix what they correct. Later UI work reads it as the look and the voice to aim for.

## Done

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
