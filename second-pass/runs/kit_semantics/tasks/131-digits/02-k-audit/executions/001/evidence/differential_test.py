#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for HumanEval/131."""

from __future__ import annotations

import argparse
import importlib.util
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.digits


def make_inputs() -> list[int]:
    documented = [1, 4, 235]
    branch_boundaries = [
        1, 2, 3, 4, 8, 9, 10, 11, 12, 19, 20, 21,
        88, 89, 90, 91, 98, 99, 100, 101, 109, 110, 111,
        200, 201, 208, 209, 2468, 97531, 1010101, 8080808,
        111111, 135790, 246802468, 975319753,
    ]
    decimal_boundaries: list[int] = []
    for exponent in range(1, 121):
        power = 10 ** exponent
        decimal_boundaries.extend([power - 1, power, power + 1])

    rng = random.Random(131)
    generated = [
        rng.randrange(1, 10 ** rng.randrange(1, 121))
        for _ in range(5000)
    ]

    # Preserve order while avoiding duplicate calls.
    return list(dict.fromkeys(
        documented
        + branch_boundaries
        + list(range(1, 25001))
        + decimal_boundaries
        + generated
    ))


def call_or_exception(function, value: int):
    try:
        return ("value", function(value))
    except Exception as err:  # only for explicit out-of-contract observations
        return ("exception", type(err).__name__)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-inputs", action="store_true")
    parser.add_argument("--input-file", type=Path)
    args = parser.parse_args()

    generated_inputs = make_inputs()
    if args.list_inputs:
        for value in generated_inputs:
            print(value)
        return 0

    if args.input_file is None:
        parser.error("--input-file is required unless --list-inputs is used")
    inputs = [int(line) for line in args.input_file.read_text().splitlines()]
    if inputs != generated_inputs:
        raise AssertionError("preserved input file does not match the generator")

    canonical = load_function("trusted_canonical_131", Path("/reference/canonical.py"))
    candidate = load_function(
        "scratch_candidate_131", Path("/tmp/audit-work/source/solution.py")
    )

    documented_expected = {1: 1, 4: 0, 235: 15}
    for value, expected in documented_expected.items():
        assert canonical(value) == expected
        assert candidate(value) == expected

    mismatches = []
    for value in inputs:
        expected = canonical(value)
        actual = candidate(value)
        if expected != actual:
            mismatches.append((value, expected, actual))

    all_even = sum(
        1 for value in inputs
        if all((ord(char) - ord("0")) % 2 == 0 for char in str(value))
    )
    has_odd = len(inputs) - all_even
    final_digit_odd = sum(value % 2 == 1 for value in inputs)
    final_digit_even = len(inputs) - final_digit_odd
    multi_digit = sum(value >= 10 for value in inputs)

    print("oracle=/reference/canonical.py:digits")
    print("candidate=/tmp/audit-work/source/solution.py:digits")
    print("documented_examples=1->1,4->0,235->15")
    print(
        f"positive_inputs={len(inputs)} multi_digit={multi_digit} "
        f"all_even_digits={all_even} has_odd_digit={has_odd} "
        f"final_digit_odd={final_digit_odd} final_digit_even={final_digit_even}"
    )
    print(f"positive_domain_mismatches={len(mismatches)}")
    if mismatches:
        print(f"first_mismatches={mismatches[:20]}")

    # Boundary observations outside the stated positive-integer contract.
    print(
        "outside_domain_n=0 "
        f"canonical={call_or_exception(canonical, 0)} "
        f"candidate={call_or_exception(candidate, 0)}"
    )
    print(
        "outside_domain_n=-1 "
        f"canonical={call_or_exception(canonical, -1)} "
        f"candidate={call_or_exception(candidate, -1)}"
    )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
