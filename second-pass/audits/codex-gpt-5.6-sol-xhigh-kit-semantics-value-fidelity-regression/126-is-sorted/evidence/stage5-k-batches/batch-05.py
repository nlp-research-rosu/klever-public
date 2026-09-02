def is_sorted(lst):
    result = lst == sorted(lst)
    current = 0
    for current in lst:
        if lst.count(current) > 2:
            result = False
    return result

assert is_sorted([1, 0, 1, 0]) == False
assert is_sorted([1, 0, 1, 1]) == False
assert is_sorted([1, 0, 1, 2]) == False
assert is_sorted([1, 0, 1, 3]) == False
assert is_sorted([1, 0, 2, 0]) == False
assert is_sorted([1, 0, 2, 1]) == False
assert is_sorted([1, 0, 2, 2]) == False
assert is_sorted([1, 0, 2, 3]) == False
assert is_sorted([1, 0, 3, 0]) == False
assert is_sorted([1, 0, 3, 1]) == False
assert is_sorted([1, 0, 3, 2]) == False
assert is_sorted([1, 0, 3, 3]) == False
assert is_sorted([1, 1, 0, 0]) == False
assert is_sorted([1, 1, 0, 1]) == False
assert is_sorted([1, 1, 0, 2]) == False
assert is_sorted([1, 1, 0, 3]) == False
assert is_sorted([1, 1, 1, 0]) == False
assert is_sorted([1, 1, 1, 1]) == False
assert is_sorted([1, 1, 1, 2]) == False
assert is_sorted([1, 1, 1, 3]) == False
assert is_sorted([1, 1, 2, 0]) == False
assert is_sorted([1, 1, 2, 1]) == False
assert is_sorted([1, 1, 2, 2]) == True
assert is_sorted([1, 1, 2, 3]) == True
assert is_sorted([1, 1, 3, 0]) == False
assert is_sorted([1, 1, 3, 1]) == False
assert is_sorted([1, 1, 3, 2]) == False
assert is_sorted([1, 1, 3, 3]) == True
assert is_sorted([1, 2, 0, 0]) == False
assert is_sorted([1, 2, 0, 1]) == False
assert is_sorted([1, 2, 0, 2]) == False
assert is_sorted([1, 2, 0, 3]) == False
assert is_sorted([1, 2, 1, 0]) == False
assert is_sorted([1, 2, 1, 1]) == False
assert is_sorted([1, 2, 1, 2]) == False
assert is_sorted([1, 2, 1, 3]) == False
assert is_sorted([1, 2, 2, 0]) == False
assert is_sorted([1, 2, 2, 1]) == False
assert is_sorted([1, 2, 2, 2]) == False
assert is_sorted([1, 2, 2, 3]) == True
