#!/usr/bin/env python3
"""Independent differential and mathematical-oracle tests for x_or_y."""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.x_or_y


def is_prime_independent(n: int) -> bool:
    if n < 2:
        return False
    return all(n % divisor for divisor in range(2, math.isqrt(n) + 1))


def classify(entry, n: int) -> str:
    x = {"selected": "x", "n": n}
    y = {"selected": "y", "n": n}
    result = entry(n, x, y)
    if result is x:
        return "x"
    if result is y:
        return "y"
    return f"other:{result!r}"


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} CANONICAL.py GENERATED.py", file=sys.stderr)
        return 64
    canonical = load_entry(Path(sys.argv[1]), "trusted_canonical")
    generated = load_entry(Path(sys.argv[2]), "audited_generated")

    named_cases = [
        ("documented-prime", 7, 34, 12),
        ("documented-composite", 15, 8, 5),
        ("negative-boundary", -1, "x-neg", "y-neg"),
        ("zero-boundary", 0, (), ("y",)),
        ("one-boundary", 1, ["x"], ["y"]),
        ("range-empty-prime", 2, {"x": 2}, {"y": 2}),
        ("one-loop-prime", 3, b"x", b"y"),
        ("first-divisor", 4, 41, 42),
        ("later-divisor", 9, 91, 92),
        ("square-composite", 49, 491, 492),
        ("larger-prime", 97, 971, 972),
    ]
    named_results = []
    named_failures = []
    for label, n, x, y in named_cases:
        canonical_result = canonical(n, x, y)
        generated_result = generated(n, x, y)
        expected = x if is_prime_independent(n) else y
        row = {
            "label": label,
            "n": n,
            "canonical": repr(canonical_result),
            "generated": repr(generated_result),
            "oracle": repr(expected),
            "canonical_matches_generated": (
                type(canonical_result) is type(generated_result)
                and canonical_result == generated_result
            ),
            "generated_matches_oracle_by_identity": generated_result is expected,
        }
        named_results.append(row)
        if not row["generated_matches_oracle_by_identity"]:
            named_failures.append(row)

    positive_mismatches = []
    broad_mismatches = []
    oracle_mismatches = []
    for n in range(-20, 301):
        canonical_branch = classify(canonical, n)
        generated_branch = classify(generated, n)
        oracle_branch = "x" if is_prime_independent(n) else "y"
        if canonical_branch != generated_branch:
            mismatch = {
                "n": n,
                "canonical": canonical_branch,
                "generated": generated_branch,
            }
            broad_mismatches.append(mismatch)
            if n >= 1:
                positive_mismatches.append(mismatch)
        if generated_branch != oracle_branch:
            oracle_mismatches.append(
                {"n": n, "generated": generated_branch, "oracle": oracle_branch}
            )

    print("NAMED_CASES=" + json.dumps(named_results, sort_keys=True))
    print("GENERATED_SCOPE=all integers n from -20 through 300 inclusive")
    print("POSITIVE_SCOPE=all integers n from 1 through 300 inclusive")
    print(f"POSITIVE_CANONICAL_MISMATCH_COUNT={len(positive_mismatches)}")
    print("POSITIVE_CANONICAL_MISMATCHES=" + json.dumps(positive_mismatches))
    print(f"BROAD_CANONICAL_MISMATCH_COUNT={len(broad_mismatches)}")
    print("BROAD_CANONICAL_MISMATCHES=" + json.dumps(broad_mismatches))
    print(f"GENERATED_ORACLE_MISMATCH_COUNT={len(oracle_mismatches)}")
    print("GENERATED_ORACLE_MISMATCHES=" + json.dumps(oracle_mismatches))

    # The generated implementation must match the ordinary mathematical contract.
    return 1 if named_failures or oracle_mismatches or positive_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
