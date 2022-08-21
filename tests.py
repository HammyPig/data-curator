from curator import Curator
import shutil
import re
import os

def get_rename_queue_test_basic():
    path = "tests/unit-tests/get_rename_queue/basic/"
    device = "iphone5"
    actual_rename_queue = Curator.get_rename_queue(path, device)
    expected_rename_queue = [("Penguins.jpg", "2008-02-18_iphone5_Penguins.jpg")]

    assert actual_rename_queue == expected_rename_queue, f"Expected '{expected_rename_queue}' does not equal actual '{actual_rename_queue}'"
    print("PASSED: rename_queue_test_basic")

def get_rename_queue_test_am_pm():
    path = "tests/unit-tests/get_rename_queue/am_pm/"
    device = "iphone5"
    actual_rename_queue = Curator.get_rename_queue(path, device)
    expected_rename_queue = [("Desert.jpg", "2008-03-14_iphone5_Desert.jpg")]

    assert actual_rename_queue == expected_rename_queue, f"Expected '{expected_rename_queue}' does not equal actual '{actual_rename_queue}'"
    print("PASSED: rename_queue_test_am_pm")

def get_rename_queue_test_no_date_taken():
    path = "tests/unit-tests/get_rename_queue/no_date_taken/"
    device = "internet"
    actual_rename_queue = Curator.get_rename_queue(path, device)
    expected_rename_queue = [("Lighthouse.jpg", "2022-08-21_internet_Lighthouse.jpg")]

    assert actual_rename_queue == expected_rename_queue, f"Expected '{expected_rename_queue}' does not equal actual '{actual_rename_queue}'"
    print("PASSED: rename_queue_test_no_date_taken")

def get_rename_queue_test_ignore_formatted_files():
    path = "tests/unit-tests/get_rename_queue/ignore_formatted_files/"
    device = "iphone5"
    actual_rename_queue = Curator.get_rename_queue(path, device)
    expected_rename_queue = []

    assert actual_rename_queue == expected_rename_queue, f"Expected '{expected_rename_queue}' does not equal actual '{actual_rename_queue}'"
    print("PASSED: rename_queue_test_ignore_formatted_files")

def execute_renames_test_basic():
    path = "tests/unit-tests/execute_renames/basic/"
    device = "iphone5"

    try:
        shutil.rmtree(path + "actual/")
    except FileNotFoundError:
        pass

    shutil.copytree(path + "input/", path + "actual/")

    rename_queue = Curator.get_rename_queue(path + "actual/", device)
    Curator.execute_renames(rename_queue, path + "actual/")
    expected_files = os.listdir(path + "expected/")
    actual_files = os.listdir(path + "actual/")

    assert str(actual_files) == str(expected_files), f"Expected '{str(expected_files)}' does not equal actual '{str(actual_files)}'"
    print("PASSED: execute_renames_test_basic")

def execute_renames_test_duplicate_files():
    path = "tests/unit-tests/execute_renames/duplicate_files/"
    device = "iphone5"

    try:
        shutil.rmtree(path + "actual/")
    except FileNotFoundError:
        pass

    shutil.copytree(path + "input/", path + "actual/")

    rename_queue = Curator.get_rename_queue(path + "actual/", device)
    Curator.execute_renames(rename_queue, path + "actual/")
    expected_files = os.listdir(path + "expected/")
    actual_files = os.listdir(path + "actual/")

    assert str(actual_files) == str(expected_files), f"Expected '{str(expected_files)}' does not equal actual '{str(actual_files)}'"
    print("PASSED: execute_renames_test_duplicate_files")

def main():
    get_rename_queue_test_basic()
    get_rename_queue_test_am_pm()
    get_rename_queue_test_no_date_taken()
    get_rename_queue_test_ignore_formatted_files()
    execute_renames_test_basic()
    execute_renames_test_duplicate_files()

if __name__ == "__main__":
    main()
