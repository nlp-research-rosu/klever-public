def monotonic(l):
    inc = True
    dec = True
    i = 0
    prev = 0
    x = 0
    for x in l:
        if i >= 1:
            if x < prev:
                inc = False
            if x > prev:
                dec = False
        prev = x
        i = i + 1
    return inc or dec


# HumanEval/57 dataset `check` cases (bare-bool asserts) + empty-list edge.
assert monotonic([1, 2, 4, 10])
assert monotonic([1, 2, 4, 20])
assert not monotonic([1, 20, 4, 10])
assert monotonic([4, 1, 0, -10])
assert monotonic([4, 1, 1, 0])
assert not monotonic([1, 2, 3, 2, 5, 60])
assert monotonic([1, 2, 3, 4, 5, 60])
assert monotonic([9, 9, 9, 9])
assert monotonic([])
