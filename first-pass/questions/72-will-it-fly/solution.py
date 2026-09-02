def will_it_fly(q, w):
    total = 0
    rev = []
    x = 0
    for x in q:
        total = total + x
        rev = [x] + rev
    return total <= w and q == rev
