def below_threshold(l: list, t: int):
    """Return True if all numbers in the list l are below threshold t."""
    e = 0
    for e in l:
        if e < t:
            continue
        return False
    return True


assert below_threshold([1, 2, 4, 10], 100) == True
assert below_threshold([1, 20, 4, 10], 5) == False
assert below_threshold([], 0) == True
assert below_threshold([5], 5) == False
assert below_threshold([True, False], 2) == True
assert below_threshold([1.5, -2.0], 2) == True
