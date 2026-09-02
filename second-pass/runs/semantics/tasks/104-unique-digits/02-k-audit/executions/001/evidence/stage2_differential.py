#!/usr/bin/env python3
"""Independent differential test for HumanEval/104 unique_digits."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import random
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.unique_digits


def outcome(function: Callable[[list[int]], list[int]], values: list[int]) -> dict:
    try:
        return {"kind": "return", "value": function(list(values))}
    except Exception as error:  # Deliberately records out-of-domain behavior.
        return {"kind": "exception", "type": type(error).__name__, "text": str(error)}


def intended_inputs() -> list[list[int]]:
    examples_and_boundaries = [
        [15, 33, 1422, 1],
        [152, 323, 1422, 10],
        [],
        [1],
        [2],
        [9],
        [10],
        [11],
        [12],
        [21],
        [22],
        [111111],
        [111112],
        [211111],
        [111211],
        [97531, 11, 2468, 7, 13570, 3],
        [99, 1, 99, 13, 2, 13],
        [10**50 + 1, int("9" * 60), int("1" * 60)],
    ]

    # Exhaustive singleton coverage catches every digit/loop branch for 1..20000.
    cases = examples_and_boundaries + [[number] for number in range(1, 20001)]

    pair_values = [1, 2, 9, 10, 11, 12, 19, 20, 21, 22, 99, 101, 111, 135, 246]
    cases.extend([[left, right] for left in pair_values for right in pair_values])

    triple_values = [1, 2, 10, 11, 19, 20, 99, 135]
    cases.extend(
        [[first, second, third]
         for first in triple_values
         for second in triple_values
         for third in triple_values]
    )

    rng = random.Random(104)
    for _ in range(5000):
        length = rng.randrange(0, 13)
        cases.append([rng.randrange(1, 10**18) for _ in range(length)])

    # Systematically put each decimal digit at each position in varying widths.
    for width in range(1, 19):
        for position in range(width):
            for digit in "0123456789":
                chars = ["1"] * width
                chars[position] = digit
                if chars[0] == "0":
                    chars[0] = "2"
                cases.append([int("".join(chars))])

    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs-out", required=True, type=Path)
    args = parser.parse_args()

    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_104")
    generated = load_entry(
        Path("/tmp/audit-work/candidate-src/solution.py"), "candidate_solution_104"
    )

    inputs = intended_inputs()
    args.inputs_out.write_text(
        json.dumps(
            {
                "domain": "finite lists of positive Python integers",
                "generator": {
                    "singletons": "1..20000 inclusive",
                    "random_seed": 104,
                    "random_lists": 5000,
                    "systematic_decimal_widths": "1..18",
                },
                "inputs": inputs,
            },
            separators=(",", ":"),
        )
        + "\n",
        encoding="utf-8",
    )

    mismatches = []
    for index, values in enumerate(inputs):
        expected = outcome(canonical, values)
        actual = outcome(generated, values)
        if actual != expected:
            mismatches.append(
                {"index": index, "input": values, "canonical": expected, "generated": actual}
            )
            if len(mismatches) >= 20:
                break

    excluded = []
    for values in ([0], [0, 1], [-1], [-13], [1, 0, 3]):
        excluded.append(
            {
                "input": values,
                "canonical": outcome(canonical, values),
                "generated": outcome(generated, values),
            }
        )

    encoded = args.inputs_out.read_bytes()
    summary = {
        "intended_domain_cases": len(inputs),
        "intended_domain_mismatches": len(mismatches),
        "first_mismatches": mismatches,
        "inputs_sha256": hashlib.sha256(encoded).hexdigest(),
        "out_of_domain_observations": excluded,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
