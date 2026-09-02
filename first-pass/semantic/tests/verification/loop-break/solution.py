def f(xs):
    total = 0
    for x in xs:
        if x < 0:
            break
        total += x
    return total
