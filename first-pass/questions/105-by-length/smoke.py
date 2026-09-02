def word(v):
    if v == 1:
        return "One"
    if v == 2:
        return "Two"
    if v == 3:
        return "Three"
    if v == 4:
        return "Four"
    if v == 5:
        return "Five"
    if v == 6:
        return "Six"
    if v == 7:
        return "Seven"
    if v == 8:
        return "Eight"
    if v == 9:
        return "Nine"
    return ""


def by_length(arr):
    n = len(arr)
    s = sorted(arr)
    result = []
    i = 0
    v = 0
    for i in range(0, n):
        v = s[n - 1 - i]
        if v >= 1:
            if v <= 9:
                result = result + [word(v)]
    return result


# Smoke checks from the prompt docstring (NOT hidden tests).
assert by_length([2, 1, 1, 4, 5, 8, 2, 3]) == ["Eight", "Five", "Four", "Three", "Two", "Two", "One", "One"]
assert by_length([]) == []
assert by_length([1, 0, 55]) == ["One"]
