#!/usr/bin/env python3
"""Demonstrate falsity of the fresh off-by-one postcondition."""

arr = [-3, 5]
k = 1
actual = sorted(arr)[len(arr) - k :]
mutated = sorted(arr)[len(arr) - k + 1 :]

print(f"arr={arr}")
print(f"k={k}")
print(f"precondition={0 < k <= len(arr)}")
print(f"actual_result={actual}")
print(f"mutated_required_result={mutated}")
print(f"mutation_is_false={actual != mutated}")
assert 0 < k <= len(arr)
assert actual == [5]
assert mutated == []
assert actual != mutated
