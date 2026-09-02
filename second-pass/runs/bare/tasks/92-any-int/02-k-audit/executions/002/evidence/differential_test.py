#!/usr/bin/env python3
"""Independent differential test for HumanEval 92 any_int."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


class IntSubclass(int):
    pass


def load_function(path: Path, module_name: str) -> Callable[[Any, Any, Any], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.any_int


def outcome(function: Callable[[Any, Any, Any], Any], args: tuple[Any, Any, Any]) -> tuple[str, Any]:
    try:
        return ("return", function(*args))
    except Exception as error:  # pragma: no cover - evidence for discrepancies
        return ("raise", (type(error).__name__, str(error)))


def deduplicate(cases: list[tuple[Any, Any, Any]]) -> list[tuple[Any, Any, Any]]:
    # repr preserves distinct edge classes such as int, bool, Decimal, and a
    # custom int subclass better than Python equality-based set membership.
    result: list[tuple[Any, Any, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for case in cases:
        key = tuple(f"{type(value).__qualname__}:{value!r}" for value in case)
        if key not in seen:
            seen.add(key)
            result.append(case)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical", type=Path)
    parser.add_argument("generated", type=Path)
    args = parser.parse_args()
    canonical = load_function(args.canonical, "trusted_canonical_92")
    generated = load_function(args.generated, "generated_solution_92")

    named_cases: list[tuple[str, tuple[Any, Any, Any]]] = [
        ("example-first-equality", (5, 2, 7)),
        ("example-no-equality", (3, 2, 2)),
        ("example-negative", (3, -2, 1)),
        ("example-noninteger", (3.6, -2.2, 2)),
        ("first-equality-only", (2, 3, 5)),
        ("second-equality-only", (2, 5, 3)),
        ("third-equality-only", (5, 2, 3)),
        ("all-equalities-zero", (0, 0, 0)),
        ("negative-first-equality", (-5, 2, -3)),
        ("large-unbounded-int", (10**100, -(10**100), 0)),
        ("float-position-1", (1.0, 2, 3)),
        ("float-position-2", (1, 2.0, 3)),
        ("float-position-3", (1, 2, 3.0)),
        ("nan", (math.nan, 0, 0)),
        ("positive-infinity", (math.inf, 1, 2)),
        ("bool-position-1", (True, 1, 2)),
        ("bool-position-2", (1, True, 2)),
        ("bool-position-3", (1, 2, True)),
        ("all-bool", (True, False, True)),
        ("int-subclass-position-1", (IntSubclass(1), 1, 2)),
        ("int-subclass-position-2", (1, IntSubclass(1), 2)),
        ("int-subclass-position-3", (1, 2, IntSubclass(1))),
        ("decimal", (Decimal("1"), 2, 3)),
        ("fraction", (Fraction(1, 1), 2, 3)),
        ("complex", (1 + 0j, 2, 3)),
        ("string-invalid", ("1", 2, 3)),
        ("none-invalid", (None, 2, 3)),
    ]

    generated_cases: list[tuple[Any, Any, Any]] = []
    generated_cases.extend(itertools.product(range(-5, 6), repeat=3))
    boundaries = [
        -(10**100),
        -(2**63),
        -(2**31),
        -1,
        0,
        1,
        2**31 - 1,
        2**63 - 1,
        10**100,
    ]
    generated_cases.extend(itertools.product(boundaries, repeat=3))
    mixed_pool: list[Any] = [
        -2,
        -1,
        0,
        1,
        2,
        -2.5,
        -0.0,
        0.0,
        1.0,
        2.5,
        math.inf,
        -math.inf,
        math.nan,
        False,
        True,
    ]
    generated_cases.extend(itertools.product(mixed_pool, repeat=3))
    generated_cases.extend(
        itertools.product(
            [IntSubclass(-1), IntSubclass(0), IntSubclass(1), -1, 0, 1],
            repeat=3,
        )
    )
    generated_cases = deduplicate(generated_cases)

    mismatches: list[
        tuple[str, tuple[Any, Any, Any], tuple[str, Any], tuple[str, Any]]
    ] = []
    named_by_key = {
        tuple(f"{type(value).__qualname__}:{value!r}" for value in case): name
        for name, case in named_cases
    }
    all_cases = deduplicate([case for _, case in named_cases] + generated_cases)
    for case in all_cases:
        canonical_outcome = outcome(canonical, case)
        generated_outcome = outcome(generated, case)
        if canonical_outcome != generated_outcome:
            key = tuple(f"{type(value).__qualname__}:{value!r}" for value in case)
            mismatches.append(
                (
                    named_by_key.get(key, "generated"),
                    case,
                    canonical_outcome,
                    generated_outcome,
                )
            )

    print("oracle=/reference/canonical.py:any_int")
    print("subject=/tmp/audit-work/92-any-int/candidate/solution.py:any_int")
    print(f"named_cases={len(named_cases)}")
    for name, case in named_cases:
        print(
            f"NAMED {name}: args={case!r} canonical={outcome(canonical, case)!r} "
            f"generated={outcome(generated, case)!r}"
        )
    print(f"generated_unique_cases={len(generated_cases)}")
    print(f"total_unique_cases={len(all_cases)}")
    print(f"mismatch_count={len(mismatches)}")
    for index, mismatch in enumerate(mismatches[:120], 1):
        name, case, canonical_outcome, generated_outcome = mismatch
        print(
            f"MISMATCH {index}: class={name} args={case!r} "
            f"types={tuple(type(value).__qualname__ for value in case)!r} "
            f"canonical={canonical_outcome!r} generated={generated_outcome!r}"
        )
    if len(mismatches) > 120:
        print(f"MISMATCHES_OMITTED={len(mismatches) - 120}")

    # Mismatches are preserved as audit evidence and assessed by source-domain
    # analysis in REVIEW.md; test execution itself succeeds when all cases run.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
