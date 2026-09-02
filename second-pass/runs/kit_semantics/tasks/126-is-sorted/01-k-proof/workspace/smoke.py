def is_sorted(lst):
    result = lst == sorted(lst)
    previous = (-1,)
    repeated = 0
    value = 0
    for value in lst:
        if (value,) == previous:
            repeated += 1
        else:
            repeated = 1
        if repeated > 2:
            result = False
        previous = (value,)
    return result


assert is_sorted([]) == True
assert is_sorted([5]) == True
assert is_sorted([1, 2, 3, 4, 5]) == True
assert is_sorted([1, 3, 2, 4, 5]) == False
assert is_sorted([1, 2, 3, 4, 5, 6]) == True
assert is_sorted([1, 2, 3, 4, 5, 6, 7]) == True
assert is_sorted([1, 3, 2, 4, 5, 6, 7]) == False
assert is_sorted([1, 2, 2, 3, 3, 4]) == True
assert is_sorted([1, 2, 2, 2, 3, 4]) == False
