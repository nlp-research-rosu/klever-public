#!/usr/bin/env python3
"""Independent differential and branch-boundary tests for 25-factorize."""

from __future__ import annotations

import importlib.util
import math
import random
import sys
from pathlib import Path
from typing import Any, Callable

CANONICAL_PATH = Path("/tmp/audit-work/25-factorize-audit/trusted/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/25-factorize-audit/source/solution.py")


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical_module = load_module("trusted_canonical", CANONICAL_PATH)
generated_module = load_module("generated_solution", GENERATED_PATH)
canonical: Callable[[int], list[int]] = canonical_module.factorize
generated: Callable[[int], list[int]] = generated_module.factorize


def outcome(fn: Callable[[int], list[int]], n: int) -> tuple[str, Any]:
    try:
        return ("return", fn(n))
    except Exception as exc:  # The exception class is part of observable behavior.
        return ("raise", type(exc).__name__)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    return all(n % d for d in range(2, math.isqrt(n) + 1))


def contract_holds(n: int, value: list[int]) -> bool:
    return (
        math.prod(value) == n
        and value == sorted(value)
        and all(is_prime(item) for item in value)
    )


documented = [8, 25, 70]
empty_and_public_boundaries = [0, 1, 2, 3, 4, 5]
branch_representatives = [7, 8, 9, 15, 16, 24, 25, 26, 48, 49, 50]
other_fixed = [97, 100, 121, 360, 997, 999, 1024, 65537]
exhaustive = list(range(0, 2049))

rng = random.Random(250723)
generated_sample = [rng.randint(1, 100_000) for _ in range(500)]

# This positive prime is just below one million. Trial division needs about
# 1,000 recursive Python frames, exposing the implementation's CPython stack
# boundary while the iterative canonical implementation returns normally.
recursion_stress = [999_983]

scope = sorted(
    set(
        documented
        + empty_and_public_boundaries
        + branch_representatives
        + other_fixed
        + exhaustive
        + generated_sample
        + recursion_stress
    )
)

print(f"canonical_path={CANONICAL_PATH}")
print(f"generated_path={GENERATED_PATH}")
print("documented_examples=" + repr(documented))
print("empty_and_public_boundaries=" + repr(empty_and_public_boundaries))
print("branch_representatives=" + repr(branch_representatives))
print("other_fixed=" + repr(other_fixed))
print("exhaustive_range=0..2048")
print("random_seed=250723 random_count=500 random_range=1..100000")
print("recursion_stress=" + repr(recursion_stress))
print(f"unique_nonnegative_inputs={len(scope)}")

mismatches: list[tuple[int, tuple[str, Any], tuple[str, Any]]] = []
contract_failures: list[tuple[int, Any]] = []
for value in scope:
    trusted_outcome = outcome(canonical, value)
    generated_outcome = outcome(generated, value)
    if trusted_outcome != generated_outcome:
        mismatches.append((value, trusted_outcome, generated_outcome))
    if value >= 1 and generated_outcome[0] == "return":
        if not contract_holds(value, generated_outcome[1]):
            contract_failures.append((value, generated_outcome[1]))

print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print("MISMATCH " + repr(mismatch))
print(f"generated_contract_failure_count={len(contract_failures)}")
for failure in contract_failures:
    print("CONTRACT_FAILURE " + repr(failure))

# Direct helper tests cover each source branch at its threshold on reachable
# states: n<2, divisor^2>n, divisibility, repeated division, and divisor advance.
helper_cases = {
    (0, 2): [],
    (1, 2): [],
    (2, 2): [2],
    (3, 2): [3],
    (4, 2): [2, 2],
    (5, 2): [5],
    (8, 2): [2, 2, 2],
    (25, 2): [5, 5],
    (25, 3): [5, 5],
    (25, 4): [5, 5],
    (25, 5): [5, 5],
}
helper_failures: list[tuple[tuple[int, int], Any, Any]] = []
for args, expected in helper_cases.items():
    actual = generated_module.factorize_from(*args)
    if actual != expected:
        helper_failures.append((args, expected, actual))
print("helper_cases=" + repr(helper_cases))
print(f"helper_failure_count={len(helper_failures)}")
for failure in helper_failures:
    print("HELPER_FAILURE " + repr(failure))

# Negative integers are recorded separately because the trusted implementation
# raises from math.sqrt while the generated function returns an empty list.
negative_probes = [-4, -1]
print("negative_probes=" + repr(negative_probes))
for value in negative_probes:
    print(
        f"NEGATIVE n={value} canonical={outcome(canonical, value)!r} "
        f"generated={outcome(generated, value)!r}"
    )

if mismatches or contract_failures or helper_failures:
    sys.exit(1)

