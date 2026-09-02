def get_positive(l: list):
    """Return only positive numbers in the list."""
    positive = []
    x = 0
    for x in l:
        if x > 0.0:
            positive.append(x)
    return positive


assert get_positive([-1, 2, -4, 5, 6]) == [2, 5, 6]
assert get_positive([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]) == [
    5,
    3,
    2,
    3,
    9,
    123,
    1,
]
assert get_positive([-2.5, 0.0, 1.25, 7]) == [1.25, 7]
