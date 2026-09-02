#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval/74."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.total_match


canonical = load_function(Path("/tmp/audit-work/74-total-match/canonical.py"), "trusted_canonical")
generated = load_function(Path("/tmp/audit-work/74-total-match/solution.py"), "generated_solution")

documented = [
    ([], []),
    (["hi", "admin"], ["hI", "Hi"]),
    (["hi", "admin"], ["hi", "hi", "admin", "project"]),
    (["hi", "admin"], ["hI", "hi", "hi"]),
    (["4"], ["1", "2", "3", "4", "5"]),
]
branch_boundaries = [
    ([], [""]),
    ([""], []),
    (["a"], ["b"]),
    (["a"], [""]),
    ([""], ["a"]),
    (["ab"], ["x", "y"]),
    (["é"], ["a"]),
    (["🙂"], ["x"]),
    (["a\x00b"], ["xyz"]),
    (["x" * 1000], ["y" * 999]),
]

atoms = ("", "a", "bc", "é", "🙂")
small_lists: list[list[str]] = []
for size in range(4):
    small_lists.extend([list(items) for items in itertools.product(atoms, repeat=size)])

rng = random.Random(740074)
alphabet = ["a", "Z", "é", "🙂", "\x00"]
random_cases: list[tuple[list[str], list[str]]] = []
for _ in range(2000):
    pair: list[list[str]] = []
    for _side in range(2):
        strings = []
        for _item in range(rng.randrange(0, 9)):
            strings.append(
                "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 25)))
            )
        pair.append(strings)
    random_cases.append((pair[0], pair[1]))

cases = (
    [("documented", left, right) for left, right in documented]
    + [("boundary", left, right) for left, right in branch_boundaries]
    + [
        ("exhaustive-small", left, right)
        for left, right in itertools.product(small_lists, repeat=2)
    ]
    + [("generated", left, right) for left, right in random_cases]
)

mismatches = []
branch_counts = {"first": 0, "second": 0, "equal": 0}
for group, left, right in cases:
    expected = canonical(left, right)
    actual = generated(left, right)
    if sum(map(len, left)) == sum(map(len, right)):
        branch_counts["equal"] += 1
    if actual is left:
        branch_counts["first"] += 1
    elif actual is right:
        branch_counts["second"] += 1
    else:
        mismatches.append((group, left, right, "generated returned neither input"))
        continue
    if actual is not expected or actual != expected:
        mismatches.append((group, left, right, expected, actual))

print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(branch_boundaries)}")
print(f"exhaustive_small_cases={len(small_lists) ** 2}")
print(f"generated_cases={len(random_cases)}")
print(f"total_cases={len(cases)}")
print(f"branch_counts={branch_counts}")
print("witness_equal=(['a'], ['b']) -> first")
print("witness_first_shorter=([''], ['a']) -> first")
print("witness_second_shorter=(['a'], ['']) -> second")
print(f"mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:10]:
        print(repr(mismatch))
    raise SystemExit(1)
