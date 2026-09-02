#!/usr/bin/env python3
"""Independent differential and contract checks for HumanEval/25 factorize."""

from __future__ import annotations

import importlib.util
import math
import random
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


TRUSTED_CANONICAL = Path("/reference/canonical.py")
CANDIDATE_SOLUTION = Path("/tmp/audit-work/25-factorize/solution.py")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function: Any, value: int) -> tuple[str, Any]:
    try:
        return ("return", function(value))
    except BaseException as error:
        return ("raise", (type(error).__name__, str(error)))


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def contract_errors(value: int, result: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(result, list) or any(type(item) is not int for item in result):
        return ["result is not a list of integers"]
    if result != sorted(result):
        errors.append("factors are not nondecreasing")
    if any(not is_prime(item) for item in result):
        errors.append("at least one factor is not prime")
    if math.prod(result) != value:
        errors.append(f"product is {math.prod(result)}, expected {value}")
    return errors


def main() -> int:
    canonical = load_module("trusted_factorize_canonical", TRUSTED_CANONICAL)
    candidate = load_module("generated_factorize_candidate", CANDIDATE_SOLUTION)

    documented = [8, 25, 70]
    branch_boundaries = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        15,
        16,
        17,
        24,
        25,
        26,
        31,
        48,
        49,
        50,
        70,
        97,
        100,
        121,
        169,
        360,
        999,
    ]
    exhaustive_small = list(range(1, 2001))
    generator = random.Random(250025)
    generated = [generator.randint(1, 200_000) for _ in range(300)]
    recursion_boundaries = [999_983, 1_000_003]

    intended_inputs = sorted(
        set(
            documented
            + branch_boundaries
            + exhaustive_small
            + generated
            + recursion_boundaries
        )
    )
    mismatches: list[tuple[int, tuple[str, Any], tuple[str, Any]]] = []
    contract_failures: list[tuple[str, int, list[str]]] = []
    for value in intended_inputs:
        canonical_outcome = outcome(canonical.factorize, value)
        candidate_outcome = outcome(candidate.factorize, value)
        if canonical_outcome != candidate_outcome:
            mismatches.append((value, canonical_outcome, candidate_outcome))
        for implementation, observed in (
            ("canonical", canonical_outcome),
            ("candidate", candidate_outcome),
        ):
            if observed[0] == "return":
                errors = contract_errors(value, observed[1])
                if errors:
                    contract_failures.append((implementation, value, errors))

    print("FORMALIZED SOURCE DOMAIN FOR DIFFERENTIAL: positive Python integers n >= 1")
    print(
        "INPUT SCOPE: documented=3, branch_boundaries="
        f"{len(branch_boundaries)}, exhaustive_small=1..2000, "
        f"seeded_generated=300 seed=250025 range=1..200000, "
        f"recursion_boundaries={recursion_boundaries}"
    )
    print(f"UNIQUE INTENDED INPUTS: {len(intended_inputs)}")
    print(f"RESULT/EXCEPTION MISMATCHES: {len(mismatches)}")
    for value, canonical_outcome, candidate_outcome in mismatches:
        print(
            f"MISMATCH n={value}: canonical={canonical_outcome!r} "
            f"candidate={candidate_outcome!r}"
        )
    print(f"RETURNED-VALUE CONTRACT FAILURES: {len(contract_failures)}")
    for implementation, value, errors in contract_failures[:20]:
        print(
            f"CONTRACT FAILURE implementation={implementation} n={value}: "
            + "; ".join(errors)
        )

    print("OUT-OF-DOMAIN BEHAVIOR (not counted as intended-domain mismatches)")
    for value in (-2, -1, 0):
        print(
            f"n={value}: canonical={outcome(canonical.factorize, value)!r} "
            f"candidate={outcome(candidate.factorize, value)!r}"
        )

    if mismatches or contract_failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
