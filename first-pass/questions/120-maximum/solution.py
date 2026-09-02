def maximum(arr, k):
    n = len(arr)
    s = sorted(arr)
    res = []
    j = 0
    for j in range(0, k):
        res = res + [s[n - k + j]]
    return res
