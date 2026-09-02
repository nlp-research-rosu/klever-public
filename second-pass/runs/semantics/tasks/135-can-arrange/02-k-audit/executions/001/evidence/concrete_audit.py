def can_arrange(arr):
    result = -1
    index = 0
    previous = 0
    for current in arr:
        if index > 0:
            if current < previous:
                result = index
        previous = current
        index = index + 1
    return result


# Satisfying ground instances of the entry claim's integer-sequence domain.
assert can_arrange([]) == -1
assert can_arrange([7]) == -1
assert can_arrange([1, 2]) == -1
assert can_arrange([2, 1]) == 1
assert can_arrange([1, 2, 4, 3, 5]) == 3
assert can_arrange([5, 4, 3, 2, 1]) == 4
assert can_arrange([-3, -1, -2, 0, -4]) == 4
