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


# HumanEval/122 test cases (the dataset `check`); returns an int.
assert add_elements([1, -2, -3, 41, 57, 76, 87, 88, 99], 3) == -4
assert add_elements([111, 121, 3, 4000, 5, 6], 2) == 0
assert add_elements([11, 21, 3, 90, 5, 6, 7, 8, 9], 4) == 125
assert add_elements([111, 21, 3, 4000, 5, 6, 7, 8, 9], 4) == 24
assert add_elements([1], 1) == 1
