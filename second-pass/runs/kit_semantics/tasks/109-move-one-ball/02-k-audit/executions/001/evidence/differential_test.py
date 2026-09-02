#!/usr/bin/env python3
"""Independent differential test for HumanEval 109 over its unique-int domain."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/problem-109-independent")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.move_one_ball


canonical = load_entry(SCRATCH / "canonical.py", "trusted_canonical_109")
candidate = load_entry(SCRATCH / "solution.py", "candidate_solution_109")


def rotation_oracle(values: list[int]) -> bool:
    """Directly implement the stated existential right-rotation contract."""
    expected = sorted(values)
    return any(values[-shift:] + values[:-shift] == expected for shift in range(len(values) + 1))


named_cases = [
    ("prompt_true", [3, 4, 5, 1, 2]),
    ("prompt_false", [3, 5, 4, 1, 2]),
    ("empty_branch", []),
    ("singleton", [7]),
    ("two_sorted", [-1, 5]),
    ("two_rotated", [5, -1]),
    ("already_sorted", [-9, 0, 4, 12]),
    ("one_circular_descent_threshold", [4, 12, -9, 0]),
    ("two_circular_descents_rejected", [2, 1, 3]),
    ("three_circular_descents_rejected", [4, 1, 3, 0, 2]),
    ("large_signed_integers", [10**80, -(10**90), 0, 10**40]),
]

mismatches: list[tuple[str, list[int], bool, bool, bool]] = []
checked = 0


def check(label: str, values: list[int], *, verbose: bool = False) -> None:
    global checked
    can = canonical(values.copy())
    got = candidate(values.copy())
    oracle = rotation_oracle(values.copy())
    checked += 1
    if verbose:
        print(f"{label}: input={values!r} canonical={can!r} candidate={got!r} oracle={oracle!r}")
    if can != got or can != oracle:
        mismatches.append((label, values, can, got, oracle))


for label, values in named_cases:
    check(label, values, verbose=True)

exhaustive = 0
for size in range(9):
    for permutation in itertools.permutations(range(size)):
        check(f"permutation_n{size}", list(permutation))
        exhaustive += 1

rng = random.Random(109)
generated = 0
for size in range(9, 41):
    for _ in range(25):
        values = rng.sample(range(-10**7, 10**7), size)
        check(f"generated_n{size}", values)
        generated += 1

print(
    f"summary checked={checked} named={len(named_cases)} "
    f"exhaustive_permutations={exhaustive} generated={generated} mismatches={len(mismatches)}"
)
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    raise SystemExit(1)
