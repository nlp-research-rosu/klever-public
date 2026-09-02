def is_sorted(lst):
    previous = -1
    repeated = 0
    for number in lst:
        if number < previous:
            return False
        if number == previous:
            repeated += 1
            if repeated > 1:
                return False
        else:
            repeated = 0
        previous = number
    return True


assert is_sorted([]) == True
assert is_sorted([0]) == True
assert is_sorted([0, 0]) == True
assert is_sorted([0, 0, 0]) == False
assert is_sorted([1, 2, 2, 3, 3, 4]) == True
assert is_sorted([1, 2, 2, 2, 3, 4]) == False
assert is_sorted([1, 3, 2, 4, 5]) == False
assert is_sorted([1, 1, 2, 2, 3, 3, 4, 4]) == True
assert is_sorted([1, 1, 2, 2, 3, 3, 4, 4, 4]) == False
