#!/usr/bin/env python3
"""Finite independent check of the natural-language minimum-change contract."""

from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path


def load_candidate():
    path = Path("/candidate/solution.py")
    spec = importlib.util.spec_from_file_location("contract_candidate", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.smallest_change


def brute_minimum(arr: tuple[int, ...], alphabet: tuple[int, ...]) -> int:
    half_length = (len(arr) + 1) // 2
    minimum = len(arr)
    for left_half in product(alphabet, repeat=half_length):
        if len(arr) % 2:
            palindrome = left_half + left_half[-2::-1]
        else:
            palindrome = left_half + left_half[::-1]
        distance = sum(a != b for a, b in zip(arr, palindrome))
        minimum = min(minimum, distance)
    return minimum


def main() -> int:
    candidate = load_candidate()
    alphabet = (-2, 0, 3)
    cases = 0
    for length in range(9):
        for arr in product(alphabet, repeat=length):
            expected = brute_minimum(arr, alphabet)
            actual = candidate(list(arr))
            if actual != expected:
                raise AssertionError(
                    f"input={arr!r} candidate={actual} brute_minimum={expected}"
                )
            cases += 1
    print("oracle=exhaustive enumeration of all same-length palindromes")
    print(f"alphabet={alphabet!r}")
    print("input_lengths=0..8")
    print(
        "replacement-domain-justification=an optimum can choose one endpoint "
        "of every unequal pair, so the input alphabet suffices"
    )
    print(f"cases={cases}")
    print("mismatches=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
