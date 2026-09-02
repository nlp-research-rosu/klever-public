#!/usr/bin/env python3
"""Independent differential for HumanEval/131.

The candidate and trusted canonical modules are loaded from explicit paths.
Inputs are deterministic and are also emitted as JSONL for exact reproduction.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def contract_oracle(n: int) -> int:
    """Direct restatement independent of both Python implementations."""
    odd_digits = [int(ch) for ch in str(n) if int(ch) % 2 == 1]
    if not odd_digits:
        return 0
    result = 1
    for digit in odd_digits:
        result *= digit
    return result


def build_cases() -> list[tuple[str, int]]:
    cases: list[tuple[str, int]] = []

    def add(category: str, values: list[int]) -> None:
        cases.extend((category, n) for n in values)

    add("documented-example", [1, 4, 235])
    # Zero is outside the positive-integer contract but exercises the empty loop.
    add("zero-outside-contract", [0])
    add(
        "branch-boundary",
        [
            2,
            3,
            8,
            9,
            10,
            11,
            12,
            19,
            20,
            21,
            101,
            102,
            110,
            111,
            200,
            222,
            2468,
            13579,
            10203,
            909090,
            100000000000000000001,
        ],
    )
    add("exhaustive-small-positive", list(range(1, 10_001)))

    random_source = random.Random(131_20260726)
    random_values: list[int] = []
    for _ in range(500):
        digits = random_source.randint(1, 300)
        first = str(random_source.randint(1, 9))
        rest = "".join(str(random_source.randint(0, 9)) for _ in range(digits - 1))
        random_values.append(int(first + rest))
    add("seeded-random-1-to-300-digits", random_values)

    add(
        "large-structured",
        [
            10**500,
            10**500 + 1,
            10**500 + 3,
            int("9" * 500),
            int("24680" * 100),
            int("13579" * 100),
            int("10203040506070809" * 25),
        ],
    )
    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    canonical_module = load_module("trusted_canonical_131", args.canonical)
    candidate_module = load_module("candidate_solution_131", args.candidate)

    cases = build_cases()
    args.inputs_out.parent.mkdir(parents=True, exist_ok=True)
    mismatches: list[dict[str, str]] = []
    counts: dict[str, int] = {}
    with args.inputs_out.open("w") as stream:
        for index, (category, n) in enumerate(cases):
            expected_contract = contract_oracle(n)
            expected_canonical = canonical_module.digits(n)
            actual = candidate_module.digits(n)
            record = {"index": index, "category": category, "n": str(n)}
            stream.write(json.dumps(record, sort_keys=True) + "\n")
            counts[category] = counts.get(category, 0) + 1
            if not (actual == expected_canonical == expected_contract):
                mismatches.append(
                    {
                        **record,
                        "candidate": str(actual),
                        "canonical": str(expected_canonical),
                        "contract_oracle": str(expected_contract),
                    }
                )

    print(f"candidate={args.candidate}")
    print(f"canonical={args.canonical}")
    print("oracle=independent decimal-digit filter and multiplication")
    print("input_generation_seed=131_20260726")
    print(f"input_count={len(cases)}")
    print(f"category_counts={json.dumps(counts, sort_keys=True)}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:20]:
            print("MISMATCH " + json.dumps(mismatch, sort_keys=True))
        return 1
    print("DIFFERENTIAL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
