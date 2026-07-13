# File Organizer

This project points at any folder on a computer and automatically organizes the files contained in that folder into designated subfolders.

## Features

- Uses a dictionary to give every file extension a unique category name
- Handles many file types including (images, documents, audio, video, installers, etc.)
- Creates the category folders when needed and puts files not included in the dictionary in an "Other" subfolder
- Is case-insensitive so that .PNG and .png for example will go into the same subfolder
- Is safe to run repeatedly and will skip folders, and won't reorganize its own output

## Requirements

This project uses Python 3 and only uses the standard library (`os` and `shutil`) so there is nothing extra to install.

## Usage

1. To use the program replace the "C:\Users\morit\test-folder-python-script" folder path line in the function call at the bottom of the program named: `organize_folder()` with whatever folder you want to organize on your computer. For example `organize_folder(r"C:\Users\username\Downloads")`

2. Then run the following command in your terminal

```
python organizer.py
```

## How I Built This

### What I used AI for

- I used Claude Chat to brainstorm ideas for a program that I could write to teach me python. One reason for this, is to prepare me for a market in need of programmers who can use python to automate tasks
- Claude Chat gave me the idea to create a file organizer to start out with, and I thought "that would be a helpful program to use myself on my Downloads folder"
- Then I used Claude Chat to write me a prompt I could give Claude Code so it would understand to teach me python without generating code for me, and explain concepts step by step line by line
- I also used AI to teach me how to write this README.md file

### What I did myself

- I wrote every line of code myself
- I read the explanation of each line Claude Code suggested I write, and confirmed I understood it before moving on
- I copy and pasted nothing

### What I learned

- I already knew a lot of the concepts of loops, conditionals, dictionaries, lists, variables, modules, and functions but from this program I learned the python syntax for them and how to implement them in a real world project.
- This was the first program Ive written that has done something on my computer and not online, so that was interesting and exciting to see files move and folders made automatically on my own computer after running the program. I learned that using the `os` and `shutil` module allows python to do this along with their built-in methods like `os.listdir()`, `os.path.join()`, and `shutil.move()`, just to name a few.
- I also learned and further solidified the idea of writing small pieces of code and testing it using a `print()` statement. Also, that it's okay to write messy repeating code, test it, and then refactor it so it follows the DRY principle
