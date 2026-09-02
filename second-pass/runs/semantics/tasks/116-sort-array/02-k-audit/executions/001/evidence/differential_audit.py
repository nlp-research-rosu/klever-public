#!/usr/bin/env python3
"""Independent differential test for HumanEval/116-sort-array.

The oracle and candidate modules are imported directly from the trusted and
scratch paths supplied on the command line.  The intended-domain suite contains
only lists of non-negative Python integers.  Contradictory prompt examples and
negative exploratory cases are reported separately.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path
from types import ModuleType
from typing import Callable


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def encode_inputs(cases: list[list[int]]) -> bytes:
    return json.dumps(cases, separators=(",", ":"), ensure_ascii=True).encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    parser.add_argument("--results-out", type=Path, required=True)
    args = parser.parse_args()

    oracle: Callable[[list[int]], list[int]] = load_module(
        "trusted_canonical", args.canonical
    ).sort_array
    generated: Callable[[list[int]], list[int]] = load_module(
        "generated_solution", args.candidate
    ).sort_array

    named: list[tuple[str, list[int]]] = [
        ("empty", []),
        ("singleton_zero", [0]),
        ("singleton_one", [1]),
        ("branch_boundary_0_1", [1, 0]),
        ("duplicates", [3, 3, 0, 7, 1, 1]),
        ("prompt_example_1", [1, 5, 2, 3, 4]),
        ("prompt_example_3", [1, 0, 2, 3, 4]),
        ("binary_boundaries", [0, 1, 2, 3, 4, 7, 8, 15, 16, 31, 32, 33]),
        ("tie_breaks", [10, 9, 6, 5, 3, 12]),
        ("large_ints", [2**128, 2**128 - 1, 2**128 + 1, 2**255]),
    ]

    exhaustive = [
        list(xs)
        for length in range(5)
        for xs in itertools.product(range(9), repeat=length)
    ]

    rng = random.Random(116)
    generated_cases: list[list[int]] = []
    boundary_values = [
        0,
        1,
        2,
        3,
        4,
        7,
        8,
        15,
        16,
        31,
        32,
        63,
        64,
        127,
        128,
        255,
        256,
        2**32 - 1,
        2**32,
        2**63,
    ]
    for _ in range(1000):
        length = rng.randrange(0, 30)
        generated_cases.append(
            [
                rng.choice(boundary_values)
                if rng.random() < 0.55
                else rng.randrange(0, 2**80)
                for _ in range(length)
            ]
        )

    intended_cases = [case for _, case in named] + exhaustive + generated_cases
    mismatches: list[dict[str, object]] = []
    mutation_errors: list[dict[str, object]] = []
    for index, case in enumerate(intended_cases):
        before = list(case)
        expected = oracle(list(case))
        actual = generated(list(case))
        if case != before:
            mutation_errors.append({"index": index, "input": before, "after": case})
        if expected != actual:
            mismatches.append(
                {
                    "index": index,
                    "input": before,
                    "canonical": expected,
                    "candidate": actual,
                }
            )

    contradictory_expectations = [
        {
            "input": [1, 5, 2, 3, 4],
            "prompt_expected": [1, 2, 3, 4, 5],
            "canonical": oracle([1, 5, 2, 3, 4]),
            "candidate": generated([1, 5, 2, 3, 4]),
        },
        {
            "input": [1, 0, 2, 3, 4],
            "prompt_expected": [0, 1, 2, 3, 4],
            "canonical": oracle([1, 0, 2, 3, 4]),
            "candidate": generated([1, 0, 2, 3, 4]),
        },
    ]
    outside_domain = []
    for case in [[-1], [-2, -3, -4, -5, -6], [-1, 0, 1], [-8, -7, -3, 2]]:
        outside_domain.append(
            {
                "input": case,
                "canonical": oracle(list(case)),
                "candidate": generated(list(case)),
            }
        )

    input_bytes = encode_inputs(intended_cases)
    args.inputs_out.write_bytes(input_bytes + b"\n")
    results = {
        "intended_domain": "finite lists of non-negative Python integers",
        "named_count": len(named),
        "exhaustive_scope": "all lists of lengths 0..4 over integer values 0..8",
        "exhaustive_count": len(exhaustive),
        "generated_scope": "1000 deterministic lists, lengths 0..29, seed 116",
        "generated_count": len(generated_cases),
        "total_intended_count": len(intended_cases),
        "inputs_sha256": hashlib.sha256(input_bytes).hexdigest(),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "input_mutation_count": len(mutation_errors),
        "input_mutations": mutation_errors,
        "contradictory_prompt_examples": contradictory_expectations,
        "outside_domain_observations": outside_domain,
    }
    args.results_out.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    return 0 if not mismatches and not mutation_errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
