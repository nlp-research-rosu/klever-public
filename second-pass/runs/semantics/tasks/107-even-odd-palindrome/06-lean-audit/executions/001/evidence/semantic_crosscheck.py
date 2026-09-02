#!/usr/bin/env python3
"""Independent finite checks of the frozen source and Stage 3 summaries."""

from __future__ import annotations

import json
from pathlib import Path


def source_model(n: int) -> tuple[int, int]:
    if n < 10:
        return n // 2, (n + 1) // 2
    if n < 100:
        two_digit = n // 11
        return 4 + two_digit // 2, 5 + (two_digit + 1) // 2
    if n == 1000:
        return 48, 60
    hundreds = n // 100
    current_block = (n % 100 - hundreds) // 10 + 1
    even = 8 + 10 * ((hundreds - 1) // 2)
    odd = 10 + 10 * (hundreds // 2)
    if hundreds % 2 == 0:
        even += current_block
    else:
        odd += current_block
    return even, odd


def stage3_summary(n: int) -> tuple[int, int]:
    leading_digit = n // 100
    current_block = (n % 100 - leading_digit + 10) // 10
    if 1 <= n < 10:
        return n // 2, (n + 1) // 2
    if 10 <= n < 100:
        return 4 + (n // 11) // 2, 5 + ((n // 11) + 1) // 2
    if 100 <= n < 1000:
        even = 8 + 10 * ((leading_digit - 1) // 2)
        odd = 10 + 10 * (leading_digit // 2)
        if leading_digit % 2 == 0:
            even += current_block
        else:
            odd += current_block
        return even, odd
    if n == 1000:
        return 48, 60
    raise ValueError("outside frozen theorem domain")


def independent_oracle(n: int) -> tuple[int, int]:
    even = 0
    odd = 0
    for value in range(1, n + 1):
        digits = str(value)
        if digits == digits[::-1]:
            if value % 2 == 0:
                even += 1
            else:
                odd += 1
    return even, odd


def mutant_missing_current_block_increment(n: int) -> tuple[int, int]:
    if n < 100 or n == 1000:
        return stage3_summary(n)
    leading_digit = n // 100
    current_block = (n % 100 - leading_digit) // 10
    even = 8 + 10 * ((leading_digit - 1) // 2)
    odd = 10 + 10 * (leading_digit // 2)
    if leading_digit % 2 == 0:
        even += current_block
    else:
        odd += current_block
    return even, odd


def mutant_swapped_parity_branch(n: int) -> tuple[int, int]:
    if n < 100 or n == 1000:
        return stage3_summary(n)
    leading_digit = n // 100
    current_block = (n % 100 - leading_digit + 10) // 10
    even = 8 + 10 * ((leading_digit - 1) // 2)
    odd = 10 + 10 * (leading_digit // 2)
    if leading_digit % 2 == 0:
        odd += current_block
    else:
        even += current_block
    return even, odd


def mutant_upper_bound(n: int) -> tuple[int, int]:
    if n == 1000:
        return 47, 60
    return stage3_summary(n)


def first_mismatches(model, limit: int = 8) -> list[dict]:
    result = []
    for n in range(1, 1001):
        expected = independent_oracle(n)
        observed = model(n)
        if observed != expected:
            result.append(
                {"n": n, "observed": observed, "oracle": expected}
            )
            if len(result) == limit:
                break
    return result


def main() -> None:
    all_inputs = range(1, 1001)
    source_mismatches = [
        n for n in all_inputs if source_model(n) != independent_oracle(n)
    ]
    summary_mismatches = [
        n for n in all_inputs if stage3_summary(n) != independent_oracle(n)
    ]
    source_summary_mismatches = [
        n for n in all_inputs if source_model(n) != stage3_summary(n)
    ]
    guard_memberships = {
        n: sum(
            (
                1 <= n < 10,
                10 <= n < 100,
                100 <= n < 1000,
                n == 1000,
            )
        )
        for n in all_inputs
    }
    edge_inputs = [
        1,
        2,
        3,
        8,
        9,
        10,
        11,
        12,
        21,
        22,
        98,
        99,
        100,
        101,
        109,
        110,
        111,
        190,
        191,
        199,
        200,
        202,
        909,
        919,
        989,
        999,
        1000,
    ]
    document = {
        "domain": {"minimum": 1, "maximum": 1000, "size": 1000},
        "source_vs_oracle_mismatch_count": len(source_mismatches),
        "summary_vs_oracle_mismatch_count": len(summary_mismatches),
        "source_vs_summary_mismatch_count": len(source_summary_mismatches),
        "guard_coverage_exactly_one_for_every_input": all(
            count == 1 for count in guard_memberships.values()
        ),
        "edge_examples": [
            {
                "n": n,
                "source": source_model(n),
                "summary": stage3_summary(n),
                "oracle": independent_oracle(n),
            }
            for n in edge_inputs
        ],
        "counterfactual_mutations": {
            "missing_current_block_increment": first_mismatches(
                mutant_missing_current_block_increment
            ),
            "swapped_parity_branch": first_mismatches(
                mutant_swapped_parity_branch
            ),
            "upper_bound_even_off_by_one": first_mismatches(
                mutant_upper_bound
            ),
        },
    }
    output = Path("/audit-output/evidence/semantic-crosscheck.json")
    output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    print(json.dumps(document, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
