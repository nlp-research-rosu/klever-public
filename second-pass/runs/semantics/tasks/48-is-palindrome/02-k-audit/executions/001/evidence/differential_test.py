#!/usr/bin/env python3
"""Independent differential oracle for HumanEval 48.

The candidate/proof equations are not imported.  The two Python modules are
loaded under distinct names and compared on a deterministic, printed input set.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_palindrome


def cases():
    documented = ["", "aba", "aaaaa", "zbcd"]
    boundaries = [
        "a",
        "aa",
        "ab",
        "aaa",
        "aab",
        "abb",
        "abc",
        "abba",
        "abca",
        "abcba",
        "abcca",
        "abcdefgfedcba",
        "abcdefXfedcba",
        "\x00",
        "\x00a\x00",
        "é",
        "éaé",
        "éaè",
        "🙂🙃🙂",
        "🙂🙃",
        "e\u0301",
        "e\u0301\u0301e",
        "𐐷a𐐷",
    ]

    mismatch_positions = []
    for length in range(2, 15):
        palindrome = ["a"] * length
        mismatch_positions.append("".join(palindrome))
        for position in range((length + 1) // 2):
            value = palindrome.copy()
            value[position] = "b"
            mismatch_positions.append("".join(value))

    exhaustive_small = [
        "".join(chars)
        for length in range(0, 8)
        for chars in itertools.product("ab", repeat=length)
    ]

    rng = random.Random(480048)
    alphabet = ["a", "b", "c", "0", " ", "é", "🙂", "\x00", "\u0301"]
    generated = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 41)))
        for _ in range(300)
    ]

    groups = [
        ("documented", documented),
        ("boundary", boundaries),
        ("mismatch-position", mismatch_positions),
        ("exhaustive-ab-length-0-through-7", exhaustive_small),
        ("seeded-generated", generated),
    ]
    ordinal = 0
    for group, values in groups:
        for value in values:
            yield ordinal, group, value
            ordinal += 1


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: differential_test.py CANONICAL.py GENERATED.py", file=sys.stderr)
        return 2

    canonical = load_entry(Path(sys.argv[1]), "trusted_canonical")
    generated = load_entry(Path(sys.argv[2]), "audited_generated")

    total = 0
    mismatches = 0
    for ordinal, group, value in cases():
        expected = canonical(value)
        actual = generated(value)
        record = {
            "id": ordinal,
            "group": group,
            "input": value,
            "canonical": expected,
            "generated": actual,
        }
        print(json.dumps(record, ensure_ascii=True, sort_keys=True))
        total += 1
        if type(expected) is not bool or type(actual) is not bool or expected != actual:
            mismatches += 1

    print(
        json.dumps(
            {
                "summary": {
                    "total": total,
                    "mismatches": mismatches,
                    "seed": 480048,
                }
            },
            sort_keys=True,
        )
    )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
