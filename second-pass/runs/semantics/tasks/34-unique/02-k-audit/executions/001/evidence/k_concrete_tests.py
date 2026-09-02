def unique(l: list):
    result = []
    for item in l:
        if item not in result:
            result.append(item)
    return sorted(result)


assert unique([]) == []
assert unique([7]) == [7]
assert unique([4, 4, 4]) == [4]
assert unique([2, 1]) == [1, 2]
assert unique([-1, 3, -1, 2, 3]) == [-1, 2, 3]
assert unique([5, 3, 5, 2, 3, 3, 9, 0, 123]) == [0, 2, 3, 5, 9, 123]
