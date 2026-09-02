def monotonic(l: list):
    return l == sorted(l) or l == sorted(l, reverse=True)


assert monotonic([])
assert monotonic([1])
assert monotonic([1, 1, 2])
assert monotonic([3, 2, 2])
assert not monotonic([1, 3, 2])
