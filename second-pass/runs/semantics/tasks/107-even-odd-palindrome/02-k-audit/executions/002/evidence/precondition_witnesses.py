#!/usr/bin/env python3
"""Ground witnesses for every entry claim and its K-side summary formula."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.even_odd_palindrome


def k_summary(n: int) -> tuple[int, int]:
    if 1 <= n < 10:
        return n // 2, (n + 1) // 2
    if 10 <= n < 100:
        two_digit = n // 11
        return 4 + two_digit // 2, 5 + (two_digit + 1) // 2
    if 100 <= n < 1000:
        leading_digit = n // 100
        current_block = (n % 100 - leading_digit + 10) // 10
        even = 8 + 10 * ((leading_digit - 1) // 2)
        odd = 10 + 10 * (leading_digit // 2)
        if leading_digit % 2 == 0:
            even += current_block
        else:
            odd += current_block
        return even, odd
    if n == 1000:
        return 48, 60
    raise ValueError(n)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    args = parser.parse_args()
    canonical = load_entry(args.canonical, "canonical_witness")
    generated = load_entry(args.generated, "generated_witness")
    witnesses = [
        ("1 <= N < 10", 1),
        ("10 <= N < 100", 10),
        ("100 <= N < 1000", 100),
        ("N = 1000", 1000),
    ]
    ok = True
    for precondition, n in witnesses:
        summary = k_summary(n)
        canonical_result = canonical(n)
        generated_result = generated(n)
        equal = summary == canonical_result == generated_result
        ok &= equal
        print(
            f"precondition={precondition!r} witness={n} "
            f"k_postcondition={summary} canonical={canonical_result} "
            f"generated={generated_result} all_equal={equal}"
        )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
