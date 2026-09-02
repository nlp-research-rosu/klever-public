def median(l: list):
    ordered = sorted(l)
    size = len(ordered)
    if size % 2 == 1:
        return ordered[size // 2]
    else:
        return (ordered[size // 2 - 1] + ordered[size // 2]) / 2


assert median([3, 1, 2, 4, 5]) == 3
assert median([-10, 4, 6, 1000, 10, 20]) == 8.0
assert median([7]) == 7
assert median([2, 1]) == 1.5
assert median([True, False]) == 0.5
assert median([1.0, 4, 2, 7]) == 3.0
assert median([1.5, 2.5]) == 2.0
assert median(["c", "a", "b"]) == "b"
assert median([9007199254740993, 9007199254740995]) == 9007199254740994.0
