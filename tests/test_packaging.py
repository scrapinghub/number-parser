import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def test_repository_tracks_no_symlinks():
    git = shutil.which("git")
    if git is None:
        pytest.skip("git is not available")
    try:
        output = subprocess.run(  # noqa: S603
            [git, "ls-files", "-s"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("not a git checkout")
    links = [
        line.split("\t", 1)[1]
        for line in output.splitlines()
        if line.startswith("120000 ")
    ]
    assert links == []
