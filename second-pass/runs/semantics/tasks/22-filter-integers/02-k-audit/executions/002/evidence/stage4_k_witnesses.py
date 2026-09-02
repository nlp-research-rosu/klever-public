"""Concrete satisfying witnesses for all four K entry-claim input shapes."""


def filter_integers(values):
    result = []
    for value in values:
        if isinstance(value, int):
            result.append(value)
    return result


# [empty]
assert filter_integers([]) == []

# [prompt-example-one]: S=.IntSeq, F=2.5, I=5
assert filter_integers(["", 2.5, 5]) == [5]

# [prompt-example-two]: I1=1, I2=2, I3=3, S=.IntSeq
assert filter_integers([1, 2, 3, "", {}, []]) == [1, 2, 3]

# [order-and-scalars]: B=false, A=1, S=.IntSeq, C=2.
# This is the candidate claim's expected K result. CPython disagrees because
# bool is an int subclass, which the separate Python comparison records.
assert filter_integers([False, 1, None, "", 2]) == [1, 2]
