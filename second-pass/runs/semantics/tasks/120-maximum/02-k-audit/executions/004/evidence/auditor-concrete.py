def maximum(arr, k):
    if k == 0:
        return []
    return sorted(arr)[-k:]


assert maximum([-3, -4, 5], 3) == [-4, -3, 5]
assert maximum([4, -4, 4], 2) == [4, 4]
assert maximum([-3, 2, 1, 2, -1, -2, 1], 1) == [2]
assert maximum([1, 2, 3], 0) == []
assert maximum([-1000], 1) == [-1000]
assert maximum([-1000, 1000], 1) == [1000]
assert maximum([-1000, 1000], 2) == [-1000, 1000]
assert maximum([0, 0, 0], 3) == [0, 0, 0]
