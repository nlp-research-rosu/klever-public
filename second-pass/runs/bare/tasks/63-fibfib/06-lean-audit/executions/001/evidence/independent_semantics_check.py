#!/usr/bin/env python3
"""Independent executable checks for the frozen fibfib transition system."""


def frozen_program(n: int) -> tuple[int, int, int, int]:
    a, b, c, i = 0, 0, 1, 0
    while i < n:
        a, b, c = b, c, a + b + c
        i = i + 1
    return a, b, c, i


def fibfib_math(n: int) -> int:
    if n <= 1:
        return 0
    if n == 2:
        return 1
    values = [0, 0, 1]
    for index in range(3, n + 1):
        values.append(
            values[index - 1]
            + values[index - 2]
            + values[index - 3]
        )
    return values[n]


def mutation_wrong_initial_c(n: int) -> int:
    a, b, c, i = 0, 0, 0, 0
    while i < n:
        a, b, c = b, c, a + b + c
        i += 1
    return a


def mutation_sequential_tuple(n: int) -> int:
    a, b, c, i = 0, 0, 1, 0
    while i < n:
        a = b
        b = c
        c = a + b + c
        i += 1
    return a


print("n | operational (a,b,c,i) | summary triple")
for n in range(16):
    operational = frozen_program(n)
    summary = (
        fibfib_math(n),
        fibfib_math(n + 1),
        fibfib_math(n + 2),
        n,
    )
    print(f"{n:2d} | {operational!s:24s} | {summary}")
    assert operational == summary

print("\nOne-step invariant checks:")
for i in range(12):
    before = (
        fibfib_math(i),
        fibfib_math(i + 1),
        fibfib_math(i + 2),
    )
    after = (before[1], before[2], sum(before))
    expected = (
        fibfib_math(i + 1),
        fibfib_math(i + 2),
        fibfib_math(i + 3),
    )
    print(f"i={i:2d}: {before} -> {after} == {expected}")
    assert after == expected

print("\nCounterfactual body sensitivity:")
for n in range(16):
    expected = fibfib_math(n)
    wrong_c = mutation_wrong_initial_c(n)
    sequential = mutation_sequential_tuple(n)
    if wrong_c != expected or sequential != expected:
        print(
            f"n={n:2d}: expected={expected}, "
            f"wrong_initial_c={wrong_c}, sequential_tuple={sequential}"
        )

assert mutation_wrong_initial_c(2) != fibfib_math(2)
assert mutation_sequential_tuple(3) != fibfib_math(3)
print("\nRESULT: exact transition agrees on all checks; mutations are detected.")
