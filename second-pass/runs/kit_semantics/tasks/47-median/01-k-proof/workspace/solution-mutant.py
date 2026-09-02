def median(l: list):
    """Gate A body-sensitivity mutant: the odd result is deliberately wrong."""
    ordered = sorted(l)
    size = len(ordered)
    if size % 2 == 1:
        return 0
    else:
        return (ordered[size // 2 - 1] + ordered[size // 2]) / 2
