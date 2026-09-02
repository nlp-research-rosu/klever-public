def median(l: list):
    ordered = sorted(l)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    else:
        return (ordered[middle] + ordered[middle + 1]) / 2
