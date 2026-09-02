def is_sorted(lst):
    result = True
    previous = 0
    repeats = 0
    for number in lst:
        if number < previous:
            result = False
        if number == previous:
            repeats += 1
        else:
            repeats = 1
        if repeats > 2:
            result = False
        previous = number
    return result


assert is_sorted([])
assert is_sorted([5])
assert is_sorted([1, 2, 3, 4, 5])
assert not is_sorted([1, 3, 2, 4, 5])
assert is_sorted([1, 2, 2, 3, 3, 4])
assert not is_sorted([1, 2, 2, 2, 3, 4])
assert is_sorted([0, 0])
assert not is_sorted([0, 0, 0])
