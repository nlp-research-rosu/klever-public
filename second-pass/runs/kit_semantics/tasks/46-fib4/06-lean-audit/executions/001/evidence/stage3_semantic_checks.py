#!/usr/bin/env python3
"""Independent finite checks of the frozen loop transition and fib4 summary."""


def summary(n: int) -> int:
    if n <= 0:
        return 0
    values = [0, 0, 2, 0]
    if n < 4:
        return values[n]
    for index in range(4, n + 1):
        values.append(sum(values[index - 4 : index]))
    return values[n]


def frozen_loop_transition(n: int, *, initial_c: int = 2) -> int:
    # Independent simulation of the ordered MPY assignments in solution.mpy.
    a, b, c, d, e, i = 0, 0, initial_c, 0, 0, 0
    while i < n:
        e = a + b + c + d
        a = b
        b = c
        c = d
        d = e
        i = i + 1
    return a


def mutated_three_term_summary(n: int) -> int:
    if n <= 0:
        return 0
    values = [0, 0, 2, 0]
    if n < 4:
        return values[n]
    for index in range(4, n + 1):
        values.append(sum(values[index - 3 : index]))
    return values[n]


print("case partition: N<=0 | N=1 | N=2 | N=3 | N>=4")
print("partition is pairwise disjoint and exhaustive over mathematical integers")
print("recurrence calls N-1,N-2,N-3,N-4 only under N>=4; every call decreases N")

mismatches = []
for n in range(-8, 31):
    operational = frozen_loop_transition(n)
    specified = summary(n)
    print(f"n={n:3d} operational={operational:8d} summary={specified:8d}")
    if operational != specified:
        mismatches.append((n, operational, specified))
print(f"operational/summary mismatches={mismatches}")

print("counterfactual initial-c mutation at n=2:")
print(f"  frozen c=2 result={frozen_loop_transition(2, initial_c=2)}")
print(f"  mutated c=3 result={frozen_loop_transition(2, initial_c=3)}")
print(f"  summary result={summary(2)}")
print("counterfactual recurrence mutation at n=6:")
print(f"  four-term result={summary(6)}")
print(f"  three-term result={mutated_three_term_summary(6)}")

if mismatches:
    raise SystemExit(1)
if frozen_loop_transition(2, initial_c=3) == summary(2):
    raise SystemExit("body mutation was not distinguished")
if mutated_three_term_summary(6) == summary(6):
    raise SystemExit("recurrence mutation was not distinguished")
