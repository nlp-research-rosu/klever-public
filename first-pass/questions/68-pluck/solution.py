def pluck(arr):
    # Behavior-preserving rewrite of canonical.py over the documented domain
    # (arr a list of non-negative ints).  canonical returns
    #   [min even value, FIRST index of that value]  or  []  if empty / no even.
    # Single indexed scan tracking (found, bestVal, bestIdx) and a position
    # counter i.  Update ONLY on a STRICTLY-smaller even value, so the FIRST
    # occurrence wins ties (== arr.index(min(evens))).
    i = 0
    found = False
    bestVal = 0
    bestIdx = 0
    v = 0
    for v in arr:
        if v % 2 == 0:
            if not found:
                bestVal = v
                bestIdx = i
                found = True
            else:
                if v < bestVal:
                    bestVal = v
                    bestIdx = i
        i = i + 1
    if found:
        return [bestVal, bestIdx]
    else:
        return []
