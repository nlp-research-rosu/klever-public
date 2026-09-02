def pairs_sum_to_zero(l):
    found = False
    x = 0
    for x in l:
        if x == 0:
            if l.count(0) > 1:
                found = True
        else:
            if l.count(-x) > 0:
                found = True
    return found
