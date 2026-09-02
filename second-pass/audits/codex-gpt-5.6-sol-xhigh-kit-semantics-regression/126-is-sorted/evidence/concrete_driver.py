def is_sorted(lst):
    previous = -1
    duplicates = 0
    value = 0

    for value in lst:
        if value < previous:
            return False

        if value == previous:
            if duplicates == 1:
                return False
            duplicates = 1
        else:
            duplicates = 0

        previous = value

    return True


assert is_sorted([]) == True
assert is_sorted([5]) == True
assert is_sorted([1, 2, 3, 4, 5]) == True
assert is_sorted([1, 3, 2, 4, 5]) == False
assert is_sorted([1, 2, 3, 4, 5, 6]) == True
assert is_sorted([1, 2, 3, 4, 5, 6, 7]) == True
assert is_sorted([1, 3, 2, 4, 5, 6, 7]) == False
assert is_sorted([1, 2, 2, 3, 3, 4]) == True
assert is_sorted([1, 2, 2, 2, 3, 4]) == False
assert is_sorted([0]) == True
assert is_sorted([0, 0]) == True
assert is_sorted([0, 0, 0]) == False
assert is_sorted([1, 0]) == False
assert is_sorted([0, 1]) == True
