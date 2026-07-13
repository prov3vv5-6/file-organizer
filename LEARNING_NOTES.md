# File Organizer — Learning Notes

A personal reference for the Python file-organizer project. Covers what the
script does, the concepts learned, a cheat-sheet of the tools used, the bugs
hit (and how they were fixed), and the step-by-step order the project was built.

---

## What the script does

Point it at a folder. It looks at every **file** in that folder, reads each
file's **extension** (`.pdf`, `.jpg`, …), decides which **category** that type
belongs to, creates a subfolder for the category if one doesn't exist yet, and
**moves** the file into it. Result: a messy folder sorted into labelled
subfolders (`Images`, `Documents`, `Audio`, …). Safe to run repeatedly.

---

## Python concepts learned

### File structure / imports
- `import os` and `import shutil` load built-in **modules** (bundles of ready-made
  tools). After importing, you use a tool with `module.tool()`, e.g. `os.listdir()`.
- Code runs top to bottom when the file is executed — **except** code inside a
  `def`, which only runs when the function is **called**.

### Variables
- Just `name = value`. No `let` / `const` / `var` like JavaScript.

### Strings
- **Raw strings**: `r"C:\Users\..."` — the `r` makes backslashes literal, so
  Windows paths don't break (`\` is normally an escape character).
- **Methods**: `.lower()` returns a *new* lowercased string (the original is
  unchanged — strings can't be modified in place).
- **Concatenation**: `"a" + "b"` glues strings. `+` only works string-to-string.

### Lists
- Ordered collection in square brackets: `[".png", ".jpg"]` (like a JS array).
- The `in` keyword checks membership and returns `True`/`False`:
  `".png" in image_extensions`. **Exact** match — `".arw"` ≠ `"arw"`.

### Tuples + unpacking
- `os.path.splitext("a.pdf")` returns a **tuple** `("a", ".pdf")` (like a list
  you won't change).
- **Unpacking** grabs both at once: `name, extension = os.path.splitext(file)`.

### Loops
- `for file in files:` walks a list, handing you one item per pass (like JS
  `for...of`).
- **`continue`** immediately skips to the next iteration.

### Conditionals
- `if` / `elif` / `else`. First true branch runs, the rest are skipped.
- **`not`** flips a boolean: `not os.path.exists(path)` = "if it does not exist".
- Every `if`/`for`/`def`/`elif`/`else` line ends with a **colon `:`** and its
  body is **indented** (4 spaces). Indentation *is* the block — Python has no `{}`.

### Functions
- `def organize_folder(folder_path):` — `def` defines it, `folder_path` is a
  **parameter** (an input).
- **Defining ≠ calling.** You must call it: `organize_folder(r"C:\...")`.
  Defining alone does nothing.
- The parameter replaces hardcoded values — call it with any path.

### Dictionaries
- `{ key: value }` pairs (like a JS object): extension → category.
- Many keys can share a value (all image extensions → `"Images"`).
- **`.get(key, default)`** looks up a key, returns `default` if it's missing —
  the crash-proof way to read a dict. (Plain `dict[key]` raises `KeyError` if
  the key isn't there.)
- Replaced an 8-branch `if/elif/else` chain with a single `.get()` call.

---

## Module cheat-sheet

### `os`
| Call | What it does |
|------|--------------|
| `os.listdir(path)` | Returns a list of names in a folder — **files AND folders**. |
| `os.path.splitext(name)` | Splits into `(name, extension)`, e.g. `("task2", ".pdf")`. |
| `os.path.join(a, b)` | Joins path parts with the correct separator (`\` or `/`). |
| `os.path.exists(path)` | `True` if something exists at that path. |
| `os.path.isfile(path)` | `True` only if the path is a file (not a folder). |
| `os.makedirs(path)` | Creates the folder on disk. |

### `shutil`
| Call | What it does |
|------|--------------|
| `shutil.move(src, dst)` | Moves a file. If `dst` is a folder, drops the file inside it, keeping its name. |

---

## Bugs hit & lessons (the important part)

### 1. Case sensitivity — `.PNG` vs `.png`
Camera/phone files had UPPERCASE extensions. `".PNG"` and `".png"` are different
strings to Python, so uppercase files slipped past the category checks.
**Fix:** normalize every extension with `extension = extension.lower()`.

### 2. The script organized its own folders
`os.listdir()` returns **folders as well as files**. On a second run, the
category folders created earlier (`Images`, `Documents`, …) showed up in the
listing and got "organized" — the script moved its own output folders into
`Other`. Worked the first time, broke the second.
**Fix:** skip anything that isn't a file at the top of the loop:
```python
source_path = os.path.join(folder_path, file)
if not os.path.isfile(source_path):
    continue
```
This also makes the script **idempotent** — safe to run over and over.

**Meta-lesson:** code that works once can still be broken. The second run is a
real test.

---

## Steps we took to build it

1. **Import the module.** `import os`.
2. **Point at a folder.** `folder_path = r"C:\...\test-folder-python-script"`
   (a throwaway test folder — never experiment on real files).
3. **List the files.** `files = os.listdir(folder_path)`, then `print(files)` to
   see the raw list.
4. **Loop over them.** `for file in files:` printing each name — one at a time.
5. **Extract the extension.** `name, extension = os.path.splitext(file)` and
   print just the extension.
6. **Normalize case.** `extension = extension.lower()` (fixed the `.PNG` bug).
7. **Categorize (first pass).** Made an `image_extensions` list and an `if
   extension in image_extensions:` check. (Caught the missing-dot `"arw"` bug.)
8. **Full category chain.** Added lists for every type and an
   `if/elif/.../else` chain, printing the category per file.
9. **Store instead of print.** Each branch set `category = "..."`; moved a single
   `print` below the chain (DRY — Don't Repeat Yourself).
10. **Build the destination path.** `destination_folder = os.path.join(folder_path, category)`.
11. **Create the folder if missing.** `if not os.path.exists(...): os.makedirs(...)`.
12. **Move the file.** `import shutil`; build `source_path`; `shutil.move(source_path, destination_folder)`.
13. **Fix the folder-eating bug.** Added the `os.path.isfile` + `continue` guard
    at the top of the loop.
14. **Wrap it in a function.** `def organize_folder(folder_path):` around the
    logic, called at the bottom with the path.
15. **Refactor to a dictionary.** Replaced the eight lists + `if/elif` chain with
    one `extension_categories` dict and `category = extension_categories.get(extension, "Other")`.

---

## Markdown & the README

A **README** is the front page of a project — GitHub automatically displays a
file named `README.md` on the repo's main page. It's written in **Markdown**:
plain text with a few symbols that turn into formatting.

### Markdown cheat-sheet
| Syntax | Result |
|--------|--------|
| `# Text` | H1 — biggest heading (the title). More `#` = smaller heading. |
| `## Text` | H2 — section heading. |
| `### Text` | H3 — sub-section heading. |
| blank line | Separates paragraphs. Two lines with no blank line between them get mashed onto one line. |
| `- item` | Bullet list (dash + space). |
| `1. item` | Numbered list (number + dot + space) — implies an ordered sequence. |
| `` `text` `` | Inline code (monospace) — good for `os`, `organizer.py`, etc. |
| ` ``` ` … ` ``` ` | Fenced code block — three backticks on their own lines, code between. Standard for showing terminal commands. |

### Sections a good README has
1. **Title + one-line description** — what it is (H1 + a sentence).
2. **Features** — what it does, as a bullet list.
3. **Requirements** — what's needed to run it (here: Python 3, standard library only).
4. **Usage** — how to run it, in the order the user actually does it
   (set the folder path → then run), with a fenced code block for the command.
5. **How It Works** — optional plain-English walkthrough.
6. **How I Built This** — the portfolio section (see below).

### The "How I Built This" section
A section that demonstrates **AI fluency with real comprehension underneath** —
what separates using AI as a *teacher* from using it to generate code you don't
understand. Three sub-sections (use `###` headings, not `1./2./3.` — these are
categories, not steps):
- **What I used AI for** — Claude Code as a guided teacher, given a prompt that
  told it *not* to write the code, only explain concepts line by line.
- **What I did myself** — wrote every line, read every explanation, confirmed
  understanding before moving on, copy-pasted nothing.
- **What I learned** — name specifics: `os`, `shutil`, loops, conditionals,
  functions, Python file structure, dictionaries.

### Lessons
- **Document what the tool actually does today, not what you wish it did.**
  (Usage described editing the hardcoded path, because that's the real behavior.)
- **READMEs evolve with the code** — update Usage when the code changes.
- **A README is public-facing**, so fix typos and capitalize product names
  (`Claude Code`). Spelling that doesn't matter in a variable name *does* matter
  in prose a recruiter reads.
- **Instructions should read in the order the person performs them**
  (set path → then run, not the reverse).

---

## Git & GitHub

**Git** tracks the history of your files. **GitHub** is a website that hosts a
copy of that history so it's backed up and shareable. **`gh`** is GitHub's
command-line tool.

### The mental model — four places (this is 80% of Git)
Work moves *rightward* through these:
1. **Working directory** — your actual files on disk right now.
2. **Staging area** — a "loading dock" where you gather the changes for the next save.
3. **Repository (commits)** — permanent snapshots saved locally = your history.
4. **Remote (GitHub)** — a copy of that history on GitHub's servers.

The workflow is just moving changes rightward: **edit → `add` → `commit` → `push`.**

### Command cheat-sheet
| Command | What it does | How often |
|---------|--------------|-----------|
| `git init` | Turn a folder into a repo (creates hidden `.git/`). | Once per project |
| `git status` | Show current state: branch + staged/unstaged/untracked files. Changes nothing. | Constantly |
| `git add .` | Stage everything (the `.` = current folder) for the next commit. `.gitignore` still excludes ignored files. | Each change |
| `git commit -m "msg"` | Save a snapshot of staged changes to local history. | Each change |
| `gh repo create NAME --public --source=. --remote=origin` | Create the repo on GitHub *and* link the local repo to it. | Once per project |
| `git push -u origin main` | Upload commits. `-u` links local `main` to `origin/main` so later pushes are just `git push`. | `-u` once; `git push` after |

### Key terms
- **Branch** — a line of history. Default is `main` (matches GitHub's default).
- **Untracked file** — a file Git sees but isn't tracking yet (before first `add`).
- **`.gitignore`** — lists patterns Git should never track (`__pycache__/`,
  `*.pyc`, `.DS_Store`). Makes `git add .` safe.
- **remote / `origin`** — the hosted copy on GitHub; `origin` is the conventional
  nickname for your main remote.
- **root-commit** — the very first commit in a repo.

### Steps we took (one-time setup)
1. `git init` — created the repo (branch `main`).
2. `git status` — saw 4 untracked files.
3. `git add .` — staged them (files moved to "Changes to be committed").
4. `git commit -m "Initial commit"` — first snapshot saved locally.
5. `gh repo create file-organizer --public --source=. --remote=origin` —
   created the GitHub repo and linked it.
6. `git push -u origin main` — uploaded everything; project went live.

### The everyday loop (after setup)
Once the repo exists, saving new work to GitHub is just three commands:
```
git add .
git commit -m "Describe what you changed"
git push
```
Edit → `add` → `commit` → `push`. Run `git status` anytime you're unsure of the state.

### Lessons
- **`init`, `gh repo create`, and `-u` are one-time**; `add` / `commit` / `push`
  are the repeating daily loop.
- **Commit messages** describe what the snapshot is (`"Initial commit"`, then
  present-tense like `"Fix case-sensitivity bug"`).
- **Pushing to a public repo publishes to the internet** — choose `--public` vs
  `--private` deliberately (public is right for a portfolio piece; nothing here
  is sensitive, and `.gitignore` keeps junk out).

---

## Possible next steps

- **Return a summary** — have the function `return` how many files it moved
  (learn the `return` keyword).
- **Handle name collisions** — if the destination already has a file with the
  same name, `shutil.move` clobbers it. Check and rename first.
- **Command-line argument** — use the `sys` module to run
  `python organizer.py "C:\some\folder"` without editing the code.
- **Skip temp files** — `continue` past throwaway extensions like `.asd`.
