#!/usr/bin/env python3
"""Ground witnesses for the two formal claim preconditions and destinations."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_intersection(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.intersection


def prime_from(number: int, divisor: int) -> str:
    while divisor < number:
        if number % divisor == 0:
            return "NO"
        divisor += 1
    return "YES"


def formal_result(a: int, b: int, c: int, d: int) -> str:
    overlap_length = min(b, d) - max(a, c)
    if overlap_length <= 1:
        return "NO"
    return prime_from(overlap_length, 2)


def main() -> None:
    canonical = load_intersection("canonical_witness", Path("/reference/canonical.py"))
    candidate = load_intersection("candidate_witness", Path("/candidate/solution.py"))

    # LOOP-SPEC witness: DIVISOR=2, LENGTH=3 satisfies 2 <= D <= N.
    # The original loop tests divisor 2, finds nonzero remainder, and returns YES.
    print("loop_precondition_witness DIVISOR=2 LENGTH=3")
    print("loop_guard", 2 <= 2 <= 3)
    print("loop_destination_primeFrom", prime_from(3, 2))

    entry_witnesses = [
        (0, 2, 0, 2),       # prime length 2
        (0, 4, -1, 10),     # composite length 4
        (10, 12, 0, 3),     # disjoint, negative overlap length
        (-3, -1, -5, 5),    # documented negative-coordinate example
    ]
    for endpoints in entry_witnesses:
        a, b, c, d = endpoints
        interval1 = (a, b)
        interval2 = (c, d)
        precondition = a <= b and c <= d
        formal = formal_result(a, b, c, d)
        canonical_result = canonical(interval1, interval2)
        candidate_result = candidate(interval1, interval2)
        print(
            "entry_witness",
            endpoints,
            "precondition=",
            precondition,
            "formal=",
            formal,
            "canonical=",
            canonical_result,
            "candidate=",
            candidate_result,
        )
        if not precondition or len({formal, canonical_result, candidate_result}) != 1:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
