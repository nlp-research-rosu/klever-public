#!/usr/bin/env python3
"""Finite independent checks of both GAP-VERIFICATION simplification rules."""

first_guard_hits = 0
second_guard_hits = 0
first_false_conclusions = []
second_false_conclusions = []

for n in range(0, 101):
    gap = (n + 1) ** 3 - n**3
    for d in range(1, gap):
        threshold = n**3 + d
        for i in range(0, n + 2):
            common = (
                0 <= i
                and i <= n + 1
                and 0 <= n
                and 0 < d
                and d < gap
            )
            first_guard = common and i**3 < threshold
            second_guard = common and i**3 >= threshold
            if first_guard:
                first_guard_hits += 1
                if not (i < n + 1):
                    first_false_conclusions.append((i, n, d))
            if second_guard:
                second_guard_hits += 1
                if not (i == n + 1):
                    second_false_conclusions.append((i, n, d))

print("domain: N=0..100, D=1..((N+1)^3-N^3-1), I=0..N+1")
print(f"first_rule_guard_hits={first_guard_hits}")
print(f"first_rule_false_conclusion_count={len(first_false_conclusions)}")
print(f"second_rule_guard_hits={second_guard_hits}")
print(f"second_rule_false_conclusion_count={len(second_false_conclusions)}")
assert not first_false_conclusions
assert not second_false_conclusions

