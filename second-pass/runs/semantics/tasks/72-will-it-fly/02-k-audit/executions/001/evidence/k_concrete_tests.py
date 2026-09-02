def will_it_fly(q, w):
    return q == q[::-1] and sum(q) <= w


# One satisfying witness for each symbolic entry claim.
assert will_it_fly([3, 2, 3], 9) == True
assert will_it_fly([1, 2], 5) == False
assert will_it_fly([3, 2, 3], 1) == False

# Empty, exact-threshold, even-palindrome, and negative-sum boundaries.
assert will_it_fly([], -1) == False
assert will_it_fly([], 0) == True
assert will_it_fly([1, 2, 2, 1], 6) == True
assert will_it_fly([1, 2, 2, 1], 5) == False
assert will_it_fly([4, -10, 4], -2) == True
