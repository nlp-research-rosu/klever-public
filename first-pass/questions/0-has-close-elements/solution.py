def has_close_elements(numbers, threshold):
    found = False
    n = len(numbers)
    idx = 0
    idx2 = 0
    for idx in range(0, n):
        for idx2 in range(idx + 1, n):
            if abs(numbers[idx] - numbers[idx2]) < threshold:
                found = True
    return found
