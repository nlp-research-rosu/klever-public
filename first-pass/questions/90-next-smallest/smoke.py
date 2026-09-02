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


# Smoke checks from the prompt docstring (incl. the empty/single -> None cases).
assert next_smallest([1, 2, 3, 4, 5]) == 2
assert next_smallest([5, 1, 4, 3, 2]) == 2
assert next_smallest([]) is None
assert next_smallest([1, 1]) is None
