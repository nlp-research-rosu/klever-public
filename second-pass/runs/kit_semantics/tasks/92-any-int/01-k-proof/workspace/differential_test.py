from itertools import product

from solution import any_int


def oracle(x, y, z):
    if not all(isinstance(value, int) for value in (x, y, z)):
        return False

    values = (x, y, z)
    for target_index in range(3):
        target = values[target_index]
        other_total = sum(
            value
            for index, value in enumerate(values)
            if index != target_index
        )
        if target == other_total:
            return True
    return False


integer_cases = list(product(range(-5, 6), repeat=3))
boolean_cases = list(product((False, True), repeat=3))

float_values = (-3.5, -2.0, -0.0, 0.5, 2.0, 3.5)
float_cases = []
for position in range(3):
    for floating in float_values:
        for left, right in product(range(-2, 3), repeat=2):
            args = [left, right]
            args.insert(position, floating)
            float_cases.append(tuple(args))

cases = integer_cases + boolean_cases + float_cases
mismatches = [
    (args, any_int(*args), oracle(*args))
    for args in cases
    if any_int(*args) != oracle(*args)
]

print(f"cases={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:10]:
        print(mismatch)
    raise SystemExit(1)
