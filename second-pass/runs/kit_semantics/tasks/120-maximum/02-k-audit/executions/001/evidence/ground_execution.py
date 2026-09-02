def maximum(arr, k):
    return sorted(arr)[len(arr) - k:]


result = maximum([1, 2], 1)
assert result == [2]
