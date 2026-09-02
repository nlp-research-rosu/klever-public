#!/usr/bin/env python3
"""Compare the independent recurrence reading with the frozen source loop."""

from __future__ import annotations

import json
import math


def source_loop(n: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor <= n:
        if n % divisor == 0:
            factors.append(divisor)
            n = n // divisor
        else:
            divisor = divisor + 1
    return factors


def factor_acc(acc: list[int], n: int, divisor: int) -> list[int]:
    result = list(acc)
    while True:
        if n < divisor:
            return result
        py_mod = ((n % divisor) + divisor) % divisor
        if py_mod == 0:
            result.append(divisor)
            n = (n - py_mod) // divisor
        else:
            divisor += 1


def prime_factors_oracle(n: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 1
    if n > 1:
        factors.append(n)
    return factors


def main() -> None:
    adversarial = [
        1,
        2,
        3,
        4,
        8,
        25,
        49,
        70,
        97,
        121,
        128,
        997,
        1024,
        2310,
        99991,
    ]
    sample = list(range(1, 2001)) + adversarial
    mismatches = []
    property_failures = []
    for n in sample:
        direct = source_loop(n)
        summary = factor_acc([], n, 2)
        oracle = prime_factors_oracle(n)
        if direct != summary or summary != oracle:
            mismatches.append(
                {
                    "n": n,
                    "source_loop": direct,
                    "factor_acc": summary,
                    "oracle": oracle,
                }
            )
        product = math.prod(summary)
        if (
            product != n
            or summary != sorted(summary)
            or any(
                factor < 2
                or any(factor % d == 0 for d in range(2, factor))
                for factor in summary
            )
        ):
            property_failures.append(
                {"n": n, "factors": summary, "product": product}
            )

    witnesses = {
        str(n): {
            "source_loop": source_loop(n),
            "factor_acc": factor_acc([], n, 2),
        }
        for n in adversarial
    }
    result = {
        "scope": {
            "dense_inputs": "1..2000",
            "adversarial_inputs": adversarial,
            "total_evaluations": len(sample),
        },
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "property_failure_count": len(property_failures),
        "property_failures": property_failures,
        "witnesses": witnesses,
        "guard_analysis": {
            "formal_use_domain": "N >= 1 and D >= 2",
            "base": "N < D",
            "divisible": "D <= N and pyMod(N,D) == 0",
            "nondivisible": "D <= N and pyMod(N,D) != 0",
            "pairwise_disjoint": True,
            "exhaustive_on_use_domain": True,
            "division_by_zero_excluded": True,
        },
        "operational_correspondence": {
            "base": (
                "D <= N is false, so the while exits and returns the current "
                "accumulator"
            ),
            "divisible": (
                "append D; assign N := (N - pyMod(N,D)) / D; preserve D"
            ),
            "nondivisible": "preserve accumulator and N; assign D := D + 1",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
