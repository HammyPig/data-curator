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
        """
        Return a curated file path.

            Parameters
                file_path (str): A file path e.g. C:/Users/James/Pictures/hello.jpg

            Returns:
                curated_file_path (str): A file path in the form of:
                    <archive_path><time_created>_<original_filename>
                    e.g. D:/archive/images/photos/2022-09-03_hello.jpg
        """
        date_modified = os.path.getmtime(file_path)
        date_modified = datetime.datetime.fromtimestamp(date_modified)
        date_modified_str = date_modified.strftime("%Y-%m-%d")
        time_created_str = date_modified_str

        try:
            date_taken = Image.open(file_path)._getexif()[36867]
            date_taken = datetime.datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")
            date_taken_str = date_taken.strftime("%Y-%m-%d")
            time_created_str = date_taken_str
        except Exception:
            pass

        filename = os.path.basename(file_path)

        return f"{self.archive_path}{time_created_str}_{filename}"

    def curate_from_source(self, path):
        """
        Copies all images from a source directory and pastes them into the
        curated file path. Handles duplicate file paths automatically.

            Parameters
                path (str): A file path e.g. C:/Users/James/Pictures/

            Returns:
                None
        """
        operation_cancelled_str = "Operation cancelled.\n"

        # collect image files
        try:
            file_paths = []
            for path, subdirs, files in os.walk(path):
                for name in files:
                    file_path = os.path.join(path, name)
                    file_extension = file_path.split(".")[-1]
                    if file_extension in ("jpg", "png"):
                        file_paths.append(file_path)
        except KeyboardInterrupt:
            print(operation_cancelled_str)
            return

        continue_prompt = input(
            f"{len(file_paths)} image files ready to be curated. Do you wish to continue? y/n "
        )
        print()

        if continue_prompt != "y":
            print(operation_cancelled_str)
            return

        try:
            for file_path in file_paths:
                shutil.copy2(file_path, self.unique(self.curated(file_path)))
        except KeyboardInterrupt:
            print(operation_cancelled_str)
            return

    @staticmethod
    def unique(file_path):
        """
        Return a unique file path by adding _COPY<n> if the file path already exists.

            Parameters
                file_path (str): A file path e.g. C:/Users/James/Pictures/hello.jpg

            Returns:
                unique_path (str): A file path that does not exist
                    e.g. C:/Users/James/Pictures/hello.jpg
                    e.g. C:/Users/James/Pictures/hello_COPY.jpg
        """
        unique_path = file_path
        ext_i = file_path.rfind(".")

        n = 1
        while True:
            if os.path.exists(unique_path):
                unique_path = f"{file_path[:ext_i]}_COPY{n}{file_path[ext_i:]}"
                n += 1
            else:
                break

        return unique_path
