import random

from solution import specialFilter


ODD_DIGITS = {"1", "3", "5", "7", "9"}


def oracle(nums):
    return sum(
        1
        for num in nums
        if num > 10
        and str(num)[0] in ODD_DIGITS
        and str(num)[-1] in ODD_DIGITS
    )


cases = [
    [15, -73, 14, -15],
    [33, -2, -3, 45, 21, 109],
    [],
    list(range(-500, 2001)),
    [10, 11, 12, 19, 20, 31, 99, 101, 109, 111, 24681],
    [10**100 + 1, 3 * 10**120 + 9, 8 * 10**80 + 7],
]

rng = random.Random(146)
for _ in range(1000):
    size = rng.randrange(0, 40)
    cases.append([rng.randrange(-(10**30), 10**30) for _ in range(size)])

mismatches = []
for index, nums in enumerate(cases):
    actual = specialFilter(nums)
    expected = oracle(nums)
    if actual != expected:
        mismatches.append((index, nums, actual, expected))

print(f"cases={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    raise AssertionError(mismatches[:3])
