def add(lst):
    """Add the even elements that occur at odd zero-based indices."""
    total = 0
    odd_index = False
    value = 0
    for value in lst:
        if odd_index:
            if value % 2 == 0:
                total += value
        odd_index = not odd_index
    return total
