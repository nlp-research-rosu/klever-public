def monotonic(l: list):
    """Return whether l is monotonically nondecreasing or nonincreasing."""
    return l == sorted(l) or l == sorted(l, reverse=True)


assert monotonic([1, 2, 4, 20])
assert not monotonic([1, 20, 4, 10])
assert monotonic([4, 1, 0, -10])
assert monotonic([])
assert monotonic([3])
assert monotonic([1, 1, 2, 2])
assert monotonic([2, 2, 1, 1])
assert not monotonic([1, 2, 1])
