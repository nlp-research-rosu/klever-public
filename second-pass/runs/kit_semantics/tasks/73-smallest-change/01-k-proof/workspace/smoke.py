def smallest_change(arr):
    changes = 0
    i = 0
    while i < len(arr) // 2:
        if arr[i] != arr[len(arr) - i - 1]:
            changes += 1
        i += 1
    return changes


assert smallest_change([1, 2, 3, 5, 4, 7, 9, 6]) == 4
assert smallest_change([1, 2, 3, 4, 3, 2, 2]) == 1
assert smallest_change([1, 2, 3, 2, 1]) == 0
assert smallest_change([]) == 0
assert smallest_change([9]) == 0
assert smallest_change([1, 2]) == 1
