def is_sorted(lst):
    result = lst == sorted(lst)
    current = 0
    for current in lst:
        if lst.count(current) > 2:
            result = False
    return result

assert is_sorted([1, 2, 3, 0]) == False
assert is_sorted([1, 2, 3, 1]) == False
assert is_sorted([1, 2, 3, 2]) == False
assert is_sorted([1, 2, 3, 3]) == True
assert is_sorted([1, 3, 0, 0]) == False
assert is_sorted([1, 3, 0, 1]) == False
assert is_sorted([1, 3, 0, 2]) == False
assert is_sorted([1, 3, 0, 3]) == False
assert is_sorted([1, 3, 1, 0]) == False
assert is_sorted([1, 3, 1, 1]) == False
assert is_sorted([1, 3, 1, 2]) == False
assert is_sorted([1, 3, 1, 3]) == False
assert is_sorted([1, 3, 2, 0]) == False
assert is_sorted([1, 3, 2, 1]) == False
assert is_sorted([1, 3, 2, 2]) == False
assert is_sorted([1, 3, 2, 3]) == False
assert is_sorted([1, 3, 3, 0]) == False
assert is_sorted([1, 3, 3, 1]) == False
assert is_sorted([1, 3, 3, 2]) == False
assert is_sorted([1, 3, 3, 3]) == False
assert is_sorted([2, 0, 0, 0]) == False
assert is_sorted([2, 0, 0, 1]) == False
assert is_sorted([2, 0, 0, 2]) == False
assert is_sorted([2, 0, 0, 3]) == False
assert is_sorted([2, 0, 1, 0]) == False
assert is_sorted([2, 0, 1, 1]) == False
assert is_sorted([2, 0, 1, 2]) == False
assert is_sorted([2, 0, 1, 3]) == False
assert is_sorted([2, 0, 2, 0]) == False
assert is_sorted([2, 0, 2, 1]) == False
assert is_sorted([2, 0, 2, 2]) == False
assert is_sorted([2, 0, 2, 3]) == False
assert is_sorted([2, 0, 3, 0]) == False
assert is_sorted([2, 0, 3, 1]) == False
assert is_sorted([2, 0, 3, 2]) == False
assert is_sorted([2, 0, 3, 3]) == False
assert is_sorted([2, 1, 0, 0]) == False
assert is_sorted([2, 1, 0, 1]) == False
assert is_sorted([2, 1, 0, 2]) == False
assert is_sorted([2, 1, 0, 3]) == False
