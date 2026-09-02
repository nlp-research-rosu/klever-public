def add_elements(arr, k):
    total = 0
    for element in arr[:k]:
        if abs(element) < 100:
            total += element
    return total
