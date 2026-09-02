def will_it_fly(q, w):
    return q == q[::-1] and sum(q) <= w


# CPython promotes the integer sum for comparison with a float capacity.
# The supplied MPY semantics has no Int <= Float dispatch rule.
assert will_it_fly([1], 1.0) == True
