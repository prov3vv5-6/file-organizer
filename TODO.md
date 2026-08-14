# TODO — road to a portable flashdrive tool

Goal: a single `.exe` on a flash drive that I can drag a folder onto to organize a
client's files, on a machine that has no Python installed.

## 1. Take the folder path from the command line — DONE
Replace the hardcoded `organize_folder(r"C:\Users\morit\Downloads")` with a path
read from `sys.argv`, so a folder can be dragged onto the script/exe.
- [x] `import sys` and read `sys.argv[1]`
- [x] Handle the case where nothing was passed (double-clicked with no folder)
- [x] Handle a path that isn't a real folder (typo, deleted, or a file was dragged)

## 2. Survive duplicate filenames — DONE
Note what actually turned out to be true: `shutil.Error` is only raised when you pass
`shutil.move()` a *folder* as the destination. Passing a full file path skips that guard
entirely — `os.rename()` fails, Python falls back to `copy2`, and the existing file is
silently overwritten. No exception to catch, so the check has to be ours.
- [x] Detect the collision before moving (`os.path.exists(destination_path)`)
- [x] Rename the incoming file (`invoice.pdf` -> `invoice_1.pdf`) rather than
      overwriting, and never clobber an existing file
- [x] `while` loop keeps counting (`_1`, `_2`, …) until a free name is found

## 3. Better output — DONE
- [x] Print the real move: `invite.ics -> Calendar\invite_1.ics`
- [x] Build the printed path with `os.path.join`, not a hardcoded `\` in the f-string
      (`\{` is an invalid escape sequence — warns now, SyntaxError in a future Python)

## 4. Dry-run / preview mode — DONE
No undo exists, so I need to see what *would* happen before touching anything.
- [x] A flag (`--dry-run`) that prints every planned move without moving
- [x] Guard `os.makedirs` too — a dry run must not create empty category folders
- [x] Print a summary at the end: how many files, how many per category, how many
      renamed
- [x] `planned_paths` set — a dry run moves nothing, so `os.path.exists()` alone would
      report two colliding files both landing on the same name. The set remembers the
      names already claimed this run. (`x in some_set` is O(1); a list would make the
      loop O(n²) — same trade as Two Sum.)
- Per-category counts are a frequency map built with `.get(category, 0) + 1`, printed by
  looping `.items()`. Sorting that map by value instead of key is Top K Frequent.

## 5. Error handling ← in progress
- [x] Don't let one bad file (locked, permission denied) crash the whole run —
      `try`/`except OSError as error` around **only** the `shutil.move` call, then
      `continue`. `OSError` is the parent of `PermissionError`/`FileNotFoundError`, so
      one `except` covers the whole filesystem family. Keep the `try` narrow: wrapping
      the whole loop body would swallow my own bugs and report them as "bad file".
- [x] Bind the exception with `as error` and print `{error}`. Printing `{OSError}`
      instead gives `<class 'OSError'>` — same text for every failure, and no crash to
      tell me it's wrong, because `OSError` is a valid name in that scope.
- [x] Counters have to come *after* the move, not before. `total`, `category_counts`,
      and `renamed_files` all sat above the `try`, so a file that failed was still
      counted as moved. Sitting them below the `try` block (but outside `if not
      dry_run`) fixes both paths: a real failure hits `continue` and skips them, and a
      dry run falls straight through and still counts.
- [ ] Guard `os.makedirs` too — if it fails, every file in that category fails

## 5c. Failed moves leave a partial copy — the "skipped" message lies
Found while testing step 5 with a genuinely locked file. `shutil.move` is not one
operation: it tries `os.rename` first, and on failure falls back to *copy, then delete
the original*. With a locked file the copy **succeeds** and the delete fails, so the
exception arrives after the destination is already written. Result: the client has the
same file in two places and the run prints "Skipped".
- [ ] Decide the approach: pre-flight check (try opening the file exclusively before
      moving, skip if it won't open), or detect the leftover afterward and report it
      loudly
- [ ] Do **not** "fix" it by deleting the copy — safety rule says never `os.remove` on a
      client's files, and a bug there destroys data
- [ ] Whatever the fix, the printed message must distinguish *skipped* from *half-moved*

## 5d. Renaming lowercases the extension
`new_name` is built from the `extension` variable, which was lowercased for the category
lookup. So `PHOTO.JPG` renames to `PHOTO_1.jpg`. Harmless on Windows (case-insensitive
filesystem), but wrong if the files ever land on a Mac or Linux box.
- [ ] Keep the original extension casing when building `new_name`; lowercase only for
      the dict lookup

## 6. Package as a standalone .exe
- [ ] Build with PyInstaller (`--onefile`) so no Python is needed on the target PC
- [ ] Add `build/`, `dist/`, and `*.spec` to `.gitignore`
- [ ] Test the exe from the flash drive on a machine without Python
- [ ] Note the caveats: Windows-only build; antivirus sometimes flags fresh
      PyInstaller exes

## 7. True duplicate detection (content, not filename)
Separate from step 2. Step 2 handles *same name, different file* — always rename, never
lose anything. This step handles *same content*, which is the only case where deleting a
file is defensible.
- [ ] Hash each file's contents with `hashlib` and store hashes in a dict; a repeat key
      means genuinely identical content
- [ ] Prefilter on `os.path.getsize()` first — different sizes can't be duplicates, so
      skip hashing those entirely (hashing every file is the expensive part)
- [ ] Give the user a choice: keep both (rename), or set the duplicate aside
- [ ] "Delete" must mean recoverable — move to a `_Duplicates` folder or use
      `send2trash` to the Recycle Bin. Never `os.remove()` on a client's files.
- [ ] Wire it into `--dry-run` (step 4) so the duplicate list can be reviewed first
- Interview crossover: bucketing files by content hash is Group Anagrams. Brute-force
  pairwise comparison is O(n²); hashing into a dict is O(n) — the Two Sum trade.

## Later / maybe
- [ ] Log every move to a file so a run can be reviewed (or reversed by hand)
- [ ] Let categories be edited without touching the code (config file)
