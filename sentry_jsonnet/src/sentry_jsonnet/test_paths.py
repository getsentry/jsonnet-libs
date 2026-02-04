from __future__ import annotations

import os
import tempfile
from pathlib import Path

from sentry_jsonnet.paths import FilesystemPathEntry


def test_filesystem_paths() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        full_path = Path(temp_dir) / "pathlib" / "subpath"
        os.makedirs(full_path)
        with open(full_path / "file_to_open.json", "w") as f:
            f.write("{}")

        path_entry = FilesystemPathEntry(Path(temp_dir) / "pathlib")
        with path_entry.get_physical_path(
            Path("subpath/file_to_open.json")
        ) as p:
            assert p == full_path / "file_to_open.json"

        with path_entry.get_physical_path(
            Path("subpath/not_existing.json")
        ) as p:
            assert p is None
