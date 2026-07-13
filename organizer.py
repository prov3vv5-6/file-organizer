#"Go find the os module and load all its tools so I can use them in this script." From now on, whenever you want one of those tools, you'll write os. followed by the tool's name. The os. prefix is how Python knows "this comes from the os module."
import os
import shutil

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
    ".pdf": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".srt": "Documents",
    ".csv": "Spreadsheets",
    ".xlsx": "Spreadsheets",
    ".mp3": "Audio",
    ".wav": "Audio",
    ".m4a": "Audio",
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
def organize_folder(folder_path):

    # os.listdir(). You give it a folder path inside the parentheses, and it hands back a list of the names of everything inside that folder.
    files = os.listdir(folder_path)


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
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        
        
        # shutil.move(). You give it two arguments — the source path and the destination — and it physically moves the file:
        shutil.move(source_path, destination_folder)

        print(destination_folder)

organize_folder(r"C:\Users\morit\Downloads")