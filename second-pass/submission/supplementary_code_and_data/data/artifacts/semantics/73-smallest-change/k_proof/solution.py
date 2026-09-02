def _smallest_change(arr, left, right):
    if left >= right:
        return 0
    if arr[left] != arr[right]:
        return 1 + _smallest_change(arr, left + 1, right - 1)
    return _smallest_change(arr, left + 1, right - 1)


def smallest_change(arr):
    return _smallest_change(arr, 0, len(arr) - 1)
