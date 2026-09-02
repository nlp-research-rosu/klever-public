#!/usr/bin/env python3
"""Independent finite-domain adequacy checks for HumanEval 84-solve."""

from __future__ import annotations


def frozen_source_formula(n: int) -> int:
    return (
        n % 10
        + (n // 10) % 10
        + (n // 100) % 10
        + (n // 1000) % 10
        + (n // 10000) % 10
    )


def independent_decimal_sum(n: int) -> int:
    total = 0
    while True:
        total += n % 10
        n //= 10
        if n == 0:
            return total


def independent_binary(n: int) -> str:
    if n == 0:
        return "0"
    digits: list[str] = []
    while n:
        digits.append("1" if n % 2 else "0")
        n //= 2
    return "".join(reversed(digits))


def main() -> None:
    mismatches = []
    for n in range(10001):
        source_sum = frozen_source_formula(n)
        oracle_sum = independent_decimal_sum(n)
        source_output = bin(source_sum)[2:]
        oracle_output = independent_binary(oracle_sum)
        if (source_sum, source_output) != (oracle_sum, oracle_output):
            mismatches.append((n, source_sum, oracle_sum, source_output, oracle_output))
    print("domain=all integers 0..10000 inclusive")
    print(f"case_count={10001}")
    print(f"mismatch_count={len(mismatches)}")
    print(f"boundary_samples={[0, 1, 9, 10, 147, 150, 9999, 10000]}")
    print(
        "boundary_outputs="
        + repr(
            [
                (n, bin(frozen_source_formula(n))[2:])
                for n in [0, 1, 9, 10, 147, 150, 9999, 10000]
            ]
        )
    )
    omitted_high_place = (
        10000 % 10
        + (10000 // 10) % 10
        + (10000 // 100) % 10
        + (10000 // 1000) % 10
    )
    print(
        "counterfactual_omit_10000_place="
        f"{bin(omitted_high_place)[2:]!r}; expected='1'"
    )
    print(
        "counterfactual_slice_from_1="
        f"{bin(frozen_source_formula(147))[1:]!r}; expected='1100'"
    )
    print("RESULT=" + ("PASS" if not mismatches else "FAIL"))


if __name__ == "__main__":
    main()
