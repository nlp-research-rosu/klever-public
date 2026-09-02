def add(lst):
    result = 0
    odd = False
    value = 0
    for value in lst:
        if odd:
            if value % 2 == 0:
                result += value
        odd = not odd
    return result
