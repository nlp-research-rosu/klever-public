def median(l: list):
    """Return median of elements in the list l.
    >>> median([3, 1, 2, 4, 5])
    3
    >>> median([-10, 4, 6, 1000, 10, 20])
    15.0
    """
    ordered = sorted(l)
    size = len(ordered)
    if size % 2 == 1:
        return ordered[size // 2]
    else:
        return (ordered[size // 2 - 1] + ordered[size // 2]) / 2

assert median([3, 1, 2, 4, 5]) == 3
assert median([-10, 4, 6, 1000, 10, 20]) == 8.0
assert median([-1152921504606846976, 1152921504606846976]) == 0.0
assert median([-9007199254740993, 9007199254740993, 0]) == 0
assert median([-2]) == -2
assert median([-1]) == -1
assert median([0]) == 0
assert median([1]) == 1
assert median([2]) == 2
assert median([-2, -2]) == -2.0
assert median([-2, -1]) == -1.5
assert median([-2, 0]) == -1.0
assert median([-2, 1]) == -0.5
assert median([-2, 2]) == 0.0
assert median([-1, -2]) == -1.5
assert median([-1, -1]) == -1.0
assert median([-1, 0]) == -0.5
assert median([-1, 1]) == 0.0
assert median([-1, 2]) == 0.5
assert median([0, -2]) == -1.0
assert median([0, -1]) == -0.5
assert median([0, 0]) == 0.0
assert median([0, 1]) == 0.5
assert median([0, 2]) == 1.0
assert median([1, -2]) == -0.5
assert median([1, -1]) == 0.0
assert median([1, 0]) == 0.5
assert median([1, 1]) == 1.0
assert median([1, 2]) == 1.5
assert median([2, -2]) == 0.0
assert median([2, -1]) == 0.5
assert median([2, 0]) == 1.0
assert median([2, 1]) == 1.5
assert median([2, 2]) == 2.0
assert median([-2, -2, -2]) == -2
assert median([-2, -2, -1]) == -2
assert median([-2, -2, 0]) == -2
assert median([-2, -2, 1]) == -2
assert median([-2, -2, 2]) == -2
assert median([-2, -1, -2]) == -2
assert median([-2, -1, -1]) == -1
assert median([-2, -1, 0]) == -1
assert median([-2, -1, 1]) == -1
assert median([-2, -1, 2]) == -1
assert median([-2, 0, -2]) == -2
assert median([-2, 0, -1]) == -1
assert median([-2, 0, 0]) == 0
assert median([-2, 0, 1]) == 0
assert median([-2, 0, 2]) == 0
assert median([-2, 1, -2]) == -2
assert median([-2, 1, -1]) == -1
assert median([-2, 1, 0]) == 0
assert median([-2, 1, 1]) == 1
assert median([-2, 1, 2]) == 1
assert median([-2, 2, -2]) == -2
assert median([-2, 2, -1]) == -1
assert median([-2, 2, 0]) == 0
assert median([-2, 2, 1]) == 1
assert median([-2, 2, 2]) == 2
assert median([-1, -2, -2]) == -2
assert median([-1, -2, -1]) == -1
assert median([-1, -2, 0]) == -1
assert median([-1, -2, 1]) == -1
assert median([-1, -2, 2]) == -1
assert median([-1, -1, -2]) == -1
assert median([-1, -1, -1]) == -1
assert median([-1, -1, 0]) == -1
assert median([-1, -1, 1]) == -1
assert median([-1, -1, 2]) == -1
assert median([-1, 0, -2]) == -1
assert median([-1, 0, -1]) == -1
assert median([-1, 0, 0]) == 0
assert median([-1, 0, 1]) == 0
assert median([-1, 0, 2]) == 0
assert median([-1, 1, -2]) == -1
assert median([-1, 1, -1]) == -1
assert median([-1, 1, 0]) == 0
assert median([-1, 1, 1]) == 1
assert median([-1, 1, 2]) == 1
assert median([-1, 2, -2]) == -1
assert median([-1, 2, -1]) == -1
assert median([-1, 2, 0]) == 0
assert median([-1, 2, 1]) == 1
assert median([-1, 2, 2]) == 2
assert median([0, -2, -2]) == -2
assert median([0, -2, -1]) == -1
assert median([0, -2, 0]) == 0
assert median([0, -2, 1]) == 0
assert median([0, -2, 2]) == 0
assert median([0, -1, -2]) == -1
assert median([0, -1, -1]) == -1
assert median([0, -1, 0]) == 0
assert median([0, -1, 1]) == 0
assert median([0, -1, 2]) == 0
assert median([0, 0, -2]) == 0
assert median([0, 0, -1]) == 0
assert median([0, 0, 0]) == 0
assert median([0, 0, 1]) == 0
assert median([0, 0, 2]) == 0
assert median([0, 1, -2]) == 0
assert median([0, 1, -1]) == 0
assert median([0, 1, 0]) == 0
assert median([0, 1, 1]) == 1
assert median([0, 1, 2]) == 1
assert median([0, 2, -2]) == 0
assert median([0, 2, -1]) == 0
assert median([0, 2, 0]) == 0
assert median([0, 2, 1]) == 1
assert median([0, 2, 2]) == 2
assert median([1, -2, -2]) == -2
assert median([1, -2, -1]) == -1
assert median([1, -2, 0]) == 0
assert median([1, -2, 1]) == 1
assert median([1, -2, 2]) == 1
assert median([1, -1, -2]) == -1
assert median([1, -1, -1]) == -1
assert median([1, -1, 0]) == 0
assert median([1, -1, 1]) == 1
assert median([1, -1, 2]) == 1
assert median([1, 0, -2]) == 0
assert median([1, 0, -1]) == 0
assert median([1, 0, 0]) == 0
assert median([1, 0, 1]) == 1
assert median([1, 0, 2]) == 1
assert median([1, 1, -2]) == 1
assert median([1, 1, -1]) == 1
assert median([1, 1, 0]) == 1
assert median([1, 1, 1]) == 1
assert median([1, 1, 2]) == 1
assert median([1, 2, -2]) == 1
assert median([1, 2, -1]) == 1
assert median([1, 2, 0]) == 1
assert median([1, 2, 1]) == 1
assert median([1, 2, 2]) == 2
assert median([2, -2, -2]) == -2
assert median([2, -2, -1]) == -1
assert median([2, -2, 0]) == 0
assert median([2, -2, 1]) == 1
assert median([2, -2, 2]) == 2
assert median([2, -1, -2]) == -1
assert median([2, -1, -1]) == -1
assert median([2, -1, 0]) == 0
assert median([2, -1, 1]) == 1
assert median([2, -1, 2]) == 2
assert median([2, 0, -2]) == 0
assert median([2, 0, -1]) == 0
assert median([2, 0, 0]) == 0
assert median([2, 0, 1]) == 1
assert median([2, 0, 2]) == 2
assert median([2, 1, -2]) == 1
assert median([2, 1, -1]) == 1
assert median([2, 1, 0]) == 1
assert median([2, 1, 1]) == 1
assert median([2, 1, 2]) == 2
assert median([2, 2, -2]) == 2
assert median([2, 2, -1]) == 2
assert median([2, 2, 0]) == 2
assert median([2, 2, 1]) == 2
assert median([2, 2, 2]) == 2
assert median([-2.5]) == -2.5
assert median([-0.0]) == -0.0
assert median([0.5]) == 0.5
assert median([2.0]) == 2.0
assert median([-2.5, -2.5]) == -2.5
assert median([-2.5, -0.0]) == -1.25
assert median([-2.5, 0.5]) == -1.0
assert median([-2.5, 2.0]) == -0.25
assert median([-0.0, -2.5]) == -1.25
assert median([-0.0, -0.0]) == -0.0
assert median([-0.0, 0.5]) == 0.25
assert median([-0.0, 2.0]) == 1.0
assert median([0.5, -2.5]) == -1.0
assert median([0.5, -0.0]) == 0.25
assert median([0.5, 0.5]) == 0.5
assert median([0.5, 2.0]) == 1.25
assert median([2.0, -2.5]) == -0.25
assert median([2.0, -0.0]) == 1.0
assert median([2.0, 0.5]) == 1.25
assert median([2.0, 2.0]) == 2.0
assert median([False]) == False
assert median([True]) == True
assert median([-3]) == -3
assert median([2]) == 2
assert median([-1.5]) == -1.5
assert median([3.5]) == 3.5
assert median([False, False]) == 0.0
assert median([False, True]) == 0.5
assert median([False, -3]) == -1.5
assert median([False, 2]) == 1.0
assert median([False, -1.5]) == -0.75
assert median([False, 3.5]) == 1.75
assert median([True, False]) == 0.5
assert median([True, True]) == 1.0
assert median([True, -3]) == -1.0
assert median([True, 2]) == 1.5
assert median([True, -1.5]) == -0.25
assert median([True, 3.5]) == 2.25
assert median([-3, False]) == -1.5
assert median([-3, True]) == -1.0
assert median([-3, -3]) == -3.0
assert median([-3, 2]) == -0.5
assert median([-3, -1.5]) == -2.25
assert median([-3, 3.5]) == 0.25
assert median([2, False]) == 1.0
assert median([2, True]) == 1.5
assert median([2, -3]) == -0.5
assert median([2, 2]) == 2.0
assert median([2, -1.5]) == 0.25
assert median([2, 3.5]) == 2.75
assert median([-1.5, False]) == -0.75
assert median([-1.5, True]) == -0.25
assert median([-1.5, -3]) == -2.25
assert median([-1.5, 2]) == 0.25
assert median([-1.5, -1.5]) == -1.5
assert median([-1.5, 3.5]) == 1.0
assert median([3.5, False]) == 1.75
assert median([3.5, True]) == 2.25
assert median([3.5, -3]) == 0.25
assert median([3.5, 2]) == 2.75
assert median([3.5, -1.5]) == 1.0
assert median([3.5, 3.5]) == 3.5
