def incr_list(l: list):
    """Return list with elements incremented by 1."""
    result = []
    for x in l:
        result.append(x + 1)
    return result


assert incr_list([1, 2, 3]) == [2, 3, 4]
assert incr_list([5, 3, 5, 2, 3, 3, 9, 0, 123]) == [
    6, 4, 6, 3, 4, 4, 10, 1, 124
]
assert incr_list([]) == []
assert incr_list([-2, -1, 0, 1]) == [-1, 0, 1, 2]
assert incr_list([1, -2, 0]) == [2, -1, 1]
