#!/usr/bin/env python3
"""Independent return-value differential test for HumanEval 120."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add_case(cases, label, arr, k, category):
    cases.append(
        {
            "label": label,
            "arr": list(arr),
            "k": k,
            "category": category,
        }
    )


def build_cases():
    cases = []

    add_case(cases, "example-1", [-3, -4, 5], 3, "documented")
    add_case(cases, "example-2", [4, -4, 4], 2, "documented")
    add_case(
        cases,
        "example-3",
        [-3, 2, 1, 2, -1, -2, 1],
        1,
        "documented",
    )

    # Requested empty case. It is useful behavior evidence but lies outside the
    # prompt's len(arr) >= 1 precondition.
    add_case(cases, "empty-k0", [], 0, "out-of-domain-empty")

    add_case(cases, "single-min-k0", [-1000], 0, "boundary")
    add_case(cases, "single-min-k1", [-1000], 1, "boundary")
    add_case(cases, "single-max-k1", [1000], 1, "boundary")
    add_case(cases, "value-extremes-k1", [-1000, 1000], 1, "boundary")
    add_case(cases, "value-extremes-kn", [-1000, 1000], 2, "boundary")
    add_case(cases, "all-duplicates", [7, 7, 7, 7], 3, "boundary")
    add_case(cases, "mixed-k0", [3, -1, 2], 0, "branch-boundary")
    add_case(cases, "mixed-k1", [3, -1, 2], 1, "branch-boundary")
    add_case(cases, "mixed-k-nminus1", [3, -1, 2], 2, "branch-boundary")
    add_case(cases, "mixed-kn", [3, -1, 2], 3, "branch-boundary")

    length_1000 = [-1000 if i % 2 == 0 else 1000 for i in range(1000)]
    for k in (0, 1, 500, 999, 1000):
        add_case(cases, f"length-1000-k{k}", length_1000, k, "boundary")

    rng = random.Random(120)
    for index in range(500):
        n = rng.randint(1, 80)
        arr = [rng.randint(-1000, 1000) for _ in range(n)]
        boundary_k = [0, 1, max(0, n - 1), n]
        k = boundary_k[index % len(boundary_k)] if index < 200 else rng.randint(0, n)
        add_case(cases, f"generated-{index:03d}", arr, k, "generated")

    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--results-json", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_module(args.canonical, "trusted_canonical_120")
    generated = load_module(args.generated, "audited_generated_120")

    cases = build_cases()
    results = []
    return_mismatches = []
    side_effect_differences = []

    for case in cases:
        original = case["arr"]
        canonical_arg = list(original)
        generated_arg = list(original)
        canonical_result = canonical.maximum(canonical_arg, case["k"])
        generated_result = generated.maximum(generated_arg, case["k"])
        return_equal = canonical_result == generated_result
        side_effect_equal = canonical_arg == generated_arg
        row = {
            **case,
            "canonical_result": canonical_result,
            "generated_result": generated_result,
            "return_equal": return_equal,
            "canonical_argument_after": canonical_arg,
            "generated_argument_after": generated_arg,
            "side_effect_equal": side_effect_equal,
        }
        results.append(row)
        if not return_equal:
            return_mismatches.append(case["label"])
        if not side_effect_equal:
            side_effect_differences.append(case["label"])

    serialized = json.dumps(results, sort_keys=True, separators=(",", ":")).encode()
    args.results_json.write_bytes(json.dumps(results, indent=2, sort_keys=True).encode())

    print(f"canonical={args.canonical}")
    print(f"generated={args.generated}")
    print("domain=len 1..1000; integer elements -1000..1000; 0 <= k <= len")
    print("oracle=trusted canonical.py, imported independently")
    print("generated sample seed=120; generated cases=500")
    print(f"total_cases={len(results)}")
    print(f"intended_domain_cases={sum(r['category'] != 'out-of-domain-empty' for r in results)}")
    print("out_of_domain_cases=1 (empty array with k=0)")
    print(f"return_mismatches={len(return_mismatches)}")
    print(f"return_mismatch_labels={return_mismatches}")
    print(f"side_effect_differences={len(side_effect_differences)}")
    print("side_effect_note=canonical sorts its argument for k>0; generated leaves it unchanged")
    print(f"results_sha256={hashlib.sha256(serialized).hexdigest()}")
    print(f"results_json={args.results_json}")
    print("selected_results:")
    for row in results[:19]:
        canonical_result = row["canonical_result"]
        generated_result = row["generated_result"]
        if len(canonical_result) > 20:
            canonical_result = {
                "length": len(canonical_result),
                "first_5": canonical_result[:5],
                "last_5": canonical_result[-5:],
            }
        if len(generated_result) > 20:
            generated_result = {
                "length": len(generated_result),
                "first_5": generated_result[:5],
                "last_5": generated_result[-5:],
            }
        print(
            json.dumps(
                {
                    "label": row["label"],
                    "arr_length": len(row["arr"]),
                    "k": row["k"],
                    "canonical_result": canonical_result,
                    "generated_result": generated_result,
                    "return_equal": row["return_equal"],
                },
                sort_keys=True,
            )
        )

    return 0 if not return_mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
