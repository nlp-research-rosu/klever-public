#!/usr/bin/env python3
"""Concrete satisfying witnesses for every positive entry precondition."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def trial_prime(n: int, d: int) -> bool:
    if n < 2 or d < 2:
        return False
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--solution", type=Path, required=True)
    args = parser.parse_args()
    canonical = load_module("witness_canonical", args.canonical)
    solution = load_module("witness_solution", args.solution)

    witnesses = [
        ("intersection-c-gt-a-e-lt-b", (0, 10), (2, 7), lambda a, b, c, e: e - c),
        ("intersection-c-gt-a-e-ge-b", (0, 5), (2, 5), lambda a, b, c, e: b - c),
        ("intersection-c-le-a-e-lt-b", (2, 7), (0, 5), lambda a, b, c, e: e - a),
        ("intersection-c-le-a-e-ge-b", (2, 7), (2, 7), lambda a, b, c, e: b - a),
    ]

    for label, first, second, claimed_length in witnesses:
        a, b = first
        c, e = second
        assert a <= b and c <= e
        if label.startswith("intersection-c-gt-a"):
            assert c > a
        else:
            assert c <= a
        if label.endswith("e-lt-b"):
            assert e < b
        else:
            assert e >= b
        length = claimed_length(a, b, c, e)
        claimed = "YES" if trial_prime(length, 2) else "NO"
        canonical_result = canonical.intersection(first, second)
        solution_result = solution.intersection(first, second)
        assert claimed == canonical_result == solution_result
        print(
            f"{label}: interval1={first} interval2={second} "
            f"claimed_length={length} primeAnswer={claimed} "
            f"canonical={canonical_result} submitted={solution_result} precondition=true"
        )

    print("prime-loop: N=5 D=2 N>=2=true D>=2=true trialPrime(5,2)=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
