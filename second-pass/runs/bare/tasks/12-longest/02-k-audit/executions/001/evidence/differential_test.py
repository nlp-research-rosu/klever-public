#!/usr/bin/env python3
"""Independent differential test for HumanEval 12-longest.

Oracle: /reference/canonical.py copied byte-for-byte into the isolated work
directory. Subject: the candidate solution.py copied into that directory.
Domain: finite Python lists whose elements are Python strings.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Callable, Optional


WORK = Path("/tmp/audit-work/12-longest-audit")


def load_longest(path: Path, module_name: str) -> Callable[[list[str]], Optional[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.longest


canonical = load_longest(WORK / "canonical.py", "trusted_canonical")
candidate = load_longest(WORK / "solution.py", "candidate_solution")

directed: list[list[str]] = [
    [],                              # empty branch
    [""],                            # singleton / empty string
    ["a"],                           # singleton / nonempty string
    ["a", "b", "c"],                 # documented equal-length tie
    ["a", "bb", "ccc"],              # documented repeated growth
    ["a", "bbb", "cc"],              # growth then shorter
    ["aa", "b", "cc"],               # later tie must not replace first
    ["", "a"],                       # strict comparison true boundary
    ["a", ""],                       # strict comparison false boundary
    ["", ""],                        # equal zero lengths
    ["ab", "cd", "e", "fg"],         # several equal maxima
    ["é", "e\u0301", "😀😀", "zz"],  # Unicode/code-point lengths and tie
    ["\x00", "\n\n", "\t"],          # control characters are ordinary str
]

pool = ["", "a", "b", "aa", "bb", "abc", "é", "e\u0301", "😀"]
exhaustive = [
    list(items)
    for length in range(5)
    for items in itertools.product(pool, repeat=length)
]

rng = random.Random(120012)
alphabet = ["a", "b", "c", "é", "😀", "\u0301", "\x00"]
generated: list[list[str]] = []
for _ in range(2000):
    count = rng.randrange(0, 13)
    generated.append(
        [
            "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 17)))
            for _ in range(count)
        ]
    )

cases = directed + exhaustive + generated
mismatches: list[tuple[int, list[str], object, object]] = []
for index, strings in enumerate(cases):
    expected = canonical(strings)
    actual = candidate(strings)
    if expected != actual:
        mismatches.append((index, strings, expected, actual))

print("oracle=/tmp/audit-work/12-longest-audit/canonical.py")
print("subject=/tmp/audit-work/12-longest-audit/solution.py")
print(f"directed_cases={len(directed)}")
print("exhaustive_scope=all lists of length 0..4 over a fixed 9-string pool")
print(f"exhaustive_cases={len(exhaustive)}")
print("generated_scope=2000 seed-120012 lists, length 0..12, strings length 0..16")
print(f"generated_cases={len(generated)}")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
for row in mismatches[:20]:
    print("MISMATCH", repr(row))

for strings in directed:
    print(
        "DIRECTED",
        repr(strings),
        "canonical=",
        repr(canonical(strings)),
        "candidate=",
        repr(candidate(strings)),
    )

if mismatches:
    raise SystemExit(1)
print("DIFFERENTIAL_RESULT=PASS")
