def median(l: list):
    ordered = sorted(l)
    size = len(ordered)
    if size % 2 == 1:
        return ordered[size // 2]
    else:
        return (ordered[size // 2 - 1] + ordered[size // 2]) / 2


assert median([3, 1, 2, 4, 5]) == 3
assert median([-10, 4, 6, 1000, 10, 20]) == 8.0
assert median([1, 3]) == 2.0
assert median([0, True]) == 0.5
assert median([False, 2]) == 1.0
assert median([False, True]) == 0.5
assert median([1.0, 3.0]) == 2.0
assert median([1, 2.0]) == 1.5
assert median([1.5, 2]) == 1.75
assert median([False, 2.0]) == 1.0
assert median([0.5, True]) == 0.75
assert median(["c", "a", "b"]) == "b"
