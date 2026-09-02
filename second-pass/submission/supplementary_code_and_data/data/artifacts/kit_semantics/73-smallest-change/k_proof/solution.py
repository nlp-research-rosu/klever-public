def smallest_change(arr):
    changes = 0
    i = 0
    while i < len(arr) // 2:
        if arr[i] != arr[len(arr) - i - 1]:
            changes += 1
        i += 1
    return changes
