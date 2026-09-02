def median(l: list):
    values = sorted(l)
    middle = len(values) // 2
    if len(values) % 2 == 1:
        return values[middle]
    return (values[middle] + values[middle + 1]) / 2.0


# Ground instances satisfying, respectively, MEDIAN-SPEC.median-odd and
# MEDIAN-SPEC.median-even.
assert median([3, 1, 2, 4, 5]) == 3
assert median([4, 1, 3, 2]) == 3.5
