def will_it_fly(q, w):
    return q == q[::-1] and sum(q) <= w


# Prompt examples.
assert will_it_fly([1, 2], 5) == False
assert will_it_fly([3, 2, 3], 1) == False
assert will_it_fly([3, 2, 3], 9) == True
assert will_it_fly([3], 5) == True

# Empty, sum threshold, palindrome boundary, and negative values.
assert will_it_fly([], -1) == False
assert will_it_fly([], 0) == True
assert will_it_fly([1, 1], 1) == False
assert will_it_fly([1, 1], 2) == True
assert will_it_fly([1, 2], 3) == False
assert will_it_fly([-4, 1, -4], -7) == True
assert will_it_fly([-4, 1, -4], -8) == False

# The supplied model's homogeneous-float branch and unbalanced short circuit.
assert will_it_fly([1.5], 2.0) == True
assert will_it_fly([1.0, 2.0], 5) == False
