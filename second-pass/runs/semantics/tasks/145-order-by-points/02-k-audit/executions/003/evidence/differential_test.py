#!/usr/bin/env python3
"""Independent differential test for HumanEval/145.

Scope:
* the two documented examples;
* hand-selected empty, singleton, sign, decimal-boundary, duplicate, and
  stability cases;
* every tuple of length 0..4 over {-20,-11,-10,-1,0,1,10,11,20};
* 2,000 deterministic random lists of length 0..30 with integers selected from
  a mix of [-10^6,10^6] and signed integers with 1..80 decimal digits.

The oracle module and generated module are imported from distinct mounted
source files. No candidate K equations are reused.
"""
from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(Path("/reference/canonical.py"), "trusted_canonical_145")
generated = load(Path("/candidate/solution.py"), "generated_solution_145")

documented = [
    [1, 11, -1, -11, -12],
    [],
]

hand_selected = [
    [0],
    [1],
    [-1],
    [9, 10, 11, 99, 100, 101],
    [-9, -10, -11, -99, -100, -101],
    [0, -1, 1, -10, 10, -11, 11, -20, 20],
    [11, 20, 101, 2, -11, -20, -101, -2],
    [11, 11, -11, -11, 20, 20],
    [10**80 + 123456789, -(10**80 + 123456789), 0],
]

alphabet = (-20, -11, -10, -1, 0, 1, 10, 11, 20)
exhaustive = (
    list(items)
    for length in range(5)
    for items in itertools.product(alphabet, repeat=length)
)

rng = random.Random(145)


def random_integer() -> int:
    if rng.randrange(2) == 0:
        return rng.randint(-10**6, 10**6)
    digits = rng.randint(1, 80)
    value = rng.randrange(10 ** (digits - 1), 10**digits)
    return value if rng.randrange(2) else -value


random_cases = [
    [random_integer() for _ in range(rng.randint(0, 30))]
    for _ in range(2000)
]

checked = 0
mismatches = []
for category, cases in (
    ("documented", documented),
    ("hand_selected", hand_selected),
    ("exhaustive", exhaustive),
    ("random", random_cases),
):
    for case_index, values in enumerate(cases):
        original = list(values)
        expected = canonical.order_by_points(list(values))
        actual = generated.order_by_points(list(values))
        if actual != expected or values != original:
            mismatches.append(
                {
                    "category": category,
                    "case_index": case_index,
                    "input": original,
                    "expected": expected,
                    "actual": actual,
                    "input_after": values,
                }
            )
            if len(mismatches) >= 10:
                break
        checked += 1
    if mismatches:
        break

print("python_version:", sys.version.split()[0])
print("documented_cases:", len(documented))
print("hand_selected_cases:", len(hand_selected))
print("exhaustive_alphabet:", alphabet)
print("exhaustive_lengths:", "0..4")
print("exhaustive_case_count:", sum(len(alphabet) ** n for n in range(5)))
print("random_seed:", 145)
print("random_case_count:", len(random_cases))
print("random_length_range:", "0..30")
print("random_integer_sources:", "[-10^6,10^6] or signed 1..80 digit integers")
print("total_checked:", checked)
print("mismatch_count:", len(mismatches))
if mismatches:
    for mismatch in mismatches:
        print("MISMATCH:", repr(mismatch))
    raise SystemExit(1)
