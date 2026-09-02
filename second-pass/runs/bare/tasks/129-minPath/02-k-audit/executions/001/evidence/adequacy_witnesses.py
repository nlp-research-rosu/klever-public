#!/usr/bin/env python3
"""Ground witnesses satisfying each submitted entry claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Callable


def load(path: str, name: str) -> Callable[[list[list[int]], int], list[int]]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


def alternating(length: int, neighbor: int) -> list[int]:
    return [1 if index % 2 == 0 else neighbor for index in range(length)]


def valid_tail(a: int, b: int, c: int) -> bool:
    return (
        2 <= a <= 4
        and 2 <= b <= 4
        and 2 <= c <= 4
        and a != b
        and a != c
        and b != c
    )


def main() -> int:
    candidate = load("/tmp/audit-work/candidate-src/solution.py", "candidate_witness")
    canonical = load("/tmp/audit-work/reference/canonical.py", "canonical_witness")
    witnesses = [
        (1, "ground", [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, [1, 2, 1], True),
        (2, "ground", [[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1, [1], True),
        (3, "ground", [[5, 9, 3], [4, 1, 6], [7, 8, 2]], 6, [1, 4, 1, 4, 1, 4], True),
        (4, "A=2,B=3,C=4; A<B", [[1, 2], [3, 4]], 5, alternating(5, 2), valid_tail(2, 3, 4) and 2 < 3),
        (5, "A=3,B=2,C=4; B<A", [[1, 3], [2, 4]], 5, alternating(5, 2), valid_tail(3, 2, 4) and 2 < 3),
        (6, "A=2,B=3,C=4; A<B", [[2, 1], [4, 3]], 5, alternating(5, 2), valid_tail(2, 3, 4) and 2 < 3),
        (7, "A=3,B=2,C=4; B<A", [[3, 1], [4, 2]], 5, alternating(5, 2), valid_tail(3, 2, 4) and 2 < 3),
        (8, "A=2,B=3,C=4; A<B", [[2, 4], [1, 3]], 5, alternating(5, 2), valid_tail(2, 3, 4) and 2 < 3),
        (9, "A=3,B=2,C=4; B<A", [[3, 4], [1, 2]], 5, alternating(5, 2), valid_tail(3, 2, 4) and 2 < 3),
        (10, "A=2,B=3,C=4; A<B", [[4, 2], [3, 1]], 5, alternating(5, 2), valid_tail(2, 3, 4) and 2 < 3),
        (11, "A=3,B=2,C=4; B<A", [[4, 3], [2, 1]], 5, alternating(5, 2), valid_tail(3, 2, 4) and 2 < 3),
    ]

    failures = []
    for number, precondition, grid, k, expected, precondition_holds in witnesses:
        candidate_result = candidate([row[:] for row in grid], k)
        canonical_result = canonical([row[:] for row in grid], k)
        match = precondition_holds and candidate_result == canonical_result == expected
        print(
            f"CLAIM={number:02d}|PRE={precondition}|PRE_HOLDS={precondition_holds}|"
            f"GRID={grid}|K={k}|EXPECTED={expected}|CANDIDATE={candidate_result}|"
            f"CANONICAL={canonical_result}|MATCH={match}"
        )
        if not match:
            failures.append(number)
    print(f"TOTAL_WITNESSES={len(witnesses)}")
    print(f"FAILURES={failures}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
