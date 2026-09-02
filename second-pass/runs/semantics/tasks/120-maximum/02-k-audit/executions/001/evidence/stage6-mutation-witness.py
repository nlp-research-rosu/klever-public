#!/usr/bin/env python3

arr = [-3, -4, 5]
k = 2
ordered = sorted(arr)
true_result = ordered[len(arr) - k :]
mutated_result = ordered[1 + len(arr) - k :]

print(f"arr={arr}")
print(f"k={k}")
print(f"precondition={0 < k <= len(arr)}")
print(f"true_start={len(arr) - k}")
print(f"mutated_start={1 + len(arr) - k}")
print(f"true_result={true_result}")
print(f"mutated_result={mutated_result}")
print(f"mutation_is_false={true_result != mutated_result}")

raise SystemExit(0 if 0 < k <= len(arr) and true_result != mutated_result else 1)
