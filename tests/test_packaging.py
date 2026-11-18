import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _load_find_symlinks():
    spec = importlib.util.spec_from_file_location(
        "packaging_checks", ROOT / "packaging_checks.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_symlinks


find_symlinks = _load_find_symlinks()


def test_repository_has_no_symlinks_in_packaged_files():
    assert find_symlinks(ROOT) == []


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


@pytest.mark.skipif(not hasattr(os, "symlink"), reason="symlinks are not supported")
@pytest.mark.parametrize(
    "link",
    [
        "tests/link.txt",
        "number_parser/link.txt",
        "number_parser/data/link.py",
        "README.rst",
        "NOTICE",
        "AUTHORS.txt",
    ],
)
def test_find_symlinks_reports_links(tmp_path, link):
    outside = tmp_path / "outside.txt"
    outside.write_text("not part of the repository")
    root = tmp_path / "repo"
    (root / "tests").mkdir(parents=True)
    (root / "number_parser" / "data").mkdir(parents=True)
    (root / "tests" / "test_ok.py").write_text("")
    (root / "number_parser" / "__init__.py").write_text("")
    try:
        (root / link).symlink_to(outside)
    except OSError:
        pytest.skip("cannot create symlinks here")
    assert find_symlinks(root) == [root / link]


@pytest.mark.skipif(not hasattr(os, "symlink"), reason="symlinks are not supported")
def test_find_symlinks_reports_directory_links(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("not part of the repository")
    root = tmp_path / "repo"
    (root / "tests").mkdir(parents=True)
    try:
        (root / "tests" / "linked_dir").symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("cannot create symlinks here")
    assert find_symlinks(root) == [root / "tests" / "linked_dir"]


@pytest.mark.skipif(not hasattr(os, "symlink"), reason="symlinks are not supported")
def test_setup_refuses_to_build_with_a_symlink(tmp_path):
    pytest.importorskip("setuptools")
    root = tmp_path / "repo"
    (root / "number_parser").mkdir(parents=True)
    (root / "tests").mkdir()
    for name in (
        "setup.py",
        "packaging_checks.py",
        "README.rst",
        "CHANGES.rst",
        "number_parser/VERSION",
    ):
        (root / name).write_bytes((ROOT / name).read_bytes())
    outside = tmp_path / "outside.txt"
    outside.write_text("not part of the repository")
    try:
        (root / "tests" / "link.txt").symlink_to(outside)
    except OSError:
        pytest.skip("cannot create symlinks here")
    result = subprocess.run(
        [sys.executable, "setup.py", "--version"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "symbolic links are not allowed" in result.stderr
    assert str(Path("tests") / "link.txt") in result.stderr
