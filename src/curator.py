import os
import shutil
import datetime
from PIL import Image

class Curator:

    def __init__(self):
        self.archive_path = ""

    def get_archive_path(self):
        return self.archive_path

    def set_archive_path(self, archive_path):
        self.archive_path = archive_path

    def curated(self, file_path):
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

        return f"{time_created_str}_{filename}"

    def curate_from_source(self, path):
        # collect image files
        file_paths = []
        for path, subdirs, files in os.walk(path):
            for name in files:
                file_path = os.path.join(path, name)
                file_extension = file_path.split(".")[-1]
                if file_extension in ("jpg", "png"):
                    file_paths.append(file_path)
        
        continue_prompt = input(f"{len(file_paths)} image files ready to be curated. Do you wish to continue? y/n ")
        print()

        if continue_prompt != "y":
            print("Operation cancelled.\n")
            return

        # create copy queue
        copy_queue = []
        for file_path in file_paths:
            copy_queue.append((file_path, self.curated(file_path)))

        for old_file_path, new_file_path in copy_queue:
            shutil.copy2(old_file_path, new_file_path)
