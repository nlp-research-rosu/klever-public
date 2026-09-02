#!/usr/bin/env python3
"""Independent differential test for HumanEval 104.

The oracle is loaded from the trusted /reference/canonical.py.  The candidate
entry point is loaded from the clean scratch copy of candidate solution.py.
All generated cases stay within the documented domain: lists of positive ints.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_cases() -> tuple[list[list[int]], dict[str, int]]:
    documented = [
        [15, 33, 1422, 1],
        [152, 323, 1422, 10],
    ]
    boundaries = [
        [],
        [1],
        [2],
        [9],
        [10],
        [11],
        [12],
        [19],
        [20],
        [99],
        [100],
        [101],
        [111],
        [13579],
        [13570],
        [97531],
        [999999999999999999999999999999],
        [10**200 - 1],
        [10**200 + 1],
        [33, 1, 15, 33, 3],
        [222, 111, 2, 1],
    ]

    branch_values = [1, 2, 9, 10, 11, 12, 15, 20, 33, 99, 100, 101, 135, 222]
    exhaustive = [
        list(values)
        for length in range(4)
        for values in itertools.product(branch_values, repeat=length)
    ]
    singletons = [[value] for value in range(1, 301)]

    rng = random.Random(104)
    generated = []
    for _ in range(1000):
        length = rng.randrange(0, 13)
        generated.append([rng.randrange(1, 10**30) for _ in range(length)])

    cases = documented + boundaries + exhaustive + singletons + generated
    counts = {
        "documented": len(documented),
        "boundaries": len(boundaries),
        "exhaustive_products_length_0_to_3": len(exhaustive),
        "singletons_1_to_300": len(singletons),
        "seeded_generated": len(generated),
        "total": len(cases),
    }
    return cases, counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_module(args.canonical, "trusted_canonical")
    candidate = load_module(args.candidate, "candidate_solution")
    cases, counts = build_cases()

    args.inputs_out.write_text(json.dumps(cases, separators=(",", ":")) + "\n")
    serialized = args.inputs_out.read_bytes()

    expected_examples = {
        0: [1, 15, 33],
        1: [],
    }
    mismatches = []
    mutation_failures = []
    for index, values in enumerate(cases):
        canonical_input = list(values)
        candidate_input = list(values)
        expected = canonical.unique_digits(canonical_input)
        actual = candidate.unique_digits(candidate_input)
        if index in expected_examples and expected != expected_examples[index]:
            mismatches.append(
                {
                    "index": index,
                    "kind": "trusted-example-disagrees-with-prompt",
                    "expected_from_prompt": expected_examples[index],
                    "canonical": expected,
                }
            )
        if actual != expected:
            mismatches.append(
                {
                    "index": index,
                    "input": values,
                    "canonical": expected,
                    "candidate": actual,
                }
            )
        if canonical_input != values or candidate_input != values:
            mutation_failures.append(
                {
                    "index": index,
                    "input": values,
                    "canonical_after": canonical_input,
                    "candidate_after": candidate_input,
                }
            )

    print(f"case_counts={json.dumps(counts, sort_keys=True)}")
    print(f"inputs_sha256={hashlib.sha256(serialized).hexdigest()}")
    print(f"mismatch_count={len(mismatches)}")
    print(f"input_mutation_count={len(mutation_failures)}")
    if mismatches:
        print(json.dumps(mismatches[:10], sort_keys=True))
    if mutation_failures:
        print(json.dumps(mutation_failures[:10], sort_keys=True))
    return 1 if mismatches or mutation_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
