def common(l1: list, l2: list):
    result = []
    item = 0
    for item in l1:
        if item in l2 and item not in result:
            result.append(item)
    return sorted(result)


# Python and the canonical implementation return [True].  The supplied K
# membership fold compares Bool true and Int 1 with structural K equality,
# producing the empty list and therefore failing this assertion.
assert common([True], [1]) == [True]
