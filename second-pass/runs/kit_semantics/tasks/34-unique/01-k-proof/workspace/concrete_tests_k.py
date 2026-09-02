def unique(l: list):
    """Return sorted unique elements in a list."""
    result = []
    x = None
    for x in l:
        if x not in result:
            result.append(x)
    return sorted(result)


assert unique([]) == []
assert unique([5, 3, 5, 2, 3, 3, 9, 0, 123]) == [0, 2, 3, 5, 9, 123]
assert unique(["b", "a", "b", "c", "a"]) == ["a", "b", "c"]
assert unique([True, 1]) == [True]
assert unique([True, 1, 0, False, 2]) == [0, True, 2]
assert unique([3.0, 2, 2.0, 3]) == [2, 3.0]
assert unique([-4, 7, -4, 0, 7, -1]) == [-4, -1, 0, 7]
