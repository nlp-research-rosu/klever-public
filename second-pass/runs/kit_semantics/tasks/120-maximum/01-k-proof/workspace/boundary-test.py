def maximum(arr, k):
    return sorted(arr)[len(arr) - k:]


arr = [0 for i in range(1000)]
result = maximum(arr, 1000)
assert len(arr) == 1000
assert len(result) == 1000
assert result[0] == 0
assert result[999] == 0
