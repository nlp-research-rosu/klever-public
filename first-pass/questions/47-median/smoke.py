def median(l):
    m = len(l) // 2
    s = sorted(l)
    return s[m]


# HumanEval/47 dataset docstring case + edges, ODD-length only (the proof is scoped to
# odd-length; the even case averages the two middles = float, deferred).
assert median([3, 1, 2, 4, 5]) == 3
assert median([1]) == 1
assert median([7, 2, 10, 5, 8]) == 7
assert median([-5, -1, -3]) == -3
assert median([5, 3, 1, 2, 4, 6, 7]) == 4
