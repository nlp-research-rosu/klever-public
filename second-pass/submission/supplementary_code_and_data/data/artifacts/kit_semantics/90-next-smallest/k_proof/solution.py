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
        # Keep the loop variable in the semantics' integer subsort.  For the
        # promised integer inputs this is the identity operation.
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
