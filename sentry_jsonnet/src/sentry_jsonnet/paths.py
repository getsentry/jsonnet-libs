from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Optional


class PathEntry(ABC):
    """
    Abstracts a path entry to take library from when running `jsonnet`.

    It is a class so that we can provide multiple sources types, like
    file system directories or python packages.
    """

    @abstractmethod
    def get_physical_path(self, local_path: Path) -> Optional[Path]:
        """
        Opens a file from the path represented by this object and returns the
        content of the file if the file is present.

        If the file is not present in this path, it returns None.
        """
        raise NotImplementedError


class FilesystemPathEntry(PathEntry):
    """
    The traditional path entry that represents a directory on the file
    system.

    If a required file is a subpath of the one provided to initialize
    this object it is returned.
    """

    def __init__(self, root: Path) -> None:
        self.__root = root

    def get_physical_path(self, local_path: Path) -> Optional[Path]:
        full_path = self.__root / local_path
        if full_path.exists() and full_path.is_file():
            return full_path
        else:
            return None
