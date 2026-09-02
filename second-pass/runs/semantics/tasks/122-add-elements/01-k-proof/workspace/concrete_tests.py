def add_elements(arr, k):
    total = 0
    for element in arr[:k]:
        if abs(element) < 100:
            total += element
    return total


assert add_elements([111, 21, 3, 4000, 5, 6, 7, 8, 9], 4) == 24
assert add_elements([1, -2, -100, 99, 100], 5) == 98
assert add_elements([0], 1) == 0
assert add_elements([-99, 999, 10], 2) == -99
