#!/usr/bin/env python3
"""Independent candidate/canonical/contract differential for HumanEval 37."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Any, Callable


def load_function(path: Path, module_name: str) -> Callable[[list[Any]], list[Any]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_even


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_function(
    Path("/tmp/audit-work/37-sort-even/solution.py"), "generated_candidate"
)


def contract(source: list[Any], result: list[Any]) -> bool:
    return (
        len(result) == len(source)
        and result[1::2] == source[1::2]
        and result[::2] == sorted(source[::2])
    )


checked = 0


def check(case: list[Any], label: str | None = None) -> None:
    global checked
    canonical_input = list(case)
    candidate_input = list(case)
    expected = canonical(canonical_input)
    actual = candidate(candidate_input)
    assert canonical_input == case, ("canonical mutated input", case, canonical_input)
    assert candidate_input == case, ("candidate mutated input", case, candidate_input)
    assert actual == expected, ("differential mismatch", case, expected, actual)
    assert contract(case, actual), ("contract mismatch", case, actual)
    checked += 1
    if label:
        print(f"{label}: {case!r} -> {actual!r}")


boundary_cases = [
    ("empty", []),
    ("singleton", [4]),
    ("pair-ordered", [1, 9]),
    ("pair-any-odd", [4, -9]),
    ("first-prompt", [1, 2, 3]),
    ("second-prompt", [5, 6, 3, 4]),
    ("equal-even-values", [2, 8, 2, -4]),
    ("ordered-even-values", [-3, 1, 0, 2, 4]),
    ("reversed-even-values", [4, 1, 0, 2, -3]),
    ("odd-length", [9, 8, -1, 7, 3]),
    ("even-length", [9, 8, -1, 7, 3, 6]),
    ("negative-and-duplicate", [-1, 7, -3, 6, 0, 5, -3]),
]
for boundary_label, boundary_case in boundary_cases:
    check(boundary_case, boundary_label)

# Exhaust all integer lists through length 7 over a five-value alphabet.  This
# exercises both outcomes of each equality/order branch at every recursion depth.
alphabet = (-2, -1, 0, 1, 2)
for length in range(8):
    for values in itertools.product(alphabet, repeat=length):
        check(list(values))
print(f"exhaustive_integer_cases={sum(len(alphabet) ** n for n in range(8))}")

# A deterministic broader sample covers longer lists and wider integer values.
rng = random.Random(370037)
for _ in range(1000):
    length = rng.randrange(0, 41)
    check([rng.randrange(-10_000, 10_001) for _ in range(length)])
print("random_seed=370037 random_cases=1000 lengths=0..40 values=-10000..10000")

# The natural-language signature says only `list`; these homogeneous orderable
# values show behavior that the Python program and canonical implementation
# support even though the generated K runtime is integer-specific.
generic_cases = [
    ["b", "odd", "a"],
    ["z", "x", "m", "y", "a"],
    [2.5, 99.0, -1.25, 0.0],
    [True, False, False],
]
for index, generic_case in enumerate(generic_cases, 1):
    check(generic_case, f"generic-orderable-{index}")

print(f"total_cases={checked} mismatches=0 contract_failures=0")
