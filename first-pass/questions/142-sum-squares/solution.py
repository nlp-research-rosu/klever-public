def sum_squares(lst):
    result = 0
    i = 0
    e = 0
    for e in lst:
        if i % 3 == 0:
            result = result + e * e
        else:
            if i % 4 == 0:
                result = result + e * e * e
            else:
                result = result + e
        i = i + 1
    return result
