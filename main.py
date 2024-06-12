import os
import shutil
import sys

target_dir = input("Provide Target Directory's FilePath: ")

def get_all_folders(directory):
    folder_paths = []
    for entry in os.scandir(directory):
        if entry.is_dir():
            folder_paths.append(entry.path)
    return folder_paths

if not os.path.exists(target_dir):
    print("Target directory does not exist!")
    sys.exit()

method = input("Would you like to sort included files stored in folders inside the target directory (y/n)?: ")

sorted_items = {}

if method.lower() in ["y", "yes"]:
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                ext = os.path.splitext(file)[-1].lower()
                if ext:
                    ext = ext[1:]  # Remove the leading dot
                    if ext in sorted_items:
                        sorted_items[ext].append(file_path)
                    else:
                        sorted_items[ext] = [file_path]

elif method.lower() in ["n", "no"]:
    sorted_items = {"folders": []}
    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        if os.path.isdir(item_path):
            sorted_items["folders"].append(item_path)
        elif os.path.isfile(item_path):
            ext = os.path.splitext(item)[-1].lower()
            if ext:
                ext = ext[1:]  # Remove the leading dot
                if ext in sorted_items:
                    sorted_items[ext].append(item_path)
                else:
                    sorted_items[ext] = [item_path]
# import json
# with open("test.txt", "w") as test:
#     test.write(json.dumps(sorted_items, indent=4))
confirmation = input("Are you sure you would like to sort all files (y/n)?: ").lower()

if confirmation in ["y", "yes"]:
    pass
elif confirmation in ["n", "no"]:
    sys.exit("Operation cancelled.")
else:
    print("Invalid input.")
    sys.exit()

for key, values in sorted_items.items():
    target_path = os.path.join(target_dir, key)
    os.makedirs(target_path, exist_ok=True)
    for file_path in values:
        try:
            shutil.move(file_path, target_path)
            print(f"Moved '{file_path}' to '{target_path}'.")
        except Exception as e:
            print(f"Failed to move '{file_path}' to '{target_path}': {e}")

if method.lower() in ["y", "yes"]:
    del_folders = input("Would you like to delete all folders that were left over, place them all in a new folder or do nothing (1, 2 or 3): ")
    if del_folders == "1":
        all_folders = get_all_folders(target_dir)
        for fold in all_folders:
            if fold.replace(target_dir, "").replace("/", "") not in sorted_items.keys():
                try:
                    shutil.rmtree(fold)
                    print(f"Folder '{fold}' successfully deleted.")
                except OSError as e:
                    print(f"Error: {fold} : {e.strerror}")
    elif del_folders == "2":
        os.makedirs(os.path.join(target_dir, "folders"),exist_ok = True)
        folders = os.path.join(target_dir, "folders")
        for item in get_all_folders(target_dir):
            if item.replace(target_dir, "").replace("/", "") not in sorted_items:
                shutil.move(item, folders)

    else:
        pass