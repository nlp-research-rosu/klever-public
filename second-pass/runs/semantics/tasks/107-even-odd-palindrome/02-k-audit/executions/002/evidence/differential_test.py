#!/usr/bin/env python3
"""Independent differential check of trusted canonical vs submitted Python."""

from __future__ import annotations

import argparse
import importlib.util
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.even_odd_palindrome


def direct_oracle(n: int) -> tuple[int, int]:
    palindromes = [value for value in range(1, n + 1) if str(value) == str(value)[::-1]]
    return (
        sum(value % 2 == 0 for value in palindromes),
        sum(value % 2 == 1 for value in palindromes),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical")
    generated = load_entry(args.generated, "submitted_generated")

    examples = [3, 12]
    empty_or_boundary = [1, 2, 9, 10, 11, 12, 99, 100, 101, 109, 110, 111, 999, 1000]
    branch_boundaries = [
        9,
        10,
        99,
        100,
        199,
        200,
        299,
        300,
        399,
        400,
        499,
        500,
        599,
        600,
        699,
        700,
        799,
        800,
        899,
        900,
        999,
        1000,
    ]
    rng = random.Random(107)
    generated_samples = sorted({rng.randint(1, 1000) for _ in range(64)})
    exhaustive = list(range(1, 1001))

    mismatches: list[tuple[int, object, object, object]] = []
    for n in exhaustive:
        expected = canonical(n)
        actual = generated(n)
        direct = direct_oracle(n)
        if expected != actual or expected != direct:
            mismatches.append((n, expected, actual, direct))

    print(f"documented_examples={examples}")
    print(f"empty_interval_case=minimal_positive_n=1")
    print(f"boundary_cases={empty_or_boundary}")
    print(f"branch_boundaries={branch_boundaries}")
    print(f"generated_samples_seed=107 count={len(generated_samples)} values={generated_samples}")
    print("intended_domain=all integers n with 1 <= n <= 1000")
    print(f"exhaustive_cases={len(exhaustive)}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(f"mismatches={mismatches[:20]}")
        return 1

    for n in sorted(set(examples + empty_or_boundary + branch_boundaries + generated_samples)):
        print(f"witness n={n} result={generated(n)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
