def below_threshold(l: list, t: int):
    """Return True if all numbers in the list l are below threshold t."""
    e = 0
    for e in l:
        if e < t:
            continue
        return False
    return True
