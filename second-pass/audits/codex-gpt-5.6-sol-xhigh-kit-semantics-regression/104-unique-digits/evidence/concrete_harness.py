def unique_digits(x):
    """Return the sorted elements of x whose decimal digits are all odd."""
    result = []
    for number in x:
        digits = str(number)
        if ("0" not in digits and "2" not in digits and
                "4" not in digits and "6" not in digits and
                "8" not in digits):
            result.append(number)
    return sorted(result)


# Reviewer-authored concrete assertions: prompt examples, empty and singleton
# boundaries, every even digit at varied decimal positions, all-odd acceptance,
# sorting, and duplicate preservation.
assert unique_digits([15, 33, 1422, 1]) == [1, 15, 33]
assert unique_digits([152, 323, 1422, 10]) == []
assert unique_digits([]) == []
assert unique_digits([1]) == [1]
assert unique_digits([2]) == []
assert unique_digits([10, 101, 110]) == []
assert unique_digits([20, 121, 112]) == []
assert unique_digits([40, 141, 114]) == []
assert unique_digits([60, 161, 116]) == []
assert unique_digits([80, 181, 118]) == []
assert unique_digits([3, 5, 7, 9, 11, 13, 15, 31, 99, 111, 97531]) == [
    3, 5, 7, 9, 11, 13, 15, 31, 99, 111, 97531
]
assert unique_digits([222, 135, 55, 15, 135, 3, 8642, 1]) == [
    1, 3, 15, 55, 135, 135
]
