#!/usr/bin/env python3
"""Independent differential test for HumanEval/80 is_happy."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import random
import string
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_happy


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    canonical = load_function(args.canonical, "trusted_canonical")
    candidate = load_function(args.candidate, "generated_candidate")

    documented = [
        "a",
        "aa",
        "abcd",
        "aabb",
        "adb",
        "xyy",
    ]
    branch_boundaries = [
        "",
        "a",
        "ab",
        "aaa",  # first equality
        "aab",  # positions i and i+1 equal
        "aba",  # positions i and i+2 equal
        "abb",  # positions i+1 and i+2 equal
        "abc",  # no equality, loop exits
        "abca",  # two successful windows
        "abac",  # second-index equality at the first window
        "abcc",  # failure in a later window
        "abcad",  # later i versus i+2 equality
        "abcdefgh",
        "abcdefghh",
        "\x00ab",
        "a\x00a",
        "åβ🙂",
        "åβ🙂å",
        "𐀀𐀁𐀂",
    ]

    exhaustive = [
        "".join(chars)
        for length in range(0, 9)
        for chars in itertools.product("abc", repeat=length)
    ]
    rng = random.Random(800080)
    alphabet = string.ascii_letters + string.digits + "åβ🙂𐀀\x00"
    generated = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 101)))
        for _ in range(5000)
    ]

    tests = documented + branch_boundaries + exhaustive + generated
    mismatches: list[tuple[str, bool, bool]] = []
    for value in tests:
        expected = canonical(value)
        actual = candidate(value)
        if expected != actual:
            mismatches.append((value, expected, actual))

    print("DOCUMENTED_CASES")
    for value in documented:
        print(
            repr(value),
            "canonical=",
            canonical(value),
            "candidate=",
            candidate(value),
        )
    print("BRANCH_BOUNDARY_CASES")
    for value in branch_boundaries:
        print(
            repr(value),
            "canonical=",
            canonical(value),
            "candidate=",
            candidate(value),
        )
    print("EXHAUSTIVE_SCOPE alphabet='abc' lengths=0..8 count=", len(exhaustive))
    print(
        "GENERATED_SCOPE seed=800080 count=5000 lengths=0..100 "
        "alphabet=ascii_letters+digits+five_non_ascii_or_nul"
    )
    print("TOTAL_COMPARISONS", len(tests))
    print("MISMATCHES", len(mismatches))
    for mismatch in mismatches[:20]:
        print("MISMATCH", repr(mismatch))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
