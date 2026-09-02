#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval 26.

Input scope:
* all lists of lengths 0..6 over {-2, -1, 0, 1, 2};
* fixed documented/boundary/branch cases below;
* 2,000 deterministic generated lists, lengths 0..30, values -9..9.

The oracle is the trusted, separately implemented /reference/canonical.py.
The implementation under test is the scratch copy of /candidate/solution.py.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Callable, List


def load_entry(path: Path, module_name: str) -> Callable[[List[int]], List[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_duplicates


trusted = load_entry(
    Path("/tmp/audit-work/trusted/canonical.py"), "trusted_canonical"
)
generated = load_entry(
    Path("/tmp/audit-work/candidate-src/solution.py"), "generated_solution"
)

fixed_cases = [
    [1, 2, 3, 2, 4],                 # documented example
    [],                              # empty boundary
    [0],                             # one occurrence: predicate true
    [0, 0],                          # exactly two: predicate false
    [0, 0, 0],                       # more than two: predicate false
    [1, 2, 1],                       # repeated value around a survivor
    [1, 2, 1, 2],                    # no survivors, interleaved
    [1, 2, 3, 1, 4, 2, 5],          # stable order of several survivors
    [-1, 0, -1, 2],                  # negatives and zero
    [-(2**100), 0, 2**100, 0],       # unbounded Python integers
    [7] * 50,                        # high multiplicity
    list(range(-20, 21)),            # all unique
]

checked = 0
mismatches = []


def check(xs: List[int], source: str) -> None:
    global checked
    expected = trusted(xs)
    actual = generated(xs)
    checked += 1
    if expected != actual:
        mismatches.append(
            {"source": source, "input": xs, "canonical": expected, "generated": actual}
        )


for index, case in enumerate(fixed_cases):
    check(case, f"fixed[{index}]")

example_actual = generated([1, 2, 3, 2, 4])
if example_actual != [1, 3, 4]:
    raise AssertionError(f"documented example returned {example_actual!r}")

alphabet = [-2, -1, 0, 1, 2]
exhaustive_count = 0
for length in range(7):
    for values in itertools.product(alphabet, repeat=length):
        check(list(values), f"exhaustive-length-{length}")
        exhaustive_count += 1

rng = random.Random(260026)
random_count = 2_000
for index in range(random_count):
    length = rng.randint(0, 30)
    check([rng.randint(-9, 9) for _ in range(length)], f"random[{index}]")

print("oracle=/tmp/audit-work/trusted/canonical.py:remove_duplicates")
print("subject=/tmp/audit-work/candidate-src/solution.py:remove_duplicates")
print(f"fixed_cases={len(fixed_cases)}")
print(f"exhaustive_alphabet={alphabet}")
print("exhaustive_lengths=0..6")
print(f"exhaustive_cases={exhaustive_count}")
print("random_seed=260026")
print(f"random_cases={random_count}")
print("random_lengths=0..30")
print("random_values=-9..9")
print(f"total_cases={checked}")
print(f"mismatches={len(mismatches)}")

if mismatches:
    for mismatch in mismatches[:20]:
        print(mismatch)
    raise SystemExit(1)
