def zero_key(number):
    return 0


# Python's stable reverse sort preserves source order among equal keys.
assert sorted([1, 2], key=zero_key, reverse=True) == [1, 2]
