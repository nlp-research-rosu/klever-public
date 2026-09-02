import random

from solution import do_algebra


def oracle(operators, operands):
    expression = str(operands[0])
    for operator, operand in zip(operators, operands[1:]):
        expression += operator + str(operand)
    return eval(expression)


rng = random.Random(160)
operators = ["+", "-", "*", "//", "**"]
tested = 0
skipped_zero_division = 0

while tested < 500:
    count = rng.randint(1, 3)
    ops = [rng.choice(operators) for _ in range(count)]
    nums = [rng.randint(0, 4) for _ in range(count + 1)]
    try:
        expected = oracle(ops, nums)
        actual = do_algebra(ops, nums)
    except ZeroDivisionError:
        skipped_zero_division += 1
        continue
    assert actual == expected, (ops, nums, expected, actual)
    tested += 1

print(
    f"tested={tested} "
    f"skipped_zero_division={skipped_zero_division} "
    "mismatches=0"
)
