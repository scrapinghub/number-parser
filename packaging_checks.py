"""Checks that setup.py runs before it builds a distribution.

This module only uses the standard library, so the tests can import it
without setuptools.
"""

import os
from pathlib import Path

# Directories that are packaged recursively (see MANIFEST.in and setup.py).
PACKAGED_DIRECTORIES = ("number_parser", "tests")


def find_symlinks(root, directories=PACKAGED_DIRECTORIES):
    """Return the symbolic links among the files that can be packaged.

    setuptools stores the *target* of a symbolic link in the sdist and the
    wheel. A link that points outside the checkout would therefore publish
    a file that is not part of the repository.

    Every file at the top level is checked, because setuptools also packages
    files that MANIFEST.in does not name (for example LICENSE*, NOTICE* and
    AUTHORS*), and the packaged directories are checked recursively.
    """
    root = Path(root)
    found = [path for path in root.iterdir() if path.is_symlink() and not path.is_dir()]
    for name in directories:
        path = root / name
        if path.is_symlink():
            found.append(path)
            continue
        for directory, dir_names, file_names in os.walk(path):
            for entry in dir_names + file_names:
                entry_path = Path(directory) / entry
                if entry_path.is_symlink():
                    found.append(entry_path)
    return sorted(found)
