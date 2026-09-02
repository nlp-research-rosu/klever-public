#!/usr/bin/env python3
"""Independent differential and branch-boundary tests for HumanEval 145."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_digit_key(number: int) -> int:
    digits = [int(char) for char in str(abs(number))]
    if number < 0:
        digits[0] = -digits[0]
    return sum(digits)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_module("trusted_canonical", args.canonical)
    generated = load_module("generated_solution", args.generated)

    explicit = [
        [],
        [1, 11, -1, -11, -12],
        [0],
        [-1, 0, 1],
        [9, 10, 11, 19, 20],
        [-9, -10, -11, -19, -20],
        [10, 1, 100, 1000, -10, -1, -100, -1000],
        [-12, -21, 3, 30, 12, 21],
        [999, -999, 0, 999, -999],
        [10**100, -(10**100), 10**100 - 1, -(10**100 - 1)],
    ]

    checked = 0
    digest = hashlib.sha256()

    def check(values: list[int], label: str) -> None:
        nonlocal checked
        oracle = canonical.order_by_points(list(values))
        actual = generated.order_by_points(list(values))
        if actual != oracle:
            raise AssertionError(
                f"{label}: input={values!r} canonical={oracle!r} generated={actual!r}"
            )
        digest.update(
            json.dumps(
                [values, oracle], separators=(",", ":"), ensure_ascii=True
            ).encode()
        )
        digest.update(b"\n")
        checked += 1

    for index, values in enumerate(explicit):
        check(values, f"explicit-{index}")
        print(
            "EXPLICIT",
            index,
            "input=",
            values,
            "output=",
            generated.order_by_points(list(values)),
        )

    alphabet = [-101, -20, -12, -11, -10, -9, -1, 0, 1, 9, 10, 11, 20, 101]
    for length in range(4):
        for values in itertools.product(alphabet, repeat=length):
            check(list(values), f"exhaustive-length-{length}")

    rng = random.Random(145_2026)
    boundaries = [
        -101,
        -100,
        -99,
        -11,
        -10,
        -9,
        -1,
        0,
        1,
        9,
        10,
        11,
        99,
        100,
        101,
    ]
    for sample in range(2500):
        values = []
        for _ in range(rng.randrange(0, 41)):
            if rng.randrange(4) == 0:
                value = rng.choice(boundaries)
            else:
                value = rng.randrange(-(10**60), 10**60 + 1)
            values.append(value)
        check(values, f"random-{sample}")

    helper_checked = 0
    helper_points = set(range(-10050, 10051))
    for power in range(1, 101):
        pivot = 10**power
        helper_points.update(
            {
                -pivot - 1,
                -pivot,
                -pivot + 1,
                pivot - 1,
                pivot,
                pivot + 1,
            }
        )
    for number in sorted(helper_points):
        expected = independent_digit_key(number)
        actual = generated.digit_sum(number)
        if actual != expected:
            raise AssertionError(
                f"digit_sum({number}) expected {expected}, generated {actual}"
            )
        helper_checked += 1

    print(
        "SUMMARY",
        f"entry_cases={checked}",
        f"helper_cases={helper_checked}",
        "random_seed=1452026",
        f"case_digest={digest.hexdigest()}",
        "mismatches=0",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
