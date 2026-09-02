def maximum(arr, k):
    return sorted(arr)[len(arr) - k:]


assert maximum([-3, -4, 5], 3) == [-4, -3, 5]
assert maximum([4, -4, 4], 2) == [4, 4]
assert maximum([-3, 2, 1, 2, -1, -2, 1], 1) == [2]
assert maximum([7], 0) == []
assert maximum([7], 1) == [7]
assert maximum([-1000, 0, 1000, -1000, 1000], 4) == [-1000, 0, 1000, 1000]
