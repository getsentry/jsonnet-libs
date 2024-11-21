from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from contextlib import contextmanager
from importlib.resources import as_file
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Generator
from typing import Optional


class PathEntry(ABC):
    """
    Abstracts a path entry to take library from when running `jsonnet`.

    It is a class so that we can provide multiple sources types, like
    file system directories or python packages.

    TODO: Consider changing the abstraction we rely on in the `jsonnet`
    function. That is designed to obtain a path, it then load the content.
    A better abstraction would be for the PathEntry to return the content,
    though it requires changing the public callback interface.
    """

    @contextmanager
    @abstractmethod
    def get_physical_path(
        self, local_path: Path
    ) -> Generator[Optional[Path], None, None]:
        """
        Yields a path object that the `jsonnet` function can use to load the
        content.
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

    @contextmanager
    def get_physical_path(
        self, local_path: Path
    ) -> Generator[Optional[Path], None, None]:
        full_path = self.__root / local_path
        if full_path.exists() and full_path.is_file():
            yield full_path
        else:
            yield None


class PythonPackagePathEntry(PathEntry):
    """
    This relies on `importlib.resources` to retrieve static resources from a
    python package.
    """

    def __init__(self, root: Traversable, subdir: str = "") -> None:
        self.__traversable = root / subdir

    @contextmanager
    def get_physical_path(
        self, local_path: Path
    ) -> Generator[Optional[Path], None, None]:
        file_path = self.__traversable / str(local_path)
        if not file_path.is_file():
            yield None
        else:
            with as_file(file_path) as path:
                yield path
