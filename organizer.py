#"Go find the os module and load all its tools so I can use them in this script." From now on, whenever you want one of those tools, you'll write os. followed by the tool's name. The os. prefix is how Python knows "this comes from the os module."
import os
import shutil
import sys

# refactoring list and using a dictionary instead. which stores everything as a key value pair. the extention is the key and the category 
# becomes the value. this will make adding new extensions and categories easier if need be by only adding one line
extension_categories = {
    ".png": "Images",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".svg": "Images",
    ".arw": "Images",
    ".gif": "Images",
    ".heic": "Images",
    ".avif": "Images",
    ".cr2": "Images",
    ".pdf": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".srt": "Documents",
    ".csv": "Spreadsheets",
    ".xlsx": "Spreadsheets",
    ".mp3": "Audio",
    ".wav": "Audio",
    ".m4a": "Audio",
    ".alp": "Audio",
    ".mp4": "Video",
    ".mov": "Video",
    ".webm": "Video",
    ".zip": "Archive",
    ".exe": "Installers",
    ".apk": "Installers",
    ".msi": "Installers",
    ".ics": "Calendar",
}

# function that organizes any folder and puts files into seperate categorized folders
def organize_folder(folder_path, dry_run):

    # os.listdir(). You give it a folder path inside the parentheses, and it hands back a list of the names of everything inside that folder.
    files = os.listdir(folder_path)
    total = 0
    renamed_files = 0
    planned_paths = set()
    category_counts = {}

    # python for loop
    # for file in files:
        # do something with filename
    for file in files:
        # build the full path to this entry. join C:\Users\morit\test-folder-python-script + \[each file] and store in a variable
        source_path = os.path.join(folder_path, file)

        # if that path is not a file (i.e. it's a folder), skip to the next item
        if not os.path.isfile(source_path):
            continue
        # splits the extension from the file and stores the .ext in a variable called extension and the name of the file as name
        name, extension = os.path.splitext(file)
        # make the extensions all lower case
        extension = extension.lower()

        # "look up this extension (key); if it's in the dict, give me its category(value); if not, give me "Other"."
        category = extension_categories.get(extension, "Other")

        # os.path.join() standard way to build paths in Python, this method joins the file_path and the category together and adds a \ or a / depending on the operating system (mac or windows) 
        destination_folder = os.path.join(folder_path, category)

        #" if the destination folder does not exist, then create it." Files whose folder already exists just skip the creation and move on.
        # os.path.exists() — you give it a path, and it returns True if something's already there, False if not. It's a yes/no question, perfect for an if
        # The not keyword — this flips a True/False value to its opposite. not True is False, and not False is True. So not os.path.exists(destination_folder) reads as: "if that folder does not exist."
        # os.makedirs() — you give it a folder path, and it actually creates that folder on disk.
        if not os.path.exists(destination_folder) and not dry_run:
            os.makedirs(destination_folder)

        # Joins the destination folder and file together and creates a file path, stores in destination_path variable 
        destination_path = os.path.join(destination_folder, file)
     
        counter = 1
        while os.path.exists(destination_path) or destination_path in planned_paths:
            new_name = f"{name}_{counter}{extension}"
            destination_path = os.path.join(destination_folder, new_name)
            counter += 1
            
        planned_paths.add(destination_path)
        if counter >= 2:
            renamed_files += 1

        total += 1
        category_counts[category] = category_counts.get(category, 0) + 1

        # shutil.move(). You give it two arguments — the source path and the destination — and it physically moves the file:
        if not dry_run:
            shutil.move(source_path, destination_path)

        print(f"{file} -> {os.path.join(category, os.path.basename(destination_path))}")
    
    print(f"Total files moved: {total}")
    print(f"Total files renamed: {renamed_files}")
    print("---------------------------------------")
    print("Breakdown")
    for category, count in category_counts.items():
        print(f"{category}: {count}")

# if the length of sys.argv(list of strings) is less than two means it only has our script name in the list and a folder has not been dragged in it yet. 
if len(sys.argv) < 2:
    print("Drag a folder onto this program to organize it.")
    sys.exit(1)
target_folder = sys.argv[1]

if not os.path.isdir(target_folder):
    print(f"{target_folder} Is not a valid folder path, please try again")
    sys.exit(1)

dry_run = "--dry-run" in sys.argv

if dry_run:
    print("DRY RUN — no files will be moved")

organize_folder(target_folder, dry_run)