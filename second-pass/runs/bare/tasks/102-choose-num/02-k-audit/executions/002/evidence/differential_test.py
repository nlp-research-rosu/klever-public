#!/usr/bin/env python3
"""Independent canonical/candidate differential test for choose_num."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.choose_num


def mathematical_oracle(x: int, y: int) -> int:
    if x > y:
        return -1
    largest_even_at_most_y = y - (y % 2)
    return largest_even_at_most_y if largest_even_at_most_y >= x else -1


def branch(x: int, y: int) -> str:
    if x > y:
        return "empty"
    if y % 2 == 0:
        return "even_upper"
    if x == y:
        return "odd_singleton"
    return "odd_upper_with_room"


def main() -> int:
    canonical = load_function(
        "trusted_canonical", Path("/tmp/audit-work/reference/canonical.py")
    )
    candidate = load_function(
        "candidate_solution", Path("/tmp/audit-work/candidate-src/solution.py")
    )

    documented_and_boundaries = [
        (12, 15),
        (13, 12),
        (1, 1),
        (1, 2),
        (2, 2),
        (2, 3),
        (3, 3),
        (3, 4),
        (4, 3),
        (999_999_999_999_999_999, 1_000_000_000_000_000_000),
        (10**80 + 1, 10**80 + 1),
        (10**80 + 1, 10**80 + 9),
        (10**80 + 9, 10**80 + 1),
    ]
    exhaustive = [(x, y) for x in range(1, 129) for y in range(1, 129)]
    rng = random.Random(102)
    generated = [
        (rng.randint(1, 10**12), rng.randint(1, 10**12)) for _ in range(1024)
    ]
    cases = list(dict.fromkeys(documented_and_boundaries + exhaustive + generated))

    counts = {name: 0 for name in (
        "empty",
        "even_upper",
        "odd_singleton",
        "odd_upper_with_room",
    )}
    mismatches = []
    for x, y in cases:
        expected = mathematical_oracle(x, y)
        reference_value = canonical(x, y)
        candidate_value = candidate(x, y)
        counts[branch(x, y)] += 1
        if not (reference_value == candidate_value == expected):
            mismatches.append((x, y, expected, reference_value, candidate_value))

    print("documented_examples=[(12,15),(13,12)]")
    print("boundary_cases=" + repr(documented_and_boundaries))
    print("exhaustive_scope=x,y in [1,128]")
    print("generated_scope=1024 pairs in [1,10^12], seed=102")
    print(f"unique_cases={len(cases)}")
    print(f"branch_counts={counts}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print("first_mismatches=" + repr(mismatches[:20]))
        return 1
    print("DIFFERENTIAL_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
