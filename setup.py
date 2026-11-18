#!/usr/bin/env python

import os
from pathlib import Path

from setuptools import find_packages, setup

ROOT = Path(__file__).parent

# Everything that ends up in the sdist or the wheel (see MANIFEST.in).
PACKAGED_PATHS = (
    "CHANGES.rst",
    "LICENSE",
    "README.rst",
    "MANIFEST.in",
    "setup.py",
    "setup.cfg",
    "pyproject.toml",
    "number_parser",
    "tests",
)


def find_symlinks(root=ROOT, paths=PACKAGED_PATHS):
    """Return the symbolic links among the files that are packaged.

    setuptools stores the *target* of a symbolic link in the sdist and the
    wheel. A link that points outside the checkout would therefore publish
    a file that is not part of the repository, so the build refuses links.
    """
    found = []
    for name in paths:
        path = Path(root) / name
        if path.is_symlink():
            found.append(path)
            continue
        if not path.is_dir():
            continue
        for directory, dir_names, file_names in os.walk(path):
            for entry in dir_names + file_names:
                entry_path = Path(directory) / entry
                if entry_path.is_symlink():
                    found.append(entry_path)
    return sorted(found)


if __name__ == "__main__":
    symlinks = find_symlinks()
    if symlinks:
        raise SystemExit(
            "Refusing to build: symbolic links are not allowed in packaged files: "
            + ", ".join(str(path.relative_to(ROOT)) for path in symlinks)
        )

    version = (ROOT / "number_parser/VERSION").read_text("ascii").strip()

    setup(
        name="number-parser",
        version=version,
        description="parse numbers written in natural language",
        long_description=(ROOT / "README.rst").read_text(encoding="utf8")
        + "\n\n"
        + (ROOT / "CHANGES.rst").read_text(encoding="utf8"),
        author="Arnav Kapoor",
        author_email="arnavk805@gmail.com",
        url="https://github.com/scrapinghub/number-parser/",
        packages=find_packages(exclude=["tests"]),
        include_package_data=True,
        install_requires=[
            "attrs >= 17.3.0",
        ],
        zip_safe=False,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3.13",
        ],
    )
