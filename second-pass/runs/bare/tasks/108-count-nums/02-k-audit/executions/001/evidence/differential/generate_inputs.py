#!/usr/bin/env python3
"""Generate a deterministic, fully preserved differential corpus."""

from __future__ import annotations

import itertools
import json
import pathlib
import random
import sys


def add_case(cases: list[dict[str, object]], seen: set[tuple[int, ...]],
             label: str, values: list[int]) -> None:
    key = tuple(values)
    if key not in seen:
        cases.append({"label": label, "arr": values})
        seen.add(key)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} OUTPUT.json", file=sys.stderr)
        return 64

    cases: list[dict[str, object]] = []
    seen: set[tuple[int, ...]] = set()

    documented = [
        ("example-empty", []),
        ("example-mixed", [-1, 11, -11]),
        ("example-all-positive", [1, 1, 2]),
    ]
    for label, values in documented:
        add_case(cases, seen, label, values)

    branch_values = [
        -1000, -999, -101, -100, -99, -98, -20, -19, -11, -10,
        -9, -8, -1, 0, 1, 8, 9, 10, 11, 19, 20, 98, 99, 100,
        101, 999, 1000,
    ]
    for value in branch_values:
        add_case(cases, seen, f"singleton-boundary-{value}", [value])
    for left, right in itertools.product(branch_values, repeat=2):
        add_case(cases, seen, f"pair-{left}-{right}", [left, right])

    small_branch_set = [-100, -99, -10, -9, 0, 9, 10, 99, 100]
    for length in range(4):
        for values in itertools.product(small_branch_set, repeat=length):
            add_case(cases, seen, f"small-product-len-{length}", list(values))

    for value in range(-1000, 1001):
        add_case(cases, seen, f"singleton-exhaustive-{value}", [value])

    rng = random.Random(108)
    for index in range(2000):
        length = rng.randrange(0, 26)
        values = [rng.randint(-(10**18), 10**18) for _ in range(length)]
        add_case(cases, seen, f"random-{index}", values)

    output = {
        "schema": 1,
        "seed": 108,
        "scope": {
            "documented_examples": 3,
            "branch_values": branch_values,
            "all_branch_value_pairs": True,
            "small_cartesian_lengths": [0, 1, 2, 3],
            "exhaustive_singletons": [-1000, 1000],
            "random_cases_requested": 2000,
            "random_length_range": [0, 25],
            "random_integer_range": [-(10**18), 10**18],
        },
        "cases": cases,
    }
    output_path = pathlib.Path(sys.argv[1])
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"WROTE {output_path}")
    print(f"UNIQUE_CASES {len(cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
