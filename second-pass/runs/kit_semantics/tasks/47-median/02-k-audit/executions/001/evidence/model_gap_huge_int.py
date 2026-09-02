def median(l: list):
    ordered = sorted(l)
    size = len(ordered)
    if size % 2 == 1:
        return ordered[size // 2]
    else:
        return (ordered[size // 2 - 1] + ordered[size // 2]) / 2


# CPython divides the arbitrary-precision numerator before producing its
# correctly-rounded binary64 result. The supplied semantics' divII first
# converts the numerator itself to binary64.
assert median([10 ** 308, 10 ** 308]) == 1e308
