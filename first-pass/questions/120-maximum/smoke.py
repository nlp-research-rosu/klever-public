def maximum(arr, k):
    n = len(arr)
    s = sorted(arr)
    res = []
    j = 0
    for j in range(0, k):
        res = res + [s[n - k + j]]
    return res


assert maximum([-3, -4, 5], 3) == [-4, -3, 5]
assert maximum([4, -4, 4], 2) == [4, 4]
assert maximum([-3, 2, 1, 2, -1, -2, 1], 1) == [2]
assert maximum([1, 2, 3], 0) == []
