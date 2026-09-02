#!/usr/bin/env python3
"""Concrete satisfying witnesses for every claim shape with Python comparisons."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.order_by_points


def score(n: int) -> int:
    digits = [int(ch) for ch in str(abs(n))]
    return sum(digits) - (2 * digits[0] if n < 0 else 0)


def main() -> int:
    canonical = load(Path("/reference/canonical.py"), "claim_canonical")
    candidate = load(
        Path("/tmp/audit-work/reconstruction/solution.py"), "claim_candidate"
    )
    lists = [
        [],
        [0],
        [0, 0],
        [1, 0],
        [1, 11, -1, -11, -12],
        [12, 21, -12, 3],
    ]
    for nums in lists:
        left = canonical(list(nums))
        right = candidate(list(nums))
        print(
            f"input={nums!r} canonical={left!r} candidate={right!r} "
            f"match={left == right}"
        )
    for n in [-12, -11, -1, 0, 1, 11]:
        print(f"score_witness n={n} score={score(n)}")
    print("c05 witness VS=.Vals")
    print("c06 witness empty Vals")
    print("c07 witness N=0")
    print("c08 witness N=0 M=0: 0 <= 0")
    print("c09 witness N=1 M=0: 1 > 0")
    print("c10 witness prompt list")
    print("c11 witness empty list")
    print("c12 witness [12,21,-12,3]")
    print("c13 witness ground ordered sequence from prompt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
