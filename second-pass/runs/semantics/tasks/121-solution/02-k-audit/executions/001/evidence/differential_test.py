#!/usr/bin/env python3
"""Independent differential test for HumanEval problem 121."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import random
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_module("audit_canonical", args.canonical).solution
    candidate = load_module("audit_candidate", args.candidate).solution

    documented_and_boundary = [
        [5, 8, 7, 1],
        [3, 3, 3, 3, 3],
        [30, 13, 24, 321],
        [],  # outside the stated non-empty domain, checked as a boundary
        [0],
        [1],
        [-1],
        [2],
        [-2],
        [7, 9],
        [8, 7],
        [-5, 2, -3],
        [10**100, -(10**100), 10**100 + 1, -(10**100 + 1)],
    ]

    # Exhaustively crosses empty/non-empty, even/odd positions, negative/zero/
    # positive values, and even/odd values. The seed makes the broader sample
    # fully reproducible.
    alphabet = [-100, -3, -2, -1, 0, 1, 2, 3, 100]
    exhaustive = (
        list(values)
        for length in range(0, 6)
        for values in itertools.product(alphabet, repeat=length)
    )
    rng = random.Random(121)
    generated = [
        [rng.randint(-(10**9), 10**9) for _ in range(rng.randint(1, 20))]
        for _ in range(2000)
    ]

    checked = 0
    mismatches: list[tuple[list[int], int, int]] = []
    for values in itertools.chain(documented_and_boundary, exhaustive, generated):
        expected = canonical(values)
        actual = candidate(values)
        checked += 1
        if actual != expected:
            mismatches.append((values, expected, actual))
            if len(mismatches) >= 20:
                break

    print("oracle=/reference/canonical.py:solution")
    print("candidate=/tmp/audit-work/121-audit/solution.py:solution")
    print(f"documented_and_boundary_cases={len(documented_and_boundary)}")
    print("exhaustive_lengths=0..5")
    print(f"exhaustive_alphabet={alphabet}")
    print("generated_seed=121 generated_cases=2000 lengths=1..20")
    print(f"checked={checked}")
    print(f"mismatches={len(mismatches)}")
    for values, expected, actual in mismatches:
        print(f"MISMATCH input={values!r} canonical={expected!r} candidate={actual!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
