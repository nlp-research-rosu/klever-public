#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for HumanEval/3."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


CANONICAL = Path("/reference/canonical.py")
CANDIDATE = Path("/tmp/audit-work/rebuild/solution.py")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.below_zero


def independent_oracle(operations: list[int]) -> bool:
    running = 0
    for item in operations:
        running = running + item
        if running < 0:
            return True
    return False


def main() -> None:
    canonical = load_entry("trusted_humaneval_3", CANONICAL)
    candidate = load_entry("candidate_humaneval_3", CANDIDATE)

    named_cases = [
        ("empty", []),
        ("prompt-positive", [1, 2, 3]),
        ("prompt-negative-third-prefix", [1, 2, -4, 5]),
        ("negative-first-prefix", [-1]),
        ("zero-boundary-single", [0]),
        ("zero-boundary-after-positive", [5, -5]),
        ("negative-after-zero", [5, -5, -1]),
        ("recovers-after-negative-but-must-return-true", [-1, 100]),
        ("large-positive-and-negative-zero", [10**100, -(10**100)]),
        ("large-negative-first", [-(10**100), 10**100]),
    ]

    exhaustive_cases = (
        list(values)
        for length in range(0, 6)
        for values in itertools.product(range(-3, 4), repeat=length)
    )

    rng = random.Random(0x3B310)
    generated_cases: list[list[int]] = []
    edge_values = [
        -(10**100),
        -(2**63),
        -10**9,
        -1,
        0,
        1,
        10**9,
        2**63,
        10**100,
    ]
    for _ in range(1000):
        length = rng.randrange(0, 31)
        generated_cases.append(
            [
                rng.choice(edge_values)
                if rng.randrange(3) == 0
                else rng.randrange(-(10**12), 10**12 + 1)
                for _ in range(length)
            ]
        )

    checked = 0
    mismatches: list[tuple[list[int], bool, bool, bool]] = []

    def check(case: list[int]) -> None:
        nonlocal checked
        expected = independent_oracle(case)
        canonical_value = canonical(case)
        candidate_value = candidate(case)
        checked += 1
        if (
            canonical_value is not expected
            or candidate_value is not expected
            or type(canonical_value) is not bool
            or type(candidate_value) is not bool
        ):
            mismatches.append(
                (case, expected, canonical_value, candidate_value)
            )

    for name, case in named_cases:
        check(case)
        print(
            f"NAMED {name}: input={case!r} "
            f"canonical={canonical(case)!r} candidate={candidate(case)!r}"
        )
    for case in exhaustive_cases:
        check(case)
    for case in generated_cases:
        check(case)

    exhaustive_count = sum(7**length for length in range(0, 6))
    print(
        "SCOPE: 10 named boundary/example cases; "
        f"{exhaustive_count} exhaustive lists of lengths 0..5 over [-3,3]; "
        "1000 seeded lists of lengths 0..30 with ordinary, 64-bit-edge, "
        "and arbitrary-precision values"
    )
    print(f"CHECKED={checked} MISMATCHES={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:20]:
            print(f"MISMATCH {mismatch!r}")
        raise SystemExit(1)
    print("DIFFERENTIAL: PASS")


if __name__ == "__main__":
    main()
