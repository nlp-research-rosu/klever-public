#!/usr/bin/env python3
"""Independent differential test of HumanEval/82 canonical vs candidate."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import random
import sys


ROOT = Path("/tmp/audit-work/differential")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    canonical = load("trusted_canonical", ROOT / "canonical.py").prime_length
    candidate = load("generated_candidate", ROOT / "solution.py").prime_length

    documented = ["Hello", "abcdcba", "kittens", "orange"]
    boundaries = [
        "",
        "a",
        "ab",
        "abc",
        "abcd",
        "abcde",
        "abcdef",
        "abcdefg",
        "abcdefgh",
        "a" * 9,
        "a" * 10,
        "a" * 11,
        "a" * 12,
        "a" * 13,
        "a" * 25,
        "a" * 49,
    ]
    unicode_cases = [
        "é",
        "e\u0301",
        "😀",
        "😀😀",
        "𐐷abc",
        "\x00",
        "\n\t",
        "你好世界",
    ]
    exhaustive_lengths = ["x" * n for n in range(0, 301)]

    rng = random.Random(8202026)
    alphabet = "abCD09é😀中\u0301"
    generated = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 2001)))
        for _ in range(200)
    ]

    groups = [
        ("documented", documented),
        ("branch_boundaries", boundaries),
        ("unicode_and_control", unicode_cases),
        ("all_lengths_0_through_300", exhaustive_lengths),
        ("seeded_generated", generated),
    ]

    mismatches = []
    total = 0
    for group_name, cases in groups:
        group_mismatches = 0
        for index, value in enumerate(cases):
            expected = canonical(value)
            actual = candidate(value)
            total += 1
            if actual != expected or type(actual) is not bool:
                group_mismatches += 1
                mismatches.append(
                    (group_name, index, len(value), repr(value[:40]), expected, actual)
                )
        print(
            f"group={group_name} cases={len(cases)} "
            f"mismatches={group_mismatches}"
        )

    explicit = {
        "Hello": True,
        "abcdcba": True,
        "kittens": True,
        "orange": False,
        "": False,
        "a": False,
        "ab": True,
        "abc": True,
        "abcd": False,
    }
    for value, wanted in explicit.items():
        got = candidate(value)
        if got != wanted:
            mismatches.append(("explicit_oracle", 0, len(value), repr(value), wanted, got))

    print(f"total_cases={total} total_mismatches={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch}")
    return 0 if not mismatches else 1


if __name__ == "__main__":
    sys.exit(main())
