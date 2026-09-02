#!/usr/bin/env python3
"""Independent canonical/generated differential and bounded contract oracle."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_equal_to_sum_even


def brute_contract(n: int) -> bool:
    positive_evens = range(2, max(2, n + 1), 2)
    return any(sum(parts) == n for parts in itertools.product(positive_evens, repeat=4))


def main() -> int:
    canonical = load_function(
        Path("/tmp/audit-work/138-audit/canonical.py"), "trusted_canonical"
    )
    generated = load_function(
        Path("/tmp/audit-work/138-audit/scratch/solution.py"), "generated_solution"
    )

    documented = [4, 6, 8]
    branch_boundaries = [-10, -2, -1, 0, 1, 2, 6, 7, 8, 9, 10, 11, 12]
    large = [
        -(10**100),
        -(10**30 + 1),
        10**30,
        10**30 + 1,
        10**100,
        10**100 + 1,
    ]
    rng = random.Random(138)
    generated_inputs = [rng.randint(-(10**18), 10**18) for _ in range(500)]
    inputs = list(dict.fromkeys(documented + branch_boundaries + large + generated_inputs))

    mismatches = []
    for n in inputs:
        left = canonical(n)
        right = generated(n)
        if left != right:
            mismatches.append((n, left, right))

    brute_mismatches = []
    for n in range(-20, 81):
        expected = brute_contract(n)
        canonical_result = canonical(n)
        generated_result = generated(n)
        if expected != canonical_result or expected != generated_result:
            brute_mismatches.append((n, expected, canonical_result, generated_result))

    print("documented_examples:", [(n, canonical(n), generated(n)) for n in documented])
    print(
        "branch_boundaries:",
        [(n, canonical(n), generated(n)) for n in branch_boundaries],
    )
    print("differential_input_count:", len(inputs))
    print("differential_mismatch_count:", len(mismatches))
    print("bounded_bruteforce_domain: integers [-20, 80]")
    print("bounded_bruteforce_mismatch_count:", len(brute_mismatches))
    if mismatches:
        print("differential_mismatches:", mismatches[:20])
    if brute_mismatches:
        print("bounded_bruteforce_mismatches:", brute_mismatches[:20])
    print("empty_case: not applicable; the source-contract domain is integer-valued")
    return 0 if not mismatches and not brute_mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
