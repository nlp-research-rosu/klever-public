def search(lst):
    result = -1
    for value in lst:
        count = 0
        for item in lst:
            if item == value:
                count += 1
        if count >= value:
            if value > result:
                result = value
    return result


assert search([4, 1, 2, 2, 3, 1]) == 2
assert search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3
assert search([5, 5, 4, 4, 4]) == -1
assert search([1]) == 1
assert search([2]) == -1
assert search([2, 2]) == 2
assert search([3, 3]) == -1
assert search([3, 3, 3]) == 3
