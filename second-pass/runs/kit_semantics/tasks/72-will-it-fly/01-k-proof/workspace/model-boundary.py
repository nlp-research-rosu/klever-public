def will_it_fly(q, w):
    return q == q[::-1] and sum(q) <= w


# CPython identifies 1 and True numerically, while the supplied MPY list
# equality compares the distinct Int and Bool constructors structurally.
assert will_it_fly([1, True], 2) == True
