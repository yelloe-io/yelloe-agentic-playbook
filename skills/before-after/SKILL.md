---
name: before-after
description: Capture before and after evidence of a change, as labelled comparison images or a short video of a flow, and post it to an issue or PR. Use when asked for before/after screenshots, a demo video, visual proof of a fix, or images for an issue or PR.
---

# Before and after evidence

Proof of a fix a reader gets at a glance: the same screen with the bug and without it, the changed spot boxed in red and green. When a still cannot show the change (a drag, an animation, a flow over several screens), record a short video instead, see step 4b.

Needs:

- A browser driver. The steps use `playwright-cli` (`npm install -g @playwright/cli`) in a session of your own (`-s=<name>`). Another browser tool works if it can take screenshots; video needs `playwright-cli`.
- Python 3 with Pillow 10.1 or newer (`pip install pillow`) for `compose.py`.
- `ffmpeg` for the video contact sheet.
- The GitHub CLI `gh`, a version with `--attach`, to post. With an older `gh`, drag the files into the comment in the browser.

Work in a scratch folder in the OS temp directory, such as `<temp>/before-after-<issue>/`, with `shots/` inside.

## 1. Plan the shots

For each issue, list the steps from its repro and pick the screens that show the bug. Done when every claim in the issue has a screen that shows it.

## 2. Before

The fix sits committed on its branch, in a checkout or worktree with a running dev server. Undo it in the working tree only, against the merge base with the repo's default branch:

```bash
git -C <worktree> diff $(git -C <worktree> merge-base origin/<default-branch> HEAD) HEAD | git -C <worktree> apply -R
```

If the dev server does not reload on file changes, restart it. Walk the repro and take a screenshot at each planned screen, saved into `shots/` as `<issue>-before-<n>-<what>.png`. Look at every screenshot. Done when each planned screen visibly shows the bug.

## 3. After

Restore the fix and confirm the tree is clean with `git -C <worktree> checkout -- . && git -C <worktree> status --short`. Close the before browser and open a fresh one, so storage from the buggy run cannot leak in. Walk the same steps and save `<issue>-after-<n>-<what>.png` with the same numbers.

## 4. Mark

Write a spec and run `compose.py` from this skill's folder:

```bash
python <this-skill-folder>/compose.py <scratch>/spec.json
```

```json
{
  "shots": "<scratch>/shots",
  "out": "<scratch>/shots/compare",
  "images": [
    {
      "file": "42-before-after.png",
      "layout": "stack",
      "scale": 0.75,
      "panels": [
        {"shot": "42-before-1-report.png", "kind": "before", "crop": [0, 55, 1920, 700], "box": [330, 425, 1590, 675], "note": "total is 400 off"},
        {"shot": "42-after-1-report.png", "kind": "after", "crop": [0, 55, 1920, 700], "box": [330, 425, 1590, 675], "note": "total matches the invoice"}
      ]
    }
  ]
}
```

- One image per claim, before panel then after panel. `stack` for full-width screens, `side` for narrow crops.
- `crop` and `box` are `[left, top, right, bottom]` in the screenshot's pixels. Box the same spot in both panels.
- The note says in plain words what the panel shows.

Look at every composed image. Done when each one reads at a glance without the issue beside it.

## 4b. Video

Rehearse the flow once with `snapshot` and refs, then write the take as a script: `video-start <issue>-after.webm --size 1280x720 --cursor`, a `video-chapter "<what happens next>" --duration=1500` before each step, the steps by text selectors, and `video-stop`. Check the take on a contact sheet:

```bash
ffmpeg -loglevel error -y -i <issue>-after.webm -vf "fps=1,scale=640:-1,tile=3x3" -frames:v 1 <issue>-after-sheet.png
```

Look at the sheet. Done when it shows every chapter and the change, and the file is under 10 MB.

## 5. Hand off

When the evidence is for a PR you are writing, hand the files and one note per file to that step. Otherwise write a short comment per issue to a file, show the user, and post after they say yes:

```bash
gh issue comment <issue> --body-file comment.md --attach ./<file>.png
```
