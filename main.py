import os
from src.curator import Curator

ARCHIVE_PATH_FILENAME = ".archive-path.txt"


def welcome_message():
    owl_art = (
        "           _________   \n"
        "  /\ /\\   /         \\\n"
        " ((ovo)) <  Welcome! | \n"
        " ():::()  \\_________/ \n"
        "   VVV                 \n"
    )

    title_name = "DATA CURATOR"
    title_width = 32

    program_title = (
        f"{owl_art}"
        f"{title_width*'-'}\n"
        f"{title_name:^{title_width}}\n"
        f"{title_width*'-'}\n"
    )

    return program_title


def archive_path_input(override=False):
    def cache_archive_path():
        path = input("Please paste a destination path to store your archive in: ")
        print()

        path = path.replace("\\", "/")

        if path[-1] != "/":
            path += "/"

        with open(ARCHIVE_PATH_FILENAME, "w") as f:
            f.write(path)

        return path

    if (not os.path.exists(".archive-path.txt")) or override:
        path = cache_archive_path()
    else:
        with open(ARCHIVE_PATH_FILENAME, "r") as f:
            path = f.readline()

    print(f"Destination path being used: '{path}'\n")

    return path


def main():
    print(welcome_message())

    c = Curator()
    c.set_archive_path(archive_path_input())

    user_actions = (
        "0: Change destination path\n" "1: Curate from a directory\n" "q: Exit\n"
    )

    while True:

        print(user_actions)
        user_action_key = input("User action: ")
        print()

        if user_action_key == "0":
            c.set_archive_path(archive_path_input(True))
        elif user_action_key == "1":
            path = input("Please paste a source path: ")
            print()
            c.curate_from_source(path)
        elif user_action_key == "q":
            print("Goodbye!")
            exit(0)
        else:
            print("ERROR: Please enter a valid user action")


if __name__ == "__main__":
    main()
