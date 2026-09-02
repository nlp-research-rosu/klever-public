#!/usr/bin/env python3
"""Compare each grounded K claim postcondition to both Python entry points."""

from __future__ import annotations

import importlib.util


def load_function(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_integers


canonical = load_function("trusted_canonical_stage4", "/reference/canonical.py")
generated = load_function(
    "submitted_solution_stage4", "/tmp/audit-work/22-filter-integers/solution.py"
)

witnesses = [
    ("empty", [], []),
    ("prompt-example-one", ["", 2.5, 5], [5]),
    ("prompt-example-two", [1, 2, 3, "", {}, []], [1, 2, 3]),
    ("order-and-scalars", [False, 1, None, "", 2], [1, 2]),
]

mismatches = 0
for label, values, claimed_k_result in witnesses:
    canonical_result = canonical(values)
    generated_result = generated(values)
    implementations_agree = canonical_result == generated_result
    claim_matches_python = claimed_k_result == canonical_result
    print(
        f"{label}: input={values!r} claimed_k={claimed_k_result!r} "
        f"canonical={canonical_result!r} generated={generated_result!r} "
        f"implementations_agree={implementations_agree} "
        f"claim_matches_python={claim_matches_python}"
    )
    assert implementations_agree
    if not claim_matches_python:
        mismatches += 1

print(f"grounded_claim_python_mismatches={mismatches}")
assert mismatches == 1
print("expected_bool_domain_mismatch_observed=true")
