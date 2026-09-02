def get_positive(l: list):
    """Return only positive numbers in the list."""
    positive = []
    x = 0
    for x in l:
        if x > 0.0:
            positive.append(x)
    return positive
