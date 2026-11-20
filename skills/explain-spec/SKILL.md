---
name: explain-spec
description: Quiz the user on a spec before agents build it. Builds one self-contained HTML page with background, toy data, a walk through the plan, and five concepts to answer, then opens it in the browser. Use when the user asks to be quizzed on a spec, or asks whether they understand a spec.
disable-model-invocation: true
---

# explain-spec

A comprehension **gate**: the user passes when they have a working mental model of what agents will build. It adapts Geoffrey Litt's explain-diff from a code change to a spec.

Input: a spec (an issue, a file or a link) that describes a build. Default: the spec this session just wrote or published.

Other input, such as a research note or a decision record, describes a decision, not a build. For that input, explain the decision and its consequences where these steps say the plan and the build.

## 1. Study

Read the spec in full, with its comments. Then read the code and docs that it changes. Done when you can say what the system does now, what it will do after the build, and why.

Pick five **concepts** for the quiz. These are the ideas the user must have to own the spec: behaviour, data flow, edge cases, failure modes, and why the spec chose this approach. Spread them across the riskiest decisions.

## 2. Write the page

Copy [`assets/quiz.html`](assets/quiz.html) to `YYYY-MM-DD-<slug>-quiz.html` in the OS temp folder (`$TMPDIR` or `/tmp` on macOS and Linux, `%TEMP%` on Windows), or in a git-ignored folder of the repo. Never save it where git would pick it up. The template is one self-contained page: inline CSS and JavaScript, system fonts, nothing from the network.

Fill its four sections, and replace every text in square brackets:

1. **Background**: the part of the system that the spec touches, and how it works now. Start with a beginner layer in the `.callout`, marked "safe to skip".
2. **Old and new**: the core idea, with toy data. Show one input, the result now, and the result after the build, in the `.diff` block.
3. **The plan**: a walk through the spec in the `.steps` list, grouped and ordered so it is easy to follow.
4. **Quiz**: fill `QUIZ` in the script.

Keep the page short and visual. Each section has a heading that states its point. Put code in `<pre>` blocks. Build diagrams from boxes and lists in HTML, not images.

For each concept, write a main question and a backup question with new wording and new options. Each question:

- Tests understanding, not trivia. A person who knows the spec can answer it. A person who only skimmed it cannot.
- Has four options. Each wrong option is a real misconception that a skimmer could hold. Keep the options similar in length. Vary the letter of the correct answer.
- Has a `why` line. The main question also has an `again` line: the concept from a different angle, aimed at the misconception that the wrong options show.

Each `QUIZ` entry has this shape: `c` is the concept name, `q` holds the main and the backup question. Each question has `t` (the question), `o` (four options, A to D), `a` (the index of the correct option), `why` (shown after any answer) and `again` (shown on a miss, main question only; leave it empty on the backup).

The page already does the rest. The first click on a question locks it. A miss shows the right answer, the `again` line and the backup question. A summary at the bottom shows **PASSED** when each concept is right through its main or its backup question.

Check the page before you hand it over. If you have a browser tool, open the file and take screenshots at desktop width and at 390px. Fix text that overlaps, is too small, or scrolls sideways, and click through one question. Search the file for `src="http`, `@import` and `url(http`: each search must find nothing. If you have no browser tool, tell the user you could not check the page visually.

## 3. Hand over

Open the page in the default browser (`open` on macOS, `xdg-open` on Linux, `start "" <path>` on Windows). Give the user the path. Ask them to reply with the summary line when they finish.

## 4. Result

The gate passes when the user reports PASSED. For each concept the user missed twice, ask: does the miss show a gap in the user, or a gap in the spec?

- **Gap in the spec**: the spec is unclear or wrong. Edit the spec so it says what was meant. Tell the user what changed.
- **Gap in the user**: explain the concept again in chat and ask a new four-option question there. Repeat until the answer is correct.

When the user stops before the gate passes, it does not pass.

Report: **PASSED** or **NOT PASSED**, each concept missed on the first try (one line each), and each spec edit.
