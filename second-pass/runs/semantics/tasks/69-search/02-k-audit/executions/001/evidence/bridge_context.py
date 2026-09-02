def probe(lst):
    result = -1
    value = 99
    for value in lst:
        count = 0
        for item in lst:
            if item == value:
                count += 1
        if count >= value:
            if value > result:
                result = value
    return value


# Fixed Python and fixed supplied K semantics both return the last iterated
# value.  The candidate bridge instead preserves the pre-loop sentinel 99.
assert probe([2]) == 2
assert probe([2]) != 99
