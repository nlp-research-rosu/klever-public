def max_element(l: list):
    return max(l)


# CPython and the trusted canonical function return [2]. The supplied K model
# represents nested list values but has no list/list ordering rule for max.
assert max_element([[1, 9], [2], [1, 10]]) == [2]
