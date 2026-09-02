def next_smallest(lst):
    smallest = 0
    second = 0
    count = 0
    value = 0

    for value in lst:
        if count == 0:
            smallest = value
            count = 1
        elif value < smallest:
            second = smallest
            count = 2
            smallest = value
        elif value != smallest:
            if count == 1 or value < second:
                second = value
                count = 2

    if count == 2:
        return second
    return None


assert next_smallest([1, 2, 3, 4, 5]) == 2
assert next_smallest([5, 1, 4, 3, 2]) == 2
assert next_smallest([]) is None
assert next_smallest([1, 1]) is None
assert next_smallest([7]) is None
assert next_smallest([2, 1]) == 2
assert next_smallest([1, 2, 1]) == 2
assert next_smallest([0, -1, 0]) == 0
assert next_smallest([-1, -3, -2, -3]) == -2
assert next_smallest([3, 3, 2, 2, 1, 1]) == 2
