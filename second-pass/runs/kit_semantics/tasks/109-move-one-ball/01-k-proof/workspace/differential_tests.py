import itertools

from solution import move_one_ball


def rotation_oracle(arr):
    if not arr:
        return True
    target = sorted(arr)
    for shifts in range(len(arr)):
        candidate = arr[-shifts:] + arr[:-shifts]
        if candidate == target:
            return True
    return False


prompt_cases = [
    ([3, 4, 5, 1, 2], True),
    ([3, 5, 4, 1, 2], False),
    ([], True),
    ([7], True),
    ([2, 1, 3], False),
]

for values, expected in prompt_cases:
    assert move_one_ball(values) == expected
    assert rotation_oracle(values) == expected

unique_cases = 0
for size in range(8):
    for values in itertools.permutations(range(size)):
        values = list(values)
        assert move_one_ball(values) == rotation_oracle(values)
        unique_cases += 1

duplicate_cases = 0
for size in range(7):
    for values in itertools.product((-1, 0, 1), repeat=size):
        values = list(values)
        assert move_one_ball(values) == rotation_oracle(values)
        duplicate_cases += 1

print(
    f"prompt_cases={len(prompt_cases)} "
    f"unique_cases={unique_cases} "
    f"duplicate_cases={duplicate_cases} "
    "mismatches=0"
)
