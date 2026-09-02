#!/usr/bin/env python3
"""Independent finite witnesses for the Stage 3 summary classifications.

This does not import or execute the frozen solution.  It separately models the
source branches and the proof-local summary equations read from verification.k.
"""


def py_mod(left: int, right: int) -> int:
    return ((left % right) + right) % right


def operational_value(index: int) -> int:
    if index == 0:
        return 1
    if index == 1:
        return 3
    if py_mod(index, 2) == 0:
        return 1 + (index - py_mod(index, 2)) // 2
    half = (index - py_mod(index, 2)) // 2
    return (half + 1) * (half + 3)


def tri_value(index: int) -> int:
    if index < 0:
        return 0
    half = (index - py_mod(index, 2)) // 2
    if py_mod(index, 2) == 1:
        return (half + 1) * (half + 3)
    return 1 + half


def tri_complete(prefix: list[int], index: int, bound: int) -> list[int]:
    result = list(prefix)
    while index <= bound:
        result.append(tri_value(index))
        index += 1
    return result


def operational_result(bound: int) -> list[int]:
    values: list[int] = []
    index = 0
    while index <= bound:
        values.append(operational_value(index))
        index += 1
    return values


indices = list(range(0, 1001))
value_mismatches = [
    (index, operational_value(index), tri_value(index))
    for index in indices
    if operational_value(index) != tri_value(index)
]
bounds = [-1, 0, 1, 2, 3, 4, 5, 20, 100]
result_mismatches = [
    (bound, operational_result(bound), tri_complete([], 0, bound))
    for bound in bounds
    if operational_result(bound) != tri_complete([], 0, bound)
]

mutated_odd_mismatches = [
    index
    for index in range(1, 20, 2)
    if operational_value(index)
    != ((index - py_mod(index, 2)) // 2 + 1)
    * ((index - py_mod(index, 2)) // 2 + 2)
]
mutated_even_mismatches = [
    index
    for index in range(0, 20, 2)
    if operational_value(index) != 2 + (index - py_mod(index, 2)) // 2
]

print("tested_indices:", f"{indices[0]}..{indices[-1]}")
print("value_mismatch_count:", len(value_mismatches))
print("value_mismatches:", value_mismatches)
print("tested_bounds:", bounds)
print("result_mismatch_count:", len(result_mismatches))
print("result_mismatches:", result_mismatches)
print("mutated_odd_detected_at:", mutated_odd_mismatches)
print("mutated_even_detected_at:", mutated_even_mismatches)

assert not value_mismatches
assert not result_mismatches
assert mutated_odd_mismatches
assert mutated_even_mismatches
