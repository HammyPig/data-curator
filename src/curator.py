import os
import datetime
from PIL import Image

class Curator:

    log_filename = "_curator.log"
    archive_path_filename = ".archive-path.txt"
    devices = ["iphone5", "iphone7"]

    def curated(file_path, device=""):
        # date attribute
        date_modified = os.path.getmtime(file_path)
        date_modified = datetime.datetime.fromtimestamp(date_modified)
        date_modified_str = date_modified.strftime("%Y-%m-%d")
        time_created_str = date_modified_str
        
        try:
            date_taken = Image.open(file_path)._getexif()[36867]
            date_taken = datetime.datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")
            date_taken_str = date_taken.strftime("%Y-%m-%d")
            time_created_str = date_taken_str
        except:
            pass
        
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)

        if device == "":
            return f"{time_created_str}_{filename}"
        else:
            return f"{time_created_str}_{device}_{filename}"

    def get_rename_queue(path, device=""):
        rename_queue = []
        files = os.listdir(path)

        for filename in files:
            absolute_path = path + filename

            if filename == Curator.log_filename:
                continue

            if len(filename) > 10 and filename[10] == "_":
                continue

            new_filename = Curator.curated(absolute_path, device)
            rename_queue.append((filename, new_filename))

        return rename_queue

    def execute_renames(rename_queue, path, undo=False):
        status_msg = ""
        count = 0
        with open(path + Curator.log_filename, "a") as f:
            for i, rename in enumerate(rename_queue):

                if undo:
                    new_filename, old_filename = rename
                else:
                    old_filename, new_filename = rename

                try:
                    os.rename(path + old_filename, path + new_filename)
                except FileExistsError:
                    # add duplicate notation
                    ext_i= new_filename.rfind(".")
                    n = 1
                    while True:
                        if n == 1:
                            n_str = ""
                        else:
                            n_str = str(n)

                        dupe_filename = f"{new_filename[:ext_i]}_COPY{n_str}{new_filename[ext_i:]}"

                        try:
                            os.rename(path + old_filename, path + dupe_filename)
                            break
                        except FileExistsError:
                            n += 1

                    if not undo:
                        rename_queue[i] = (old_filename, dupe_filename)

                    print(f"File {new_filename} already exists! Adding _COPY{n_str}...")
                    new_filename = dupe_filename

                except FileNotFoundError:
                    error_msg = f"File {old_filename} could not be located! Skipping..."
                    print(error_msg)
                    f.write(error_msg + "\n")
                    continue

                f.write(f"{path + old_filename}>{path + new_filename}\n")
                count += 1

            f.write("\n")
        
        if undo:
            action_desc = "undid"
        else:
            action_desc = "renamed"

        print(f"Successfuly {action_desc} {count} files!\n")

    def curate_from_source(path, device):
        print("Collecting files...\n")
        rename_queue = Curator.get_rename_queue(path, device)
        
        user_continue = input(f"{len(rename_queue)} files ready to be renamed. Do you wish to continue? y/n ")
        print()

        if user_continue != "y":
            exit(0)

        Curator.execute_renames(rename_queue, path, undo=False)

        # optionally undo most recent renames
        while True:
            user_undo = input("Would you like to undo changes? y/n ")
            print()

            if user_undo == "y":
                Curator.execute_renames(rename_queue, path, undo=True)
                break
            elif user_undo == "n":
                break
            else:
                print("Please answer with y/n")
                pass
