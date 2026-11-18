#!/usr/bin/env python

import sys
from pathlib import Path

from setuptools import find_packages, setup

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from packaging_checks import find_symlinks  # noqa: E402

symlinks = find_symlinks(ROOT)
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
