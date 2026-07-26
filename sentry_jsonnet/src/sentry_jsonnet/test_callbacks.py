from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Generator
from unittest import mock

import pytest

from sentry_jsonnet.callbacks import caching_import_callback
from sentry_jsonnet.callbacks import default_import_callback
from sentry_jsonnet.callbacks import pathlib_import_callback
from sentry_jsonnet.paths import FilesystemPathEntry


@pytest.fixture
def library() -> Generator[Path, None, None]:
    with tempfile.TemporaryDirectory() as temp_dir:
        subpackage1 = Path(temp_dir) / "package1/subpackage1"
        os.makedirs(subpackage1)
        with open(subpackage1 / "file1.json", "w") as f:
            f.write("{'test1': 1}")

        subpackage2 = Path(temp_dir) / "package2/subpackage2"
        os.makedirs(subpackage2)
        with open(subpackage2 / "file2.json", "w") as f:
            f.write("{'test2': 2}")

        yield Path(temp_dir)


def test_default_import(library) -> None:
    assert (
        default_import_callback(library / "package1/subpackage1/file1.json")
        == "{'test1': 1}"
    )

    assert (
        default_import_callback(library / "package1/subpackage2/file2.json")
        is None
    )


def test_cache(library) -> None:
    mock_callback = mock.Mock()

    cache = {}
    full_path = library / "package1/subpackage1/file1.json"
    assert caching_import_callback(
        cache, default_import_callback, full_path
    ) == (str(full_path), b"{'test1': 1}")

    assert caching_import_callback(cache, mock_callback, full_path) == (
        str(full_path),
        b"{'test1': 1}",
    )
    mock_callback.assert_not_called()


def test_path_support(library) -> None:
    with open(library / "file3.json", "w") as f:
        f.write("{'test3': 3}")

    callback = pathlib_import_callback(
        [
            FilesystemPathEntry(Path(library) / "package1"),
            FilesystemPathEntry(Path(library) / "package2"),
        ],
        default_import_callback,
    )

    assert callback(str(Path(library)), "file3.json") == (
        str(library / "file3.json"),
        b"{'test3': 3}",
    )
    assert callback(str(Path(library)), "subpackage1/file1.json") == (
        str(library / "package1/subpackage1/file1.json"),
        b"{'test1': 1}",
    )
    assert callback(str(Path(library)), "subpackage2/file2.json") == (
        str(library / "package2/subpackage2/file2.json"),
        b"{'test2': 2}",
    )
