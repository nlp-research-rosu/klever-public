from itertools import product
from random import Random

from solution import max_fill


def extraction_oracle(grid, capacity):
    dips = 0
    for row in grid:
        water = 0
        for cell in row:
            if cell == 1:
                water += 1
        while water > 0:
            water -= capacity
            dips += 1
    return dips


def check(grid, capacity):
    actual = max_fill(grid, capacity)
    expected = extraction_oracle(grid, capacity)
    if actual != expected:
        raise AssertionError((grid, capacity, actual, expected))


cases = 0

# Exhaust every binary grid through 3x4, including the proof's empty/ragged
# boundary shapes, for capacities 1 through 4.
check([], 1)
cases += 1
for height in range(1, 4):
    for width in range(0, 5):
        for flat in product((0, 1), repeat=height * width):
            grid = [
                list(flat[row * width:(row + 1) * width])
                for row in range(height)
            ]
            for capacity in range(1, 5):
                check(grid, capacity)
                cases += 1

# Prompt-boundary cases and a seeded broader sample over the stated domain.
for grid, capacity in (
    ([[0] * 100 for _ in range(100)], 10),
    ([[1] * 100 for _ in range(100)], 1),
    ([[1] * 100 for _ in range(100)], 10),
):
    check(grid, capacity)
    cases += 1

rng = Random(20260729)
for _ in range(250):
    height = rng.randint(1, 100)
    width = rng.randint(1, 100)
    grid = [
        [rng.randint(0, 1) for _ in range(width)]
        for _ in range(height)
    ]
    capacity = rng.randint(1, 10)
    check(grid, capacity)
    cases += 1

print(f"cases={cases} mismatches=0")
