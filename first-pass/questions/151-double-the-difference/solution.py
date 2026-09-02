def double_the_difference(lst):
    result = 0
    e = 0
    for e in lst:
        if e > 0:
            if e % 2 == 1:
                result = result + e * e
    return result
