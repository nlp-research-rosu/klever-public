def add_elements(arr, k):
    total = 0
    element = 0
    remaining = k
    for element in arr:
        if remaining == 0:
            break
        if element >= -99 and element <= 99:
            total += element
        remaining -= 1
    return total


result = add_elements([111, 21, 3, 4000, 5, 6, 7, 8, 9], 4)
