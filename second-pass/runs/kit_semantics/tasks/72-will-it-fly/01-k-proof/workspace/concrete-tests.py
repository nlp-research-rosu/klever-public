def will_it_fly(q, w):
    return q == q[::-1] and sum(q) <= w


assert will_it_fly([1, 2], 5) == False
assert will_it_fly([3, 2, 3], 1) == False
assert will_it_fly([3, 2, 3], 9) == True
assert will_it_fly([3], 5) == True
assert will_it_fly([], 0) == True
assert will_it_fly([-2, 7, -2], 3) == True
assert will_it_fly([True, False, True], 2) == True
assert will_it_fly([1.5, 2.0, 1.5], 5.0) == True
assert will_it_fly([1.5, 2.0], 10.0) == False
