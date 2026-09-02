def search(lst):
    answer = -1
    candidate = 1
    frequency = 0
    item = 1
    for candidate in lst:
        frequency = 0
        for item in lst:
            if item == candidate:
                frequency = frequency + 1
        if frequency >= candidate:
            if candidate > answer:
                answer = candidate + 0
    return answer


assert search([4, 1, 2, 2, 3, 1]) == 2
assert search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3
assert search([5, 5, 4, 4, 4]) == -1
assert search([1]) == 1
assert search([2]) == -1
assert search([7, 7, 7, 7, 7, 7, 7, 1]) == 7
