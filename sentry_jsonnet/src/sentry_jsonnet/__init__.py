from __future__ import annotations

from pathlib import Path
from typing import Any
from typing import Callable
from typing import MutableSequence
from typing import Sequence
from typing import TypeVar

from sentry_jsonish import JSONish

from sentry_jsonnet.callbacks import ImportCallback
from sentry_jsonnet.callbacks import JsonnetImportCallback
from sentry_jsonnet.callbacks import default_import_callback
from sentry_jsonnet.callbacks import pathlib_import_callback
from sentry_jsonnet.paths import FilesystemPathEntry
from sentry_jsonnet.paths import PathEntry

JsonnetSnippet = str
VarName = str
BaseDir = Path
AbsPath = Path
T = TypeVar("T")


def _getframe(back: int):
    import sys

    return sys._getframe(back)  # pyright: ignore [reportPrivateUsage]


def jsonnet(
    filename: Path | str,
    src: JsonnetSnippet = None,
    base_dir: AbsPath | str = None,
    caller_frame: int = 1,
    import_paths: Sequence[Path | str | PathEntry] = (),
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

    paths: MutableSequence[PathEntry] = []
    for path in import_paths:
        if isinstance(path, PathEntry):
            paths.append(path)
        else:
            paths.append(FilesystemPathEntry(Path(path)))

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

    _import_callback: JsonnetImportCallback = pathlib_import_callback(
        paths, import_callback
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
