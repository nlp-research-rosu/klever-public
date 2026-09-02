def max_element(l):
    m = l[0]
    for e in l:
        if e > m:
            m = e
    return m


# HumanEval/35 test cases (the dataset `check`); max_element returns an int.
assert max_element([1, 2, 3]) == 3
assert max_element([5, 3, -5, 2, -3, 3, 9, 0, 124, 1, -10]) == 124

# Extra edge cases for krun coverage (the dataset ships only the two above).
assert max_element([7]) == 7                 # single element
assert max_element([-5, -1, -3]) == -1       # all negative
assert max_element([3, 3, 3]) == 3           # all equal (ties)
assert max_element([5, 2, 5, 1]) == 5        # tie for the max, keep the earlier
assert max_element([1, 2, 3, 100]) == 100    # max at the end
assert max_element([100, 1, 2, 3]) == 100    # max at the start
assert max_element([-2, 0, -5]) == 0         # spans zero
