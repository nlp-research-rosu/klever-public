def maximum(arr, k):
    if k == 0:
        return []
    return sorted(arr)[-k:]


assert maximum([-3, -4, 5], 3) == [-4, -3, 5]
assert maximum([4, -4, 4], 2) == [4, 4]
assert maximum([-3, 2, 1, 2, -1, -2, 1], 1) == [2]
assert maximum([1, 2, 3], 0) == []
