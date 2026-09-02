#!/usr/bin/env python3
"""Independent differential test for HumanEval 7.

Oracle: /reference/canonical.py.
Candidate implementation: the source copied to fresh scratch from /candidate.
Scope: documented examples; named branch/boundary cases; exhaustive strings
over {"a", "b"} through length 2, lists through length 3; and 2,000
deterministic generated Unicode-containing cases.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[str], str], list[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_substring


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(
    Path("/tmp/audit-work/7-filter-by-substring/candidate/solution.py"),
    "generated_solution",
)

named_cases: list[tuple[list[str], str, list[str]]] = [
    ([], "a", []),
    (["abc", "bacd", "cde", "array"], "a", ["abc", "bacd", "array"]),
    ([], "", []),
    ([""], "", [""]),
    (["", "a", "bb"], "", ["", "a", "bb"]),
    (["abc"], "abc", ["abc"]),
    (["abc"], "abcd", []),
    (["abc"], "a", ["abc"]),
    (["abc"], "b", ["abc"]),
    (["abc"], "c", ["abc"]),
    (["abc"], "z", []),
    (["aaaa"], "aa", ["aaaa"]),
    (["A", "a"], "a", ["a"]),
    (["x", "x", "y"], "x", ["x", "x"]),
    (["naïve", "🙂x", "x🙂", "\x00"], "🙂", ["🙂x", "x🙂"]),
    (["\x00", "a\x00b"], "\x00", ["\x00", "a\x00b"]),
]

checked = 0
for strings, substring, expected in named_cases:
    c = canonical(strings, substring)
    g = generated(strings, substring)
    assert c == expected, (strings, substring, c, expected)
    assert g == c, (strings, substring, g, c)
    checked += 1

small_strings = [
    "".join(chars)
    for length in range(3)
    for chars in itertools.product("ab", repeat=length)
]
for list_length in range(4):
    for strings_tuple in itertools.product(small_strings, repeat=list_length):
        strings = list(strings_tuple)
        for substring in small_strings:
            c = canonical(strings, substring)
            g = generated(strings, substring)
            assert g == c, (strings, substring, g, c)
            checked += 1

rng = random.Random(0x7F17E2)
alphabet = ["", "a", "b", "A", "é", "🙂", "\x00", "中"]
for _ in range(2000):
    strings = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(9)))
        for _ in range(rng.randrange(9))
    ]
    substring = "".join(rng.choice(alphabet) for _ in range(rng.randrange(5)))
    c = canonical(strings, substring)
    g = generated(strings, substring)
    assert g == c, (strings, substring, g, c)
    checked += 1

print(f"named_cases={len(named_cases)}")
print(f"small_strings={small_strings!r}")
print("generated_seed=0x7F17E2 generated_cases=2000")
print(f"total_cases={checked} mismatches=0")
