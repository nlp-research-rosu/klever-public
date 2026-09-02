def will_it_fly(q, w):
    total = 0
    rev = []
    x = 0
    for x in q:
        total = total + x
        rev = [x] + rev
    return total <= w and q == rev


# HumanEval/72 test cases (the dataset `check`); returns a bool (bare-bool asserts).
assert will_it_fly([3, 2, 3], 9)
assert not will_it_fly([1, 2], 5)
assert will_it_fly([3], 5)
assert not will_it_fly([3, 2, 3], 1)
assert not will_it_fly([1, 2, 3], 6)
assert will_it_fly([5], 5)
