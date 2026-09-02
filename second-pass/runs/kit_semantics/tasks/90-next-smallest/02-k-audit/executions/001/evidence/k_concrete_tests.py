def next_smallest(lst):
    """
    Return the second-smallest distinct integer in lst, or None when it
    does not exist.
    """
    found_smallest = False
    found_second = False
    smallest = 0
    second = 0
    x = 0

    for x in lst:
        x = x + 0

        if not found_smallest:
            smallest = x
            found_smallest = True
        elif x < smallest:
            second = smallest
            found_second = True
            smallest = x
        elif x != smallest and (not found_second or x < second):
            second = x
            found_second = True

    if found_second:
        return second
    return None


# Docstring examples.
assert next_smallest([1, 2, 3, 4, 5]) == 2
assert next_smallest([5, 1, 4, 3, 2]) == 2
assert next_smallest([]) is None
assert next_smallest([1, 1]) is None

# Each source branch and representative integer boundaries.
assert next_smallest([2, 1]) == 2
assert next_smallest([1, 3, 2]) == 2
assert next_smallest([3, 1, 2]) == 2
assert next_smallest([2, 1, 1, 2]) == 2
assert next_smallest([-3, -1, -2, -3]) == -2
assert next_smallest([100000000000000000000, -100000000000000000000, 0]) == 0
