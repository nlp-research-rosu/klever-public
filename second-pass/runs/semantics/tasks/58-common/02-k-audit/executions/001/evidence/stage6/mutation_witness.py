#!/usr/bin/env python3
"""Show why returning heap object 0 is observably false for a ground input."""

first = [2, 2, 1, 1]
second = [1, 2, 2]
heap_0_accumulator = [2, 1]
heap_1_sorted_return = [1, 2]

print(f"FIRST={first}")
print(f"SECOND={second}")
print(f"mutated ref(0) denotes accumulator={heap_0_accumulator}")
print(f"actual ref(1) denotes sorted return={heap_1_sorted_return}")
print(f"observable_values_differ={heap_0_accumulator != heap_1_sorted_return}")

assert heap_0_accumulator != heap_1_sorted_return
