def common(l1: list, l2: list):
    result = []
    item = 0
    for item in l1:
        if item in l2 and item not in result:
            result.append(item)
    return sorted(result)


assert common(
    [1, 4, 3, 34, 653, 2, 5],
    [5, 7, 1, 5, 9, 653, 121],
) == [1, 5, 653]
assert common([5, 3, 2, 8], [3, 2]) == [2, 3]
assert common([], [1, 2]) == []
assert common([2, 2, 1, 1], [1, 2, 2]) == [1, 2]
