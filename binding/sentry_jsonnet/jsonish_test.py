from __future__ import annotations

from typing import Any

from sentry_jsonnet.jsonish import JSONish
from sentry_jsonnet.jsonish import recurse


def jsonish_lower(x: JSONish, _: Any):
    if isinstance(x, str):
        return x.lower()
    else:
        return NotImplemented


def jsonish_add_one(x: JSONish, _: Any):
    if isinstance(x, (float, int)):
        return x + 1
    else:
        return NotImplemented


def jsonish_path(x: JSONish, path: Any):
    if isinstance(x, (dict, list)):
        return NotImplemented

    from pathlib import Path

    return str(Path("/", *(str(segment) for segment in path)))


def jsonish_reverse(x: JSONish, _: Any):
    if isinstance(x, list):
        return list(reversed(x))
    else:
        return NotImplemented


def jsonish_pairs(x: JSONish, _: Any):
    if isinstance(x, dict):
        return [list(item) for item in x.items()]
    else:
        return NotImplemented


class DescribeRecurse:
    def it_can_lowercase(self):
        json: JSONish = ["Aa", {"Bb": "Bb", "Cc": ["Dd", "ee", "FF"]}]
        expected = ["aa", {"Bb": "bb", "Cc": ["dd", "ee", "ff"]}]
        actual = recurse(json, [jsonish_lower])
        assert actual == expected

    def it_operates_on_correct_type_only(self):
        json: JSONish = {"Bb": -1.5, "Cc": ["Dd", 1, "FF"]}
        expected: JSONish = {"Bb": -0.5, "Cc": ["Dd", 2, "FF"]}
        actual = recurse(json, [jsonish_add_one])
        assert actual == expected

    def it_provides_each_values_jsonpath(self):
        json: JSONish = {"Bb": -1.5, "Cc": ["Dd", 1, "FF"]}
        expected = {"Bb": "/Bb", "Cc": ["/Cc/0", "/Cc/1", "/Cc/2"]}
        actual = recurse(json, [jsonish_path])
        assert actual == expected

    def it_can_modify_lists(self):
        json: JSONish = {".": [0, 1, [[2, 3], 4, 5], 6]}
        expected = {".": [6, [5, 4, [3, 2]], 1, 0]}
        actual = recurse(json, [jsonish_reverse])
        assert actual == expected

    def it_can_take_multiple_passes(self):
        json: JSONish = {".": [0, 1, [[2, 3], 4, 5], 6], "x": -1}
        expected = [[".", [7, [6, 5, [4, 3]], 2, 1]], ["x", 0]]
        actual = recurse(
            json, [jsonish_reverse, jsonish_pairs, jsonish_add_one]
        )
        assert actual == expected

    def it_takes_passes_in_order(self):
        json: JSONish = {".": [0, 1, [[2, 3], 4, 5], 6], "x": -1}
        expected = [["x", 0], [".", [7, [6, 5, [4, 3]], 2, 1]]]
        actual = recurse(
            json, [jsonish_pairs, jsonish_reverse, jsonish_add_one]
        )
        assert actual == expected
