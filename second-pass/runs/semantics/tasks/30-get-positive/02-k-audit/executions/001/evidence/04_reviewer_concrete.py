"""Reviewer-authored concrete harness for the submitted implementation."""


def get_positive(l: list):
    result = []
    for x in l:
        if x > 0:
            result.append(x)
    return result


assert get_positive([-1, 2, -4, 5, 6]) == [2, 5, 6]
assert get_positive([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]) == [
    5, 3, 2, 3, 9, 123, 1
]
assert get_positive([]) == []
assert get_positive([-1, 0, 1]) == [1]
assert get_positive([3, 0, -2, 3, 1]) == [3, 3, 1]

