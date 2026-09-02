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
assert is_sorted([0]) == True
assert is_sorted([0, 1, 1]) == True
assert is_sorted([0, 0, 0]) == False
assert is_sorted([2, 1]) == False
assert is_sorted([0, 1, 1, 2, 2]) == True
