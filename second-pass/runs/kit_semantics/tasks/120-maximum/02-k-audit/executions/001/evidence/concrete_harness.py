def maximum(arr, k):
    return sorted(arr)[len(arr) - k:]


assert maximum([-3, -4, 5], 3) == [-4, -3, 5]
assert maximum([4, -4, 4], 2) == [4, 4]
assert maximum([-3, 2, 1, 2, -1, -2, 1], 1) == [2]
assert maximum([7], 0) == []
assert maximum([7], 1) == [7]
arr = [i - 500 for i in range(1000)]
result = maximum(arr, 3)
assert len(result) == 3
assert result[0] == 497
assert result[1] == 498
assert result[2] == 499
