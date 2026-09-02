def _smallest_change(arr, left, right):
    if left >= right:
        return 0
    if arr[left] != arr[right]:
        return 1 + _smallest_change(arr, left + 1, right - 1)
    return _smallest_change(arr, left + 1, right - 1)


def smallest_change(arr):
    return _smallest_change(arr, 0, len(arr) - 1)


assert smallest_change([]) == 0
assert smallest_change([7]) == 0
assert smallest_change([1, 2]) == 1
assert smallest_change([1, 2, 3, 5, 4, 7, 9, 6]) == 4
assert smallest_change([1, 2, 3, 4, 3, 2, 2]) == 1
assert smallest_change([1, 2, 3, 2, 1]) == 0
