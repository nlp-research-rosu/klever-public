#!/usr/bin/env python3
"""Independent differential check: trusted canonical vs candidate solution."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/65-circular-shift/solution.py")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.circular_shift


def main() -> None:
    canonical = load_entry("trusted_humaneval_65", CANONICAL_PATH)
    candidate = load_entry("candidate_humaneval_65", CANDIDATE_PATH)

    cases: list[tuple[int, int, str]] = [
        (12, 1, "documented example 1"),
        (12, 2, "documented example 2"),
    ]

    # An integer's decimal string is never empty. x=0 is the shortest
    # representation; shifts below/at/above each branch boundary are explicit.
    boundary_xs = [
        0,
        1,
        9,
        10,
        12,
        100,
        1010,
        2**63 - 1,
        10**100 + 203,
        -1,
        -9,
        -10,
        -120,
        -(10**100 + 203),
    ]
    for x in boundary_xs:
        length = len(str(x))
        for shift in sorted(
            {
                -10**6,
                -length - 1,
                -1,
                0,
                1,
                max(0, length - 1),
                length,
                length + 1,
                length + 2,
                10**6,
            }
        ):
            cases.append((x, shift, "branch boundary"))

    # Dense small integers cover signs, zeros inside the representation, and
    # every branch repeatedly.
    for x in range(-500, 501):
        for shift in range(-20, 41):
            cases.append((x, shift, "dense generated"))

    # Deterministic large arbitrary-precision representatives.
    rng = random.Random(650065)
    for _ in range(2000):
        bits = rng.choice([1, 2, 8, 32, 64, 127, 256, 1024, 4096])
        x = rng.getrandbits(bits)
        if rng.randrange(2):
            x = -x
        length = len(str(x))
        shifts = [
            -rng.randrange(0, 2 * length + 20),
            -1,
            0,
            1,
            max(0, length - 1),
            length,
            length + 1,
            rng.randrange(-2 * length - 20, 2 * length + 20),
        ]
        for shift in shifts:
            cases.append((x, shift, "large generated"))

    mismatches: list[tuple[int, int, str, str, str]] = []
    categories: dict[str, int] = {}
    for x, shift, category in cases:
        expected = canonical(x, shift)
        actual = candidate(x, shift)
        categories[category] = categories.get(category, 0) + 1
        if actual != expected:
            mismatches.append((x, shift, expected, actual, category))
            if len(mismatches) >= 20:
                break

    print(f"canonical={CANONICAL_PATH}")
    print(f"candidate={CANDIDATE_PATH}")
    print("empty_case=not_applicable: every integer has a nonempty decimal string")
    print(f"categories={categories}")
    print(f"total_cases={sum(categories.values())}")
    print(f"mismatches={len(mismatches)}")
    for mismatch in mismatches:
        print(f"MISMATCH {mismatch!r}")
    assert not mismatches
    print("DIFFERENTIAL_CHECK: PASS")


if __name__ == "__main__":
    main()
