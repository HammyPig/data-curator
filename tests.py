from src.curator import Curator

def curated_test(name, file_path, expected):
    c = Curator()
    c.set_archive_path("./tests/unit-tests/curated/basic/archive-folder/")
    actual = c.curated(file_path)
    assert actual == expected, f"FAILED (curated {name}): Expected '{expected}' does not equal actual '{actual}'"
    print(f"PASSED (curated {name})")

def curated():
    curated_test(
        "basic",
        "./tests/unit-tests/curated/basic/source-folder/Penguins.jpg",
        "./tests/unit-tests/curated/basic/archive-folder/2008-02-18_Penguins.jpg"
    )

    curated_test(
        "no date taken",
        "./tests/unit-tests/curated/basic/source-folder/Penguins.jpg",
        "./tests/unit-tests/curated/basic/archive-folder/2008-02-18_Penguins.jpg"
    )

def main():
    curated()

if __name__ == "__main__":
    main()
