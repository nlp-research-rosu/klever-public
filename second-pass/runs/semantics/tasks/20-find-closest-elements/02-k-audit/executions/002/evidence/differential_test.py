#!/usr/bin/env python3
"""Independent differential and contract tests for HumanEval/20."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import math
import random
from collections.abc import Callable
from pathlib import Path
from typing import Any


CANONICAL = Path("/reference/canonical.py")
GENERATED = Path("/tmp/audit-work/task20/solution.py")
SEED = 20260726
SMALL_DOMAIN = (-2.0, -1.0, -0.0, 0.5, 1.0, 2.0)


def load_entry(path: Path, module_name: str) -> Callable[[list[float]], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_closest_elements


def same_float(left: float, right: float) -> bool:
    if math.isnan(left) and math.isnan(right):
        return True
    if left == right:
        if left == 0.0:
            return math.copysign(1.0, left) == math.copysign(1.0, right)
        return True
    return False


def same_result(left: Any, right: Any) -> bool:
    if (
        isinstance(left, tuple)
        and isinstance(right, tuple)
        and len(left) == len(right) == 2
    ):
        return same_float(left[0], right[0]) and same_float(left[1], right[1])
    return left == right


def call_outcome(function: Callable[[list[float]], Any], values: list[float]) -> tuple:
    try:
        return ("return", function(values.copy()))
    except Exception as err:  # The out-of-domain probes intentionally reach errors.
        return ("raise", type(err).__name__, str(err))


def pair_property(values: list[float], result: tuple[float, float]) -> bool:
    """For finite inputs, check ordered membership and globally minimal gap."""
    if not all(math.isfinite(value) for value in values):
        return True
    low, high = result
    if low > high:
        return False
    remaining = values.copy()
    try:
        remaining.remove(low)
        remaining.remove(high)
    except ValueError:
        return False
    result_gap = high - low
    best_gap = min(
        abs(values[i] - values[j])
        for i in range(len(values))
        for j in range(i + 1, len(values))
    )
    return result_gap == best_gap


def main() -> int:
    canonical = load_entry(CANONICAL, "trusted_canonical")
    generated = load_entry(GENERATED, "candidate_generated")

    documented_and_boundaries = [
        [1.0, 2.0, 3.0, 4.0, 5.0, 2.2],
        [1.0, 2.0, 3.0, 4.0, 5.0, 2.0],
        [1.0, 2.0],
        [2.0, 1.0],
        [2.0, 2.0],
        [0.0, -0.0],
        [-4.5, -1.0],
        [9.0, -2.0, 4.0],
        [0.0, 10.0, 4.0],
        [0.0, 10.0, 6.0],
        [0.0, 2.0, 4.0],
        [4.0, 0.0, 2.0],
        [5.0, 0.0, 4.0, 3.0],
        [float("-inf"), 0.0, float("inf")],
        [float("inf"), float("inf")],
        [float("nan"), 1.0, 2.0],
        [1.0, float("nan"), 2.0],
        [1.0, 2.0, float("nan")],
    ]
    out_of_domain = [[], [1.0]]

    all_cases: list[list[float]] = list(documented_and_boundaries)
    for length in range(2, 7):
        all_cases.extend(
            [list(values) for values in itertools.product(SMALL_DOMAIN, repeat=length)]
        )

    rng = random.Random(SEED)
    for _ in range(5000):
        length = rng.randint(2, 25)
        values = [rng.randint(-10000, 10000) / 16.0 for _ in range(length)]
        all_cases.append(values)

    mismatches: list[tuple[list[float], tuple, tuple]] = []
    property_failures: list[tuple[list[float], Any]] = []
    case_digest = hashlib.sha256()
    for values in all_cases:
        case_digest.update(repr(values).encode("utf-8") + b"\n")
        canonical_outcome = call_outcome(canonical, values)
        generated_outcome = call_outcome(generated, values)
        outcomes_equal = (
            canonical_outcome[0] == generated_outcome[0]
            and (
                same_result(canonical_outcome[1], generated_outcome[1])
                if canonical_outcome[0] == "return"
                else canonical_outcome[1:] == generated_outcome[1:]
            )
        )
        if not outcomes_equal:
            mismatches.append((values, canonical_outcome, generated_outcome))
        if (
            generated_outcome[0] == "return"
            and not pair_property(values, generated_outcome[1])
        ):
            property_failures.append((values, generated_outcome[1]))

    print(f"canonical={CANONICAL}")
    print(f"generated={GENERATED}")
    print(f"seed={SEED}")
    print(f"small_domain={SMALL_DOMAIN}")
    print(f"documented_and_boundary_cases={documented_and_boundaries!r}")
    print(f"intended_domain_case_count={len(all_cases)}")
    print(f"intended_domain_case_digest={case_digest.hexdigest()}")
    print(f"mismatch_count={len(mismatches)}")
    print(f"mismatches={mismatches[:20]!r}")
    print(f"finite_contract_property_failure_count={len(property_failures)}")
    print(f"finite_contract_property_failures={property_failures[:20]!r}")
    print("out_of_domain_probes:")
    for values in out_of_domain:
        print(
            f"  input={values!r} canonical={call_outcome(canonical, values)!r} "
            f"generated={call_outcome(generated, values)!r}"
        )

    return 0 if not mismatches and not property_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
