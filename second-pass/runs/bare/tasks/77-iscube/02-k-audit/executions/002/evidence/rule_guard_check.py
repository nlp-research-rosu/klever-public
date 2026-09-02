#!/usr/bin/env python3
"""Finite boundary audit of the two GAP-VERIFICATION simplification lemmas."""

from __future__ import annotations


def main() -> None:
    first_premises = 0
    second_premises = 0
    first_violations: list[tuple[int, int, int]] = []
    second_violations: list[tuple[int, int, int]] = []

    for n in range(0, 31):
        gap = (n + 1) ** 3 - n**3
        for d in range(1, gap):
            for i in range(0, n + 2):
                common = (
                    0 <= i
                    and i <= n + 1
                    and 0 <= n
                    and 0 < d
                    and d < gap
                )
                first_guard = common and i**3 < n**3 + d
                second_guard = common and i**3 >= n**3 + d
                if first_guard:
                    first_premises += 1
                    if not (i < n + 1):
                        first_violations.append((n, d, i))
                if second_guard:
                    second_premises += 1
                    if not (i == n + 1):
                        second_violations.append((n, d, i))

    print("range: N=0..30, D=1..((N+1)^3-N^3-1), I=0..N+1")
    print(f"lemma1_satisfying_guards={first_premises}")
    print(f"lemma1_false_conclusions={len(first_violations)}")
    print(f"lemma2_satisfying_guards={second_premises}")
    print(f"lemma2_false_conclusions={len(second_violations)}")
    if first_violations or second_violations:
        print(f"lemma1_examples={first_violations[:10]}")
        print(f"lemma2_examples={second_violations[:10]}")
        raise SystemExit(1)
    print("RULE_GUARD_CHECK: PASS")


if __name__ == "__main__":
    main()
