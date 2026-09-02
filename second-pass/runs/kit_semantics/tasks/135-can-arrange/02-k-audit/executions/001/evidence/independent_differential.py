"""Reviewer-authored differential for HumanEval 135.

The trusted canonical implementation is used as a helper witness.  The
docstring's literal predicate, not canonical equality, is the contract oracle.
"""

from __future__ import annotations

import importlib.util
import itertools
import math
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/135-can-arrange")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


candidate = load_module("audited_solution", SCRATCH / "solution.py")
canonical = load_module("trusted_canonical", SCRATCH / "trusted-canonical.py")


def capture(function, array):
    try:
        return ("return", function(array))
    except Exception as err:
        return ("raise", type(err).__name__)


def literal_docstring_oracle(array):
    result = -1
    for index in range(1, len(array)):
        if not array[index] >= array[index - 1]:
            result = index
    return result


cases = [
    ("doc-example-descent", [1, 2, 4, 3, 5]),
    ("doc-example-sorted", [1, 2, 3]),
    ("empty", []),
    ("singleton-int", [8]),
    ("singleton-none", [None]),
    ("two-increasing", [1, 2]),
    ("two-decreasing", [2, 1]),
    ("descent-at-first-branch", [2, 1, 3]),
    ("descent-at-last-branch", [1, 3, 2]),
    ("multiple-descents-largest-wins", [5, 4, 3, 2]),
    ("mixed-bool-int-float", [False, 2, 1.5, True]),
    ("strings", ["alpha", "zeta", "beta"]),
    ("infinities", [float("-inf"), 0.0, float("inf")]),
    ("nan-middle", [1.0, float("nan"), 2.0]),
    ("nan-first", [float("nan"), 1.0]),
    ("nested-lists", [[1, 2], [1, 3], [0]]),
    ("nested-tuples", [(1, 2), (1, 3), (0,)]),
    ("incomparable-sets", [{1}, {2}]),
    ("type-error-pair", [None, None]),
]

# Exhaust every branch pattern for distinct small integers through length six.
pool = (-3, -2, -1, 0, 1, 2, 3)
for length in range(7):
    for values in itertools.permutations(pool, length):
        cases.append((f"int-permutation-{length}", list(values)))

# Deterministic representative generated inputs over the other natural classes.
rng = random.Random(135_20260730)
strings = ["", "A", "a", "aa", "b", "z", "é", "Ω"]
for _ in range(1000):
    length = rng.randrange(0, len(strings) + 1)
    cases.append(("generated-strings", rng.sample(strings, length)))

numeric = [False, True, -10, -2, 0, 3, 11, -4.5, -0.25, 2.5, 12.75,
           float("-inf"), float("inf")]
for _ in range(2000):
    shuffled = list(numeric)
    rng.shuffle(shuffled)
    chosen = []
    for value in shuffled:
        if not any(value == old for old in chosen):
            chosen.append(value)
        if len(chosen) == rng.randrange(0, 9):
            break
    cases.append(("generated-mixed-numeric", chosen))

candidate_contract_mismatches = []
canonical_differences = []
for label, array in cases:
    actual = capture(candidate.can_arrange, array)
    expected = capture(literal_docstring_oracle, array)
    helper = capture(canonical.can_arrange, array)
    if actual != expected:
        candidate_contract_mismatches.append((label, array, expected, actual))
    if actual != helper:
        canonical_differences.append((label, array, helper, actual))

assert candidate.can_arrange([1, 2, 4, 3, 5]) == 3
assert candidate.can_arrange([1, 2, 3]) == -1

print("case_count", len(cases))
print("candidate_contract_mismatches", len(candidate_contract_mismatches))
print("candidate_vs_canonical_differences", len(canonical_differences))
for difference in canonical_differences[:12]:
    label, array, helper, actual = difference
    print("DIFFERENCE", label, repr(array), "canonical=", helper,
          "candidate=", actual)

if candidate_contract_mismatches:
    for mismatch in candidate_contract_mismatches[:12]:
        print("CONTRACT_MISMATCH", mismatch)
    raise SystemExit(1)
