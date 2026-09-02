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


# Smoke checks — the HumanEval/0 dataset `check` cases.
assert has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True
assert has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) == False
assert has_close_elements([1.0, 2.0, 5.9, 4.0, 5.0], 0.95) == True
assert has_close_elements([1.0, 2.0, 5.9, 4.0, 5.0], 0.8) == False
