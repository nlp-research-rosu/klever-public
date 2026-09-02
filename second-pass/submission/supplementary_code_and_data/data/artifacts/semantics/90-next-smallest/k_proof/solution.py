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
