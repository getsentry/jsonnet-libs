from typing import Any, Callable

JsonnetSnippet = str
VarName = str
PathStr = str
BaseDir = PathStr
AbsPathStr = PathStr

# https://github.com/google/jsonnet/blob/739d3ec/python/_jsonnet.c#L484-L501
def evaluate_file(
    filename: PathStr,
    jpathdir: PathStr | list[PathStr] = [],
    max_stack: int = 500,
    gc_min_objects: int = 1000,
    gc_growth_trigger: float = 2,
    ext_vars: dict[str, str] = {},
    ext_codes: dict[str, JsonnetSnippet] = {},
    tla_vars: dict[str, str] = {},
    tla_codes: dict[str, JsonnetSnippet] = {},
    max_trace: int = 20,
    import_callback: Callable[
        [BaseDir, PathStr], tuple[AbsPathStr, bytes | None]
    ] = ...,
    native_callbacks: dict[
        str, tuple[tuple[str, ...], Callable[..., Any]]
    ] = {},
) -> str: ...

# https://github.com/google/jsonnet/blob/739d3ec/python/_jsonnet.c#L574-L589
def evaluate_snippet(
    filename: PathStr,
    src: JsonnetSnippet,
    jpathdir: PathStr | list[PathStr] = [],
    max_stack: int = 500,
    gc_min_objects: int = 1000,
    gc_growth_trigger: float = 2,
    ext_vars: dict[str, str] = {},
    ext_codes: dict[str, JsonnetSnippet] = {},
    tla_vars: dict[str, str] = {},
    tla_codes: dict[str, JsonnetSnippet] = {},
    max_trace: int = 20,
    import_callback: Callable[
        [BaseDir, PathStr], tuple[AbsPathStr, bytes | None]
    ] = ...,
    native_callbacks: dict[
        str, tuple[tuple[str, ...], Callable[..., Any]]
    ] = {},
) -> str: ...
