#!/usr/bin/env python3
"""Independent docstring/canonical/candidate differential for HumanEval 122."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.add_elements


candidate = load_entry(
    Path("/tmp/audit-work/122-add-elements/solution.py"), "audit_candidate_solution"
)
canonical = load_entry(Path("/reference/canonical.py"), "audit_trusted_canonical")


def docstring_oracle(arr: list[int], k: int) -> int:
    # "Digits" counts the decimal digits of the integer's magnitude; '-' is not
    # a digit. This is independently written and does not call either program.
    return sum(value for value in arr[:k] if abs(value) <= 99)


def main() -> int:
    domain_cases: list[tuple[str, list[int], int]] = [
        ("documented-example", [111, 21, 3, 4000, 5, 6, 7, 8, 9], 4),
        ("minimum-length", [7], 1),
        ("negative-two-digit", [-99], 1),
        ("lower-exclusion", [-100], 1),
        ("upper-inclusion", [99], 1),
        ("upper-exclusion", [100], 1),
        ("first-k-stop", [5, 100, 7], 1),
        ("full-prefix", [5, 100, 7], 3),
        ("large-integers", [10**100, -(10**100), -9, 9], 4),
        ("maximum-length-k1", list(range(-50, 50)), 1),
        ("maximum-length-k100", list(range(-50, 50)), 100),
    ]

    boundary_values = [-101, -100, -99, -10, -9, 0, 9, 10, 99, 100, 101]
    for length in range(1, 5):
        for values in itertools.product(boundary_values, repeat=length):
            arr = list(values)
            for k in range(1, length + 1):
                domain_cases.append((f"exhaustive-small-len-{length}", arr, k))

    rng = random.Random(122)
    pool = boundary_values + [
        -(10**100),
        -999_999_999,
        10**100,
        999_999_999,
    ]
    for case_index in range(2000):
        length = rng.randint(1, 100)
        arr = [rng.choice(pool) if rng.randrange(3) == 0 else rng.randint(-10000, 10000)
               for _ in range(length)]
        k = rng.randint(1, length)
        domain_cases.append((f"generated-{case_index}", arr, k))

    candidate_doc_mismatches = []
    canonical_doc_mismatches = []
    candidate_canonical_mismatches = []
    for label, arr, k in domain_cases:
        got_candidate = candidate(list(arr), k)
        got_canonical = canonical(list(arr), k)
        expected = docstring_oracle(arr, k)
        record = (label, arr, k, got_candidate, got_canonical, expected)
        if got_candidate != expected:
            candidate_doc_mismatches.append(record)
        if got_canonical != expected:
            canonical_doc_mismatches.append(record)
        if got_candidate != got_canonical:
            candidate_canonical_mismatches.append(record)

    outside_cases = [
        ("empty-k0", [], 0),
        ("k0", [1, 2], 0),
        ("k-too-large", [1, 2], 3),
        ("negative-k", [1, 2], -1),
    ]

    print(f"domain_cases={len(domain_cases)}")
    print(f"candidate_docstring_mismatches={len(candidate_doc_mismatches)}")
    print(f"canonical_docstring_mismatches={len(canonical_doc_mismatches)}")
    print(
        "candidate_canonical_mismatches="
        f"{len(candidate_canonical_mismatches)}"
    )
    print("candidate_canonical_mismatch_samples:")
    for record in candidate_canonical_mismatches[:8]:
        print(repr(record))
    print("documented_and_branch_boundary_results:")
    for label, arr, k in domain_cases[:11]:
        print(
            repr(
                (
                    label,
                    arr,
                    k,
                    candidate(list(arr), k),
                    canonical(list(arr), k),
                    docstring_oracle(arr, k),
                )
            )
        )
    print("outside_contract_observations:")
    for label, arr, k in outside_cases:
        print(repr((label, arr, k, candidate(list(arr), k), canonical(list(arr), k))))
    return 0 if not candidate_doc_mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
