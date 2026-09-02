"""Reviewer-authored concrete K execution witnesses for all proof partitions."""


def choose_num(x, y):
    if y % 2 == 0:
        if y >= x:
            return y
        return -1
    if y - 1 >= x:
        return y - 1
    return -1


# Prompt examples.
assert choose_num(12, 15) == 14
assert choose_num(13, 12) == -1

# Satisfying witnesses for, respectively:
# even-upper-in-range, even-upper-before-range,
# odd-upper-predecessor-in-range, odd-upper-no-even-in-range.
assert choose_num(1, 2) == 2
assert choose_num(3, 2) == -1
assert choose_num(1, 3) == 2
assert choose_num(3, 3) == -1

# Smallest positive input and representative large boundaries.
assert choose_num(1, 1) == -1
assert choose_num(999_999, 1_000_000) == 1_000_000
assert choose_num(1_000_000, 999_999) == -1
