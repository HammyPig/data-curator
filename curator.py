import os
import datetime
from PIL import Image

class Curator:

    log_filename = "_curator.log"
    archive_path_filename = ".archive-path.txt"
    devices = ["iphone5", "iphone7"]

    def get_rename_queue(path, device):
        rename_queue = []
        files = os.listdir(path)

        for filename in files:
            absolute_path = path + filename

            date_modified = os.path.getmtime(absolute_path)
            date_modified = datetime.datetime.fromtimestamp(date_modified)
            date_modified_str = date_modified.strftime("%Y-%m-%d")
            time_created_str = date_modified_str
            
            try:
                date_taken = Image.open(absolute_path)._getexif()[36867]
                date_taken = datetime.datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")
                date_taken_str = date_taken.strftime("%Y-%m-%d")
                time_created_str = date_taken_str
            except:
                pass
            
            if filename == Curator.log_filename:
                continue

            if filename.startswith(f"{time_created_str}_"):
                continue

            if filename.startswith(f"{date_modified_str}_"):
                new_filename = f"{time_created_str}{filename[10:]}"
                rename_queue.append((filename, new_filename))
                continue

            new_filename = f"{time_created_str}_{device}_{filename}"
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

    def curate(path, device):
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

    def run():
        
        def get_welcome_message():
            owl_art = """\
           _________
  /\ /\\   /         \\
 ((ovo)) <  Welcome! |
 ():::()  \\_________/
   VVV\
"""
            title_name = "DATA CURATOR"
            title_width = 32
            
            program_title = f"""\
{owl_art}
{title_width*"-"}
{title_name:^{title_width}}
{title_width*"-"}
"""

            return program_title

        def get_device_name():
            while True:
                for i, device in enumerate(Curator.devices):
                    print(f"{i}: {device}")
                
                device_i = int(input("Select source device: "))

                try:
                    device = Curator.devices[device_i]
                    return device
                except (TypeError, IndexError) as e:
                    print(f"ERROR: Please enter a number from 0 to {len(Curator.devices) - 1}")

        def get_archive_path(override=False):
            
            def cache_archive_path():
                path = input("Please paste a destination path to store your archive in: ")
                print()
                
                path = path.replace("\\", "/")

                if path[-1] != "/":
                    path += "/"

                with open(Curator.archive_path_filename, "w") as f:
                    f.write(path)
                
                return path

            if (not os.path.exists(Curator.archive_path_filename)) or override:
                path = cache_archive_path()
            else:
                with open(Curator.archive_path_filename, "r") as f:
                    path = f.readline()

            print(f"Destination path being used: '{path}'\n")

            return path

        print(get_welcome_message())

        path = get_archive_path()
        device = get_device_name()

        user_actions = {
            "0": ("Change destination path", get_archive_path, [True]),
            "1": ("Curate directory", Curator.curate, [path, device]),
            "q": ("Exit", exit, [0])
        }

        while True:
            
            for action_key, action in user_actions.items():
                desc = action[0]
                print(f"{action_key}: {desc}")
            print()

            user_action_key = input("User action: ")
            print()

            try:
                desc, func, args = user_actions[user_action_key]
                func(*args)
            except KeyError:
                print(f"ERROR: Please enter a number from 0 to {len(user_actions) - 1}")

def main():
    Curator.run()

if __name__ == "__main__":
    main()
