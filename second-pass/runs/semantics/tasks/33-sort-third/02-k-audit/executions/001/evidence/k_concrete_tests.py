def sort_third(l: list):
    """Sort the elements whose indices are divisible by three."""
    thirds = sorted(l[::3])
    result = []
    i = 0
    value = None
    for value in l:
        if i % 3 == 0:
            result.append(thirds[i // 3])
        else:
            result.append(value)
        i += 1
    return result


assert sort_third([]) == []
assert sort_third([7]) == [7]
assert sort_third([2, 1]) == [2, 1]
assert sort_third([1, 2, 3]) == [1, 2, 3]
assert sort_third([4, 3, 2, 1]) == [1, 3, 2, 4]
assert sort_third([5, 6, 3, 4, 8, 9, 2]) == [2, 6, 3, 4, 8, 9, 5]
assert sort_third([9, -1, 8, 6, -2, 5, 3, -3, 2, 0]) == [
    0,
    -1,
    8,
    3,
    -2,
    5,
    6,
    -3,
    2,
    9,
]
