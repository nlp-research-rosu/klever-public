#!/usr/bin/env python3
"""Independent differential test for HumanEval 157.

The trusted oracle and candidate implementation are loaded from the clean
scratch copies whose hashes are recorded in scratch_manifest.log.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Any, Callable


WORK = Path("/tmp/audit-work")


def load_function(path: Path, module_name: str) -> Callable[..., bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.right_angle_triangle


oracle = load_function(WORK / "canonical.py", "trusted_canonical")
candidate = load_function(WORK / "solution.py", "generated_solution")


def outcome(function: Callable[..., Any], args: tuple[Any, ...]) -> tuple[str, Any]:
    try:
        return ("return", function(*args))
    except Exception as error:  # deliberate comparison of empty/mistyped calls
        return ("exception", type(error).__name__)


def compare(label: str, inputs: list[tuple[Any, ...]], show: int = 12) -> int:
    mismatches: list[
        tuple[tuple[Any, ...], tuple[str, Any], tuple[str, Any]]
    ] = []
    for args in inputs:
        trusted_result = outcome(oracle, args)
        candidate_result = outcome(candidate, args)
        if trusted_result != candidate_result:
            mismatches.append((args, trusted_result, candidate_result))
    print(f"{label}: cases={len(inputs)} mismatches={len(mismatches)}")
    for args, trusted_result, candidate_result in mismatches[:show]:
        print(
            f"  mismatch args={args!r} "
            f"canonical={trusted_result!r} candidate={candidate_result!r}"
        )
    return len(mismatches)


def main() -> int:
    documented = [(3, 4, 5), (1, 2, 3)]
    empty_and_arity = [(), (3,), (3, 4)]
    branch_boundaries = [
        (0, 4, 5),       # first non-positive guard boundary
        (-1, 4, 5),      # first non-positive guard below boundary
        (1, 0, 1),       # second guard, with first guard false
        (1, -1, 1),      # second guard below boundary
        (1, 1, 0),       # third guard, earlier guards false
        (1, 1, -1),      # third guard below boundary
        (3, 4, 5),       # first Pythagorean equality
        (3, 5, 4),       # second Pythagorean equality
        (5, 3, 4),       # third Pythagorean equality
        (1, 1, 1),       # final false return
        (6, 8, 10),      # non-primitive equality
        (1, 1, 2),       # degenerate, non-right positive lengths
    ]
    exhaustive_positive = list(itertools.product(range(1, 31), repeat=3))
    rng = random.Random(157)
    random_positive = [
        (rng.randint(1, 10_000), rng.randint(1, 10_000), rng.randint(1, 10_000))
        for _ in range(5_000)
    ]
    nonpositive_boundary_grid = list(itertools.product(range(-10, 11), repeat=3))
    positive_float_cases = [
        (0.3, 0.4, 0.5),
        (1.5, 2.0, 2.5),
        (1.0, 1.0, 2.0),
        (2.2, 3.1, 4.0),
    ]

    results = {
        "documented_examples": compare("documented_examples", documented),
        "empty_and_arity": compare("empty_and_arity", empty_and_arity),
        "branch_boundaries": compare("branch_boundaries", branch_boundaries),
        "exhaustive_positive_int_1_to_30": compare(
            "exhaustive_positive_int_1_to_30", exhaustive_positive
        ),
        "seeded_positive_int_sample": compare(
            "seeded_positive_int_sample", random_positive
        ),
        "nonpositive_boundary_grid_-10_to_10": compare(
            "nonpositive_boundary_grid_-10_to_10", nonpositive_boundary_grid
        ),
        "positive_float_cases": compare("positive_float_cases", positive_float_cases),
    }
    intended_mismatches = (
        results["documented_examples"]
        + results["exhaustive_positive_int_1_to_30"]
        + results["seeded_positive_int_sample"]
        + results["positive_float_cases"]
    )
    print(f"INTENDED_POSITIVE_DOMAIN_MISMATCHES: {intended_mismatches}")
    print(
        "OUT_OF_DOMAIN_NONPOSITIVE_MISMATCHES: "
        f"{results['nonpositive_boundary_grid_-10_to_10']}"
    )
    return 0 if intended_mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
