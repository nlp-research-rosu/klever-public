def median(l: list):
    ordered = sorted(l)
    size = len(ordered)
    if size % 2 == 1:
        return 0
    else:
        return (ordered[size // 2 - 1] + ordered[size // 2]) / 2
