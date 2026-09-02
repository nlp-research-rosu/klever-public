def will_it_fly(q, w):
    return q == q[::-1] and sum(q) <= w


assert will_it_fly([1, 2], 5) == False
assert will_it_fly([3, 2, 3], 1) == False
assert will_it_fly([3, 2, 3], 9) == True
assert will_it_fly([3], 5) == True
assert will_it_fly([], 0) == True
assert will_it_fly([4, -10, 4], -1) == True
assert will_it_fly([1, 2, 2, 1], 6) == True
assert will_it_fly([1, 2, 2, 1], 5) == False
