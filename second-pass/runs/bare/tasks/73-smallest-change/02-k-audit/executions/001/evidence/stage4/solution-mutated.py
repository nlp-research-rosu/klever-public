def smallest_change(arr):
    if len(arr) <= 1:
        return 99
    if arr[0] == arr[-1]:
        return smallest_change(arr[1:-1])
    return 1 + smallest_change(arr[1:-1])
