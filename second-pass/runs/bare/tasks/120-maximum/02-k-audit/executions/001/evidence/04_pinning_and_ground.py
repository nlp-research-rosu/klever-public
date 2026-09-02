#!/usr/bin/env python3
"""Mechanical pinning checks plus concrete satisfying claim witnesses."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/120-maximum-audit/src")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compact_k(text):
    return re.sub(r"\s+", "", text)


def maximum_spec_ground(arr, k):
    sorted_values = sorted(arr)
    prefix_to_drop = len(arr) - k
    return sorted_values[prefix_to_drop:]


def main():
    solution_mpy = (SCRATCH / "solution.mpy").read_text()
    regenerated_mpy = (SCRATCH / "regenerated-solution.mpy").read_text()
    spec_k = (SCRATCH / "spec.k").read_text()
    verification_k = (SCRATCH / "verification.k").read_text()

    identity = solution_mpy.encode() == regenerated_mpy.encode()
    entry_term_pinned = compact_k(solution_mpy) in compact_k(spec_k)
    postcondition_result_constraining = (
        '<out>noResult=>listVal(maximumSpec(L,K))</out>' in compact_k(spec_k)
    )
    expected_definition = (
        "maximumSpec(L:List,K:Int)"
        "=>dropInts(size(L)-IntK,sortInts(L))"
    )
    spec_definition_present = compact_k(expected_definition) in compact_k(verification_k)

    canonical = load(Path("/reference/canonical.py"), "trusted_canonical_ground")
    generated = load(SCRATCH / "solution.py", "generated_solution_ground")

    witnesses = [
        ([-3, -4, 5], 3),
        ([4, -4, 4], 2),
        ([-3, 2, 1, 2, -1, -2, 1], 1),
        ([7, -1], 0),
        ([-1000, 1000], 1),
    ]
    rows = []
    for arr, k in witnesses:
        precondition = 0 <= k <= len(arr)
        claimed_result = maximum_spec_ground(arr, k)
        canonical_result = canonical.maximum(list(arr), k)
        generated_result = generated.maximum(list(arr), k)
        rows.append(
            {
                "L": arr,
                "K": k,
                "size(L)": len(arr),
                "precondition_0_le_K_le_size_L": precondition,
                "maximumSpec_ground_expansion": {
                    "sortInts(L)": sorted(arr),
                    "size(L)-K": len(arr) - k,
                    "dropInts_result": claimed_result,
                },
                "trusted_canonical_result": canonical_result,
                "generated_python_result": generated_result,
                "all_equal": (
                    precondition
                    and claimed_result == canonical_result == generated_result
                ),
            }
        )

    checks = {
        "submitted_equals_trusted_regeneration": identity,
        "submitted_module_term_occurs_exactly_in_entry_claim_after_whitespace_normalization": entry_term_pinned,
        "postcondition_is_listVal_maximumSpec_of_L_and_K": postcondition_result_constraining,
        "maximumSpec_definition_is_expected_sort_then_drop_expression": spec_definition_present,
        "all_ground_witnesses_satisfy_and_agree": all(r["all_equal"] for r in rows),
    }
    print(json.dumps(checks, indent=2, sort_keys=True))
    for row in rows:
        print(json.dumps(row, sort_keys=True))
    print(f"solution_mpy_sha256={hashlib.sha256(solution_mpy.encode()).hexdigest()}")
    print(f"failed_checks={[name for name, passed in checks.items() if not passed]}")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
