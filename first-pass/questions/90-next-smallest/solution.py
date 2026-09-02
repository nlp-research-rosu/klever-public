def next_smallest(lst):
    if not lst:
        return None
    min1 = lst[0]
    for x in lst:
        if x < min1:
            min1 = x
    found = False
    m2 = 0
    for x in lst:
        if x > min1:
            if found:
                if x < m2:
                    m2 = x
            else:
                m2 = x
                found = True
    return m2 if found else None
