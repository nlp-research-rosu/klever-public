#!/usr/bin/env python3
"""Independent candidate/canonical/contract differential for HumanEval 151."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import random
import sys
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[Any]], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.double_the_difference


def contract_oracle(values: list[Any]) -> int:
    # The direct reading of "positive odd integers"; bool follows CPython's
    # isinstance(..., int), matching both submitted Python programs.
    return sum(x * x for x in values if isinstance(x, int) and x > 0 and x % 2 == 1)


def same(left: Any, right: Any) -> bool:
    if isinstance(left, float) and isinstance(right, float):
        if math.isnan(left) and math.isnan(right):
            return True
    return left == right


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_151")
    candidate = load_entry(
        Path("/tmp/audit-work/candidate-src/solution.py"), "generated_solution_151"
    )

    named: list[tuple[str, list[Any]]] = [
        ("example-1", [1, 3, 2, 0]),
        ("example-2", [-1, -2, 0]),
        ("example-3", [9, -2]),
        ("example-4", [0]),
        ("empty", []),
        ("negative-odd-boundary", [-3]),
        ("negative-even-boundary", [-2]),
        ("zero-boundary", [0]),
        ("positive-even-boundary", [2]),
        ("positive-odd-boundary", [1]),
        ("branch-mix", [-3, -2, -1, 0, 1, 2, 3]),
        ("ordinary-floats", [-3.5, -2.0, 0.0, 1.0, 1.5, 3.0]),
        ("bool-python-boundary", [False, True]),
        ("large-integers", [-(10**60 + 1), 10**60, 10**60 + 1]),
        ("scientific-small-float", [1e-5]),
        ("positive-infinity", [float("inf")]),
        ("not-a-number", [float("nan")]),
    ]

    rng = random.Random(151)
    atoms: list[Any] = [
        -10**20 - 1,
        -101,
        -3,
        -2,
        -1,
        0,
        1,
        2,
        3,
        99,
        100,
        10**20 + 1,
        -3.5,
        -2.0,
        -0.25,
        0.0,
        0.25,
        1.0,
        1.5,
        1e-5,
        True,
        False,
    ]
    random_cases = [
        [rng.choice(atoms) for _ in range(rng.randrange(0, 13))]
        for _ in range(2500)
    ]

    candidate_contract_mismatches: list[tuple[str, list[Any], Any, Any]] = []
    candidate_canonical_mismatches: list[tuple[str, list[Any], Any, Any]] = []

    for name, values in named + [(f"generated-{i}", case) for i, case in enumerate(random_cases)]:
        got = candidate(values)
        expected_contract = contract_oracle(values)
        expected_canonical = canonical(values)
        if not same(got, expected_contract):
            candidate_contract_mismatches.append((name, values, got, expected_contract))
        if not same(got, expected_canonical):
            candidate_canonical_mismatches.append((name, values, got, expected_canonical))

    print(f"documented_and_boundary_cases={len(named)}")
    for name, values in named:
        print(
            f"{name}: input={values!r} candidate={candidate(values)!r} "
            f"canonical={canonical(values)!r} contract={contract_oracle(values)!r}"
        )
    print(f"generated_cases={len(random_cases)} seed=151 max_length=12")
    print(f"candidate_contract_mismatches={len(candidate_contract_mismatches)}")
    print(f"candidate_canonical_mismatches={len(candidate_canonical_mismatches)}")
    for mismatch in candidate_contract_mismatches[:20]:
        print(f"CONTRACT_MISMATCH {mismatch!r}")
    for mismatch in candidate_canonical_mismatches[:20]:
        print(f"CANONICAL_MISMATCH {mismatch!r}")

    # The candidate must satisfy the stated contract. Canonical-only mismatches
    # remain visible for audit judgment but do not make this script fail.
    return 0 if not candidate_contract_mismatches else 1


if __name__ == "__main__":
    sys.exit(main())
