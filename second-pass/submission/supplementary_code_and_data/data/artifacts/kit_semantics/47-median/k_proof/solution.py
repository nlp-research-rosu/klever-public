def median(l: list):
    """Return median of elements in the list l.
    >>> median([3, 1, 2, 4, 5])
    3
    >>> median([-10, 4, 6, 1000, 10, 20])
    15.0
    """
    ordered = sorted(l)
    size = len(ordered)
    if size % 2 == 1:
        return ordered[size // 2]
    else:
        return (ordered[size // 2 - 1] + ordered[size // 2]) / 2
