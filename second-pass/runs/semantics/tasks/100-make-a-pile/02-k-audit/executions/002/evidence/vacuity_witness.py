#!/usr/bin/env python3
"""Ground falsity witness for spec-vacuity-audit.k."""


def pile(n: int, i: int) -> list[int]:
    return [n + 2 * index for index in range(i, n)]


n, i, vs = 3, 0, []
assert n > 0 and i >= 0 and i < n
actual = vs + pile(n, i)
mutated = vs + pile(n, i + 1)
assert actual == [3, 5, 7]
assert mutated == [5, 7]
assert actual != mutated
print(f"satisfying_input=(N={n}, I={i}, VS={vs})")
print(f"actual_result={actual}")
print(f"mutated_obligation={mutated}")
print("MUTATION_DEMONSTRABLY_FALSE")
