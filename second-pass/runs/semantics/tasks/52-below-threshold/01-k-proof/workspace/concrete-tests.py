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
assert not below_threshold([5], 5)
assert below_threshold([-3, -1], 0)
