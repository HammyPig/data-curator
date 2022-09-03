from src.curator import Curator

def curated_test(name, archive_path, file_path, expected):
    c = Curator()
    c.set_archive_path(archive_path)
    actual = c.curated(file_path)
    assert actual == expected, f"FAILED (curated {name}): Expected '{expected}' does not equal actual '{actual}'"
    print(f"PASSED (curated {name})")

def unique_test(name, file_path, expected):
    actual = Curator.unique(file_path)
    assert actual == expected, f"FAILED (unique {name}): Expected '{expected}' does not equal actual '{actual}'"
    print(f"PASSED (unique {name})")

def curated():
    curated_test(
        "basic",
        "./tests/unit-tests/curated/basic/",
        "./tests/unit-tests/curated/basic/Penguins.jpg",
        "./tests/unit-tests/curated/basic/2008-02-18_Penguins.jpg"
    )

    curated_test(
        "no date taken",
        "./tests/unit-tests/curated/no-date-taken/",
        "./tests/unit-tests/curated/no-date-taken/Lighthouse.jpg",
        "./tests/unit-tests/curated/no-date-taken/2022-08-21_Lighthouse.jpg"
    )

def unique():
    unique_test(
        "basic",
        "./tests/unit-tests/unique/basic/2008-02-11_Jellyfish.jpg",
        "./tests/unit-tests/unique/basic/2008-02-11_Jellyfish_COPY1.jpg"
    )

    unique_test(
        "second-copy",
        "./tests/unit-tests/unique/second-copy/2008-02-11_Jellyfish.jpg",
        "./tests/unit-tests/unique/second-copy/2008-02-11_Jellyfish_COPY2.jpg"
    )

    unique_test(
        "fourth-copy",
        "./tests/unit-tests/unique/fourth-copy/2008-02-11_Jellyfish.jpg",
        "./tests/unit-tests/unique/fourth-copy/2008-02-11_Jellyfish_COPY4.jpg"
    )

    unique_test(
        "false-alarm",
        "./tests/unit-tests/unique/false-alarm/2008-02-11_Jellyfish.jpg",
        "./tests/unit-tests/unique/false-alarm/2008-02-11_Jellyfish_COPY1.jpg"
    )

def main():
    curated()
    unique()

if __name__ == "__main__":
    main()
