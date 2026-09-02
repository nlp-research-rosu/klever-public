#!/usr/bin/env python3
"""Generate deterministic K assertions using statistics.median as oracle."""

from __future__ import annotations

import itertools
import statistics
import sys
from pathlib import Path


def main() -> int:
    source = Path("solution.py").read_text(encoding="utf-8")
    namespace: dict[str, object] = {}
    exec(compile(source, "solution.py", "exec"), namespace)
    candidate = namespace["median"]

    cases: list[list[object]] = [
        [3, 1, 2, 4, 5],
        [-10, 4, 6, 1000, 10, 20],
        [-(2**60), 2**60],
        [-(2**53) - 1, 2**53 + 1, 0],
    ]
    cases.extend(
        list(values)
        for length in range(1, 4)
        for values in itertools.product((-2, -1, 0, 1, 2), repeat=length)
    )
    cases.extend(
        list(values)
        for length in range(1, 3)
        for values in itertools.product((-2.5, -0.0, 0.5, 2.0), repeat=length)
    )
    cases.extend(
        list(values)
        for length in range(1, 3)
        for values in itertools.product(
            (False, True, -3, 2, -1.5, 3.5), repeat=length
        )
    )

    print(source.rstrip())
    print()
    for case in cases:
        expected = statistics.median(case)
        actual = candidate(case)
        if actual != expected:
            raise AssertionError((case, actual, expected))
        print(f"assert median({case!r}) == {expected!r}")

    print(
        f"generated {len(cases)} differential cases with zero CPython mismatches",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
