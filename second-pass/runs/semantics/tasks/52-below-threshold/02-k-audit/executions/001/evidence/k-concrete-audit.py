def below_threshold(l: list, t: int):
    """Return True if all numbers in the list l are below threshold t.
    >>> below_threshold([1, 2, 4, 10], 100)
    True
    >>> below_threshold([1, 20, 4, 10], 5)
    False
    """
    for number in l:
        if number >= t:
            return False
    return True


assert below_threshold([1, 2, 4, 10], 100)
assert not below_threshold([1, 20, 4, 10], 5)
assert below_threshold([], 0)
assert below_threshold([-1], 0)
assert not below_threshold([0], 0)
assert not below_threshold([1], 0)
assert below_threshold([-3, -2, -1], 0)
assert not below_threshold([0, -1, -2], 0)
assert not below_threshold([-1, 0, -2], 0)
assert not below_threshold([-1, -2, 0], 0)
assert below_threshold([999999999999999999999], 1000000000000000000000)
assert not below_threshold([1000000000000000000000], 1000000000000000000000)
