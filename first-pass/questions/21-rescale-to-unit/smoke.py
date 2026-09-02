def rescale_to_unit(numbers):
    min_number = min(numbers)
    max_number = max(numbers)
    return [(x - min_number) / (max_number - min_number) for x in numbers]


# Smoke checks — the HumanEval/21 dataset `check` cases (bare-value asserts).
assert rescale_to_unit([2.0, 49.9]) == [0.0, 1.0]
assert rescale_to_unit([100.0, 49.9]) == [1.0, 0.0]
assert rescale_to_unit([1.0, 2.0, 3.0, 4.0, 5.0]) == [0.0, 0.25, 0.5, 0.75, 1.0]
