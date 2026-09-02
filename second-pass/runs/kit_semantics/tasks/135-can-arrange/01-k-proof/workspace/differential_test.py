from itertools import permutations
import math
import random

from solution import can_arrange


def reverse_oracle(arr):
    """Find the largest qualifying index directly, scanning right-to-left."""
    for i in range(len(arr) - 1, 0, -1):
        if not arr[i] >= arr[i - 1]:
            return i
    return -1


def add_case(cases, arr):
    if all(arr != old for old in cases):
        cases.append(arr)


cases = [
    [],
    [None],
    [[1, 2]],
    [1, 2, 4, 3, 5],
    [1, 2, 3],
    [5, 4, 3],
    ["b", "a", "c"],
    [True, 2, 1.5],
    [1.0, float("nan"), 2.0],
    [float("-inf"), 0.0, float("inf")],
]

# Exhaust all distinct integer permutations through length five.
integer_pool = tuple(range(-3, 4))
for length in range(6):
    for values in permutations(integer_pool, length):
        cases.append(list(values))

rng = random.Random(135)

# Mixed numeric arrays.  Deduplicate under Python equality so these witnesses
# stay within the prompt's no-duplicate premise.
numeric_pool = [
    False,
    True,
    -10,
    -2,
    0,
    3,
    11,
    -4.5,
    -0.25,
    2.5,
    12.75,
    float("-inf"),
    float("inf"),
]
for _ in range(2000):
    rng.shuffle(numeric_pool)
    chosen = []
    for value in numeric_pool:
        if not any(value == old for old in chosen):
            chosen.append(value)
        if len(chosen) == rng.randrange(0, 9):
            break
    add_case(cases, list(chosen))

# Distinct ASCII strings, including empty strings and differing lengths.
string_pool = ["", "a", "aa", "b", "ba", "z", "A", "0"]
for _ in range(1000):
    length = rng.randrange(0, len(string_pool) + 1)
    add_case(cases, rng.sample(string_pool, length))

mismatches = []
for arr in cases:
    expected = reverse_oracle(arr)
    actual = can_arrange(arr)
    if actual != expected:
        mismatches.append((arr, expected, actual))

print(f"cases={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:10]:
        print(mismatch)
    raise SystemExit(1)
