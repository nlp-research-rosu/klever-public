def median(l: list):
    values = sorted(l)
    middle = len(values) // 2
    if len(values) % 2 == 1:
        return values[middle]
    return (values[middle] + values[middle + 1]) / 2.0


# The trusted canonical result for this satisfying even-claim input is 2.5.
# The submitted program must fail this assertion.
assert median([4, 1, 3, 2]) == 2.5
