def add_elements(arr, k):
    total = 0
    i = 0
    x = 0
    for x in arr:
        if i < k:
            if x >= -9 and x <= 99:
                total = total + x
        i = i + 1
    return total
