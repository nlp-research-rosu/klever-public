#!/usr/bin/env python3
"""Ground witnesses for each target precondition and its result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/84-solve")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve


def digits(n: int) -> tuple[int, int, int, int, int]:
    return (
        n % 10,
        (n // 10) % 10,
        (n // 100) % 10,
        (n // 1000) % 10,
        (n // 10000) % 10,
    )


def main() -> None:
    trusted = load(ROOT / "canonical.py", "trusted_for_claim_witness")
    generated = load(ROOT / "solution.py", "generated_for_claim_witness")
    claims = [
        ("digit-sum-bound", 0),
        ("solve-sum-00-07", 0),
        ("solve-sum-08-15", 8),
        ("solve-sum-16-23", 79),
        ("solve-sum-24-31", 699),
        ("solve-sum-32-36", 5999),
    ]
    represented = []
    for d4 in range(2):
        for d3 in range(10):
            for d2 in range(10):
                for d1 in range(10):
                    for d0 in range(10):
                        if d4 == 1 and (d0 != 0 or d1 != 0 or d2 != 0 or d3 != 0):
                            continue
                        represented.append(
                            d0 + 10 * d1 + 100 * d2 + 1000 * d3 + 10000 * d4
                        )
    if len(represented) != 10001 or set(represented) != set(range(10001)):
        raise AssertionError("digitDomain is not an exact unique cover of 0..10000")
    print("digitDomain: 10001 unique tuples cover exactly N=0..10000")
    for label, n in claims:
        vector = digits(n)
        digit_sum = sum(vector)
        expected = trusted(n)
        actual = generated(n)
        if expected != actual or int(actual, 2) != digit_sum:
            raise AssertionError((label, n, vector, expected, actual))
        print(
            f"{label}: N={n} digits={vector} sum={digit_sum} "
            f"trusted={expected!r} generated={actual!r}"
        )


if __name__ == "__main__":
    main()
