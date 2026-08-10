# file-organizer

A Python script that sorts a folder's files into category subfolders (Images, Documents,
Audio, …) by extension. **Track A** of my two-track Python plan — see `~/.claude/CLAUDE.md`
for the plan and for how I want to be taught. Track B (interview prep) lives in
`../LeetCodePython`.

## Goal for this project

Package it as a standalone `.exe` on a flash drive that I can drag a folder onto and use
to organize a client's files on a machine with no Python installed. Remaining work and
current step are tracked in `TODO.md` — check there before suggesting what's next.

## Files

| File | Purpose |
|---|---|
| `organizer.py` | The whole program |
| `TODO.md` | Roadmap to the portable `.exe`, with the current step marked |
| `LEARNING_NOTES.md` | My notes on concepts as I learn them — Python, Markdown, Git |
| `README.md` | Public-facing; portfolio standards apply |

`organizer.py` is heavily commented in my own words on purpose. Those comments are study
notes, not clutter — don't strip or "clean up" them.

## Working on client files — safety rules

This tool moves real files and has no undo. Any change must respect that:

- Never overwrite an existing file. Rename the incoming one instead.
- One bad file (locked, permission denied, weird name) must not kill the run and leave a
  folder half-organized.
- Prefer a dry-run/preview before anything destructive.
- When testing, use `C:\Users\morit\test-folder-python-script`, never a real folder.

## Interview-prep crossovers in this codebase

Flag these briefly when they come up — same rule as the global file, one or two sentences:

- `extension_categories` — a dict lookup with a default (`.get(key, "Other")`). This is the
  hash-map pattern: O(1) average lookup, the core trick in Two Sum, Group Anagrams, and
  Contains Duplicate.
- The `while` loop for duplicate filenames — same "advance until the condition breaks"
  mechanic as two-pointer and sliding-window problems.
- Extending this to subfolders would mean recursion or an explicit stack — the same shape
  as tree/graph DFS.
