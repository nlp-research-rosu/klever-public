#!/usr/bin/env python3
"""Independent candidate/canonical differential and finite contract check."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


CANONICAL_PATH = Path("/tmp/audit-work/review-138/reference-src/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/review-138/candidate-src/solution.py")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_equal_to_sum_even


def brute_sum_of_four_positive_evens(n: int) -> bool:
    if n < 8:
        return False
    positive_evens = range(2, n + 1, 2)
    return any(sum(parts) == n for parts in itertools.product(positive_evens, repeat=4))


def main() -> None:
    canonical = load_function(CANONICAL_PATH, "trusted_canonical_138")
    candidate = load_function(CANDIDATE_PATH, "candidate_solution_138")

    documented_examples = [4, 6, 8]
    branch_and_boundary_cases = [
        -10**100,
        -10**18,
        -10,
        -2,
        -1,
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        10**18,
        10**100,
        10**100 + 1,
    ]
    exhaustive_small = list(range(-256, 257))
    rng = random.Random(138)
    generated_cases = [rng.randint(-(10**18), 10**18) for _ in range(200)]
    all_inputs = sorted(
        set(
            documented_examples
            + branch_and_boundary_cases
            + exhaustive_small
            + generated_cases
        )
    )

    mismatches = []
    non_bool_results = []
    for n in all_inputs:
        expected = canonical(n)
        actual = candidate(n)
        if not isinstance(expected, bool) or not isinstance(actual, bool):
            non_bool_results.append((n, type(expected).__name__, type(actual).__name__))
        if expected != actual:
            mismatches.append((n, expected, actual))

    contract_inputs = list(range(-20, 101))
    contract_mismatches = []
    for n in contract_inputs:
        brute = brute_sum_of_four_positive_evens(n)
        canonical_result = canonical(n)
        candidate_result = candidate(n)
        if brute != canonical_result or brute != candidate_result:
            contract_mismatches.append((n, brute, canonical_result, candidate_result))

    print(f"CANONICAL_PATH={CANONICAL_PATH}")
    print(f"CANDIDATE_PATH={CANDIDATE_PATH}")
    print("INTENDED_DOMAIN=Python integers; scalar input has no empty case")
    print(f"DOCUMENTED_EXAMPLES={json.dumps(documented_examples)}")
    print(f"BRANCH_AND_BOUNDARY_CASES={json.dumps(branch_and_boundary_cases)}")
    print("GENERATED_CASES_SEED=138")
    print("GENERATED_CASES_COUNT=200")
    print(f"ALL_INPUTS_COUNT={len(all_inputs)}")
    print(f"ALL_INPUTS_JSON={json.dumps(all_inputs)}")
    print(f"NON_BOOL_RESULTS={json.dumps(non_bool_results)}")
    print(f"DIFFERENTIAL_MISMATCHES={json.dumps(mismatches)}")
    print(f"CONTRACT_INPUTS={json.dumps(contract_inputs)}")
    print(f"CONTRACT_MISMATCHES={json.dumps(contract_mismatches)}")

    if non_bool_results or mismatches or contract_mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
