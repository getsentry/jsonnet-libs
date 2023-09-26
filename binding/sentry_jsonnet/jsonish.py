from __future__ import annotations

import typing
from typing import Callable
from typing import Dict
from typing import List
from typing import Sequence
from typing import Tuple
from typing import Union

JSONNumber = Union[int, float]
JSONScalar = Union[None, bool, str, JSONNumber]
JSONDict = Dict[str, "JSONish"]
JSONList = List["JSONish"]
JSONContainer = Union[JSONDict, JSONList]

JSONish = Union[JSONScalar, JSONContainer]

JSONIndex = Union[int, str]
JSONPath = Tuple[JSONIndex, ...]
# NOTE: it's impossible to annotate a `NotImplemented` return value
JSONNormalizer = Callable[[JSONish, JSONPath], JSONish]

NULL: JSONish = typing.cast(JSONish, None)


def recurse(json: JSONish, normalizers: Sequence[JSONNormalizer]) -> JSONish:
    root = [json]

    Stack = List[
        Union[
            Tuple[JSONPath, JSONDict, str, JSONish],
            Tuple[JSONPath, JSONList, int, JSONish],
        ]
    ]
    discover_children: Stack = [((), root, 0, json)]
    norm_children: Stack = []

    while discover_children:
        entry = discover_children.pop()
        path, parent, index, child = entry
        norm_children.append(entry)

        if isinstance(child, list):
            for i, val in enumerate(child):
                entry = (path + (i,), child, i, val)
                discover_children.append(entry)
        elif isinstance(child, dict):
            for key, val in child.items():
                entry = (path + (key,), child, key, val)
                discover_children.append(entry)

    while norm_children:
        entry = norm_children.pop()
        path, parent, index, child = entry
        for norm in normalizers:
            result = norm(child, path)
            if result is not NotImplemented:
                child = result
        if isinstance(parent, dict) and isinstance(index, str):
            parent[index] = child
        elif isinstance(parent, list) and isinstance(index, int):
            parent[index] = child
        else:
            raise AssertionError(type(parent), type(index), parent, index)

    return root[0]


def main():
    import json
    import sys

    def norm_number(x: JSONish, path: JSONPath) -> JSONNumber:
        if isinstance(x, (int, float)):
            y = x + 1
            print(path, x, "->", y)
            return y
        else:
            return NotImplemented

    norm_str_count = 0

    def norm_str(x: JSONish, path: JSONPath) -> str:
        if not isinstance(x, str):
            return NotImplemented

        nonlocal norm_str_count
        norm_str_count = norm_str_count + 1
        if (norm_str_count % 3) == 0:
            y = x.upper()
        elif norm_str_count % 2:
            y = x.lower()
        else:
            y = x
        if x != y:
            print(path, x, "->", y)
        return y

    def norm_list(x: JSONish, _: JSONPath) -> JSONList:
        if not isinstance(x, list):
            return NotImplemented
        return list(reversed(x))

    def norm_dict(x: JSONish, _: JSONPath) -> Union[JSONList, JSONDict]:
        if not isinstance(x, dict):
            return NotImplemented

        len_x = len(x)
        if len_x % 2:
            pairs: JSONList = [list(item) for item in x.items()]
            return pairs
        else:
            x = {"odd-dict": x}
            return x

    normalizers = [norm_number, norm_str, norm_list, norm_dict]

    for arg in sys.argv[1:]:
        data = json.loads(arg)
        data = recurse(data, normalizers)
        print(json.dumps(data))


if __name__ == "__main__":
    exit(main())
