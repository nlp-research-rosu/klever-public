def is_sorted(lst):
    prev = -1
    duplicates = 0
    result = True
    for value in lst:
        if isinstance(value, int):
            if value < prev:
                result = False
            if value == prev:
                duplicates += 1
            else:
                duplicates = 0
            if duplicates > 1:
                result = False
            prev = value
        else:
            return False
    return result


assert is_sorted([]) == True
assert is_sorted([0]) == True
assert is_sorted([0, 0]) == True
assert is_sorted([0, 0, 0]) == False
assert is_sorted([0, 1, 2]) == True
assert is_sorted([1, 0]) == False
assert is_sorted([0, 1, 0]) == False
assert is_sorted([0, 0, 1, 1]) == True
assert is_sorted([0, 0, 1, 1, 1]) == False
assert is_sorted([9223372036854775807]) == True
