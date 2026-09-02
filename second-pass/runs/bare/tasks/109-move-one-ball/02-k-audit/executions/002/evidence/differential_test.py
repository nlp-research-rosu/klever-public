#!/usr/bin/env python3
"""Independent differential test for HumanEval 109."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


CANONICAL = Path("/reference/canonical.py")
GENERATED = Path("/candidate/solution.py")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.move_one_ball


def direct_rotation_oracle(values: list[int]) -> bool:
    """Check the natural-language contract without using either algorithm."""
    if not values:
        return True
    for shifts in range(len(values)):
        rotated = values[-shifts:] + values[:-shifts] if shifts else values[:]
        if all(rotated[index] <= rotated[index + 1] for index in range(len(values) - 1)):
            return True
    return False


def main() -> int:
    canonical = load_function("trusted_canonical_109", CANONICAL)
    generated = load_function("candidate_generated_109", GENERATED)

    named_cases = [
        [],
        [0],
        [-10**30],
        [1, 2],
        [2, 1],
        [1, 2, 3],
        [3, 1, 2],
        [2, 3, 1],
        [2, 1, 3],
        [3, 2, 1],
        [3, 4, 5, 1, 2],
        [3, 5, 4, 1, 2],
        [-3, -1, 2, -10],
        [10**50, -(10**50), 0],
    ]

    tested: list[list[int]] = [case[:] for case in named_cases]
    for length in range(0, 9):
        tested.extend([list(case) for case in itertools.permutations(range(length))])

    rng = random.Random(109_20260726)
    for length in [2, 3, 4, 5, 8, 9, 16, 31, 64]:
        for _ in range(200):
            tested.append(rng.sample(range(-10**9, 10**9), length))

    mismatches: list[dict[str, object]] = []
    branch_counts = {"empty": 0, "nonempty": 0, "oracle_true": 0, "oracle_false": 0}
    digest = hashlib.sha256()
    for values in tested:
        expected = direct_rotation_oracle(values)
        canonical_result = canonical(values[:])
        generated_result = generated(values[:])
        digest.update(json.dumps(values, separators=(",", ":")).encode())
        digest.update(b"\n")
        branch_counts["empty" if not values else "nonempty"] += 1
        branch_counts["oracle_true" if expected else "oracle_false"] += 1
        if not (
            type(canonical_result) is bool
            and type(generated_result) is bool
            and canonical_result == generated_result == expected
        ):
            mismatches.append(
                {
                    "input": values,
                    "oracle": expected,
                    "canonical": canonical_result,
                    "generated": generated_result,
                }
            )
            if len(mismatches) >= 20:
                break

    print("contract_oracle=explicitly enumerate every right rotation and test nondecreasing")
    print("documented_and_boundary_cases=", len(named_cases))
    print("exhaustive_scope=all permutations of range(n), n=0..8")
    print("random_scope=200 seeded unique lists at each n in 2,3,4,5,8,9,16,31,64")
    print("random_seed=10920260726")
    print("input_sequence_sha256=", digest.hexdigest())
    print("tested=", len(tested))
    print("branch_counts=", json.dumps(branch_counts, sort_keys=True))
    print("mismatches=", len(mismatches))
    if mismatches:
        print(json.dumps(mismatches, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
