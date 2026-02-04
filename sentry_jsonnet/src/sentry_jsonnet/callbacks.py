from __future__ import annotations

from pathlib import Path
from typing import Callable
from typing import Dict
from typing import Sequence
from typing import Tuple
from typing import Union

from sentry_jsonnet.paths import FilesystemPathEntry
from sentry_jsonnet.paths import PathEntry


class unset:
    pass


ImportCache = Dict[Path, Union[bytes, None]]
ImportCallback = Callable[[Path], Union[str, bytes, None]]
# jsonnet cpython binding requires this more complex signature
JsonnetImportCallback = Callable[[str, str], Tuple[str, Union[bytes, None]]]


# Returns contents if the file was successfully retrieved,
# None if file not found, or throws an exception when the path is invalid or an
# IO error occured.
def default_import_callback(module: Path):
    if module.is_file():
        content = module.read_text()
    elif module.exists():
        raise RuntimeError("Attempted to import a directory")
    else:  # cache the import-path miss
        content = None
    return content


def caching_import_callback(
    cache: ImportCache, import_callback: ImportCallback, path: Path
) -> tuple[str, bytes | None]:
    _source = cache.get(path, unset())
    if isinstance(_source, unset):
        source = import_callback(path)
        if isinstance(source, str):
            _source = source.encode("utf-8")
        else:
            _source = source
        cache[path] = _source

    return str(path), _source


# It caches both hits and misses in the `cache` dict. Exceptions
# do not need to be cached, because they abort the computation anyway.
def pathlib_import_callback(
    import_paths: Sequence[PathEntry], import_callback: ImportCallback
) -> JsonnetImportCallback:
    from functools import wraps

    cache: ImportCache = {}

    @wraps(import_callback)
    def _import_callback(
        _base_dir: str, _path: str
    ) -> tuple[str, bytes | None]:
        all_paths: Sequence[PathEntry] = [
            FilesystemPathEntry(Path(_base_dir)),
            *import_paths,
        ]

        for entry in all_paths:
            with entry.get_physical_path(Path(_path)) as p:
                if p is not None:
                    path_tried, content = caching_import_callback(
                        cache, import_callback, p
                    )
                    if content is not None:
                        return path_tried, content

        return path_tried, None

    return _import_callback
