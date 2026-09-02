def longest(strings):
    best = None
    s = ""
    for s in strings:
        if best is None or len(s) > len(best):
            best = s
    return best
