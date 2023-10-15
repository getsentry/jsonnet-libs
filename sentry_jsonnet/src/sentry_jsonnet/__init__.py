from __future__ import annotations

from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import Sequence
from typing import Tuple
from typing import TypeVar
from typing import Union

from sentry_jsonish import JSONish

JsonnetSnippet = str
VarName = str
BaseDir = Path
AbsPath = Path
T = TypeVar("T")

ImportCache = Dict[Path, Union[bytes, None]]
ImportCallback = Callable[[Path], Union[str, bytes, None]]
# jsonnet cpython binding requires this more complex signature
_ImportCallback = Callable[[str, str], Tuple[str, Union[bytes, None]]]


def _getframe(back: int):
    import sys

    return sys._getframe(back)  # pyright: ignore [reportPrivateUsage]


class unset:
    pass


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


def _adapt_import_callback(
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
def _caching_adapted_import_callback(
    import_paths: Sequence[Path], import_callback: ImportCallback
) -> _ImportCallback:
    from functools import wraps

    cache: ImportCache = {}

    @wraps(import_callback)
    def _import_callback(
        _base_dir: str, _path: str
    ) -> tuple[str, bytes | None]:
        path_tried1, content1 = _adapt_import_callback(
            cache, import_callback, Path(_base_dir) / _path
        )
        if content1 is not None:
            return path_tried1, content1

        path = Path(_path)
        for import_path in import_paths:
            path_tried2, content2 = _adapt_import_callback(
                cache, import_callback, import_path / path
            )
            if content2 is not None:
                return path_tried2, content2

        return path_tried1, content1

    return _import_callback


def jsonnet(
    filename: Path | str,
    src: JsonnetSnippet = None,
    base_dir: AbsPath | str = None,
    caller_frame: int = 1,
    import_paths: Sequence[Path | str] = (),
    max_stack: int = 500,
    gc_min_objects: int = 1000,
    gc_growth_trigger: float = 2,
    ext_vars: dict[str, str] = None,
    ext_codes: dict[str, JsonnetSnippet] = None,
    tla_vars: dict[str, str] = None,
    tla_codes: dict[str, JsonnetSnippet] = None,
    max_trace: int = 20,
    import_callback: ImportCallback = default_import_callback,
    native_callbacks: dict[
        str, tuple[tuple[str, ...], Callable[..., Any]]
    ] = None,
) -> JSONish:
    if base_dir is None:
        # this choice of default base_dir makes all paths source-relative
        _caller_frame = _getframe(caller_frame + 1)
        base_dir = Path(_caller_frame.f_code.co_filename).parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)
    assert base_dir.is_absolute(), base_dir

    _filename = str(base_dir / filename)

    import_paths = [base_dir / path for path in import_paths]
    _jpathdir = [str(path) for path in import_paths]

    if ext_vars is None:
        ext_vars = {}
    if ext_codes is None:
        ext_codes = {}
    if tla_vars is None:
        tla_vars = {}
    if tla_codes is None:
        tla_codes = {}

    _import_callback: _ImportCallback = _caching_adapted_import_callback(
        import_paths, import_callback
    )

    if native_callbacks is None:
        native_callbacks = {}

    import _jsonnet

    if src is None:
        result = _jsonnet.evaluate_file(
            _filename,
            _jpathdir,  # XXX: unused when passing import_callback
            max_stack,
            gc_min_objects,
            gc_growth_trigger,
            ext_vars,
            ext_codes,
            tla_vars,
            tla_codes,
            max_trace,
            _import_callback,
            native_callbacks,
        )
    else:
        result = jsonnet.evaluate_snippet(
            _filename,
            src,
            _jpathdir,  # XXX: unused when passing import_callback
            max_stack,
            gc_min_objects,
            gc_growth_trigger,
            ext_vars,
            ext_codes,
            tla_vars,
            tla_codes,
            max_trace,
            _import_callback,
            native_callbacks,
        )

    import json

    return json.loads(result)
