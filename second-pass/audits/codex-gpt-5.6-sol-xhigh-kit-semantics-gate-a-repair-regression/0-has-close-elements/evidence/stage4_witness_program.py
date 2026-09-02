def has_close_elements(numbers, threshold):
    i = 0
    j = 0
    n = len(numbers)
    while i < n:
        j = i + 1
        while j < n:
            if abs(numbers[i] - numbers[j]) < threshold:
                return True
            j += 1
        i += 1
    return False


assert abs(1.0 - 1.25) < 0.5
assert has_close_elements([1.0, 1.25], 0.5) == True
