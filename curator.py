import os
import datetime
from PIL import Image

class Curator:

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
            
            if filename == "_renames.log":
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
        with open(path + "_renames.log", "a") as f:
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

        print(f"Successfuly renamed {count} files!")

    def run():
        
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
        
        def get_path():
            path = input("Paste destination path from windows explorer: ")
            #path = "E:\\archive\\images\\photos"

            path = path.replace("\\", "/")
            path += "/"

            return path

        device = get_device_name()
        path = get_path()

        print("Collecting files...")
        rename_queue = Curator.get_rename_queue(path, device)
        
        user_continue = input(f"{len(rename_queue)} files ready to be renamed. Do you wish to continue? y/n")

        if user_continue != "y":
            exit(0)

        Curator.execute_renames(rename_queue, path, undo=False)

        # optionally undo most recent renames
        while True:
            user_undo = input("Would you like to undo changes? y/n ")

            if user_undo == "y":
                execute_renames(renames, undo=True)
                break
            elif user_undo == "n":
                break
            else:
                print("Please answer with y/n")
                pass

def main():
    Curator.run()

if __name__ == "__main__":
    main()
