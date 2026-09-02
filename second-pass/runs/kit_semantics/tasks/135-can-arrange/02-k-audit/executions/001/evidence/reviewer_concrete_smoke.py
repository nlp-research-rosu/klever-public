def can_arrange(arr):
    index = -1
    i = 0
    previous = 0
    value = 0
    for value in arr:
        if i > 0:
            if not value >= previous:
                index = i
        previous = value
        i = i + 1
    return index


assert can_arrange([1, 2, 4, 3, 5]) == 3
assert can_arrange([1, 2, 3]) == -1
assert can_arrange([]) == -1
assert can_arrange([9]) == -1
assert can_arrange([5, 4, 3]) == 2
assert can_arrange(["b", "a", "c"]) == 1
