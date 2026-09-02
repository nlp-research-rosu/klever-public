def add_elements(arr, k):
    total = 0
    i = 0
    value = 0
    while i < k:
        value = arr[i]
        if -100 < value and value < 100:
            total = total + value
        i = i + 1
    return total
