#!/usr/bin/env python3
"""Ground witnesses for every entry precondition and its formal postcondition."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.even_odd_palindrome


def leading_digit(n: int) -> int:
    return n // 100


def current_block(n: int) -> int:
    # The K expression uses truncating /Int after adding 10. Its numerator is
    # nonnegative on the three-digit claim domain, so Python // agrees.
    return (n % 100 - leading_digit(n) + 10) // 10


def formal_postcondition(n: int) -> tuple[int, int]:
    if 1 <= n < 10:
        return n // 2, (n + 1) // 2
    if 10 <= n < 100:
        return 4 + (n // 11) // 2, 5 + ((n // 11) + 1) // 2
    if 100 <= n < 1000:
        leading = leading_digit(n)
        block = current_block(n)
        even = 8 + 10 * ((leading - 1) // 2)
        odd = 10 + 10 * (leading // 2)
        if leading % 2 == 0:
            even += block
        else:
            odd += block
        return even, odd
    if n == 1000:
        return 48, 60
    raise ValueError("outside the four entry claims")


canonical = load_entry("trusted_canonical_ground", Path("/reference/canonical.py"))
submitted = load_entry(
    "submitted_solution_ground", Path("/tmp/audit-work/reconstruction/solution.py")
)

witnesses = {
    "claim_1_1_to_9": 3,
    "claim_2_10_to_99": 12,
    "claim_3_100_to_999": 222,
    "claim_4_n_1000": 1000,
}

rows = []
for claim, n in witnesses.items():
    formal = formal_postcondition(n)
    trusted = canonical(n)
    generated = submitted(n)
    rows.append(
        {
            "claim": claim,
            "n": n,
            "formal_postcondition": formal,
            "canonical": trusted,
            "submitted": generated,
            "all_equal": formal == trusted == generated,
        }
    )

mismatches = []
for n in range(1, 1001):
    formal = formal_postcondition(n)
    if formal != canonical(n) or formal != submitted(n):
        mismatches.append(
            {
                "n": n,
                "formal": formal,
                "canonical": canonical(n),
                "submitted": submitted(n),
            }
        )

print("GROUND_WITNESSES:", json.dumps(rows, sort_keys=True))
print(
    "EXHAUSTIVE_FORMAL_SUMMARY_CHECK:",
    json.dumps(
        {"tested": 1000, "mismatch_count": len(mismatches), "mismatches": mismatches},
        sort_keys=True,
    ),
)
sys.exit(1 if mismatches else 0)
