def f(xs):
    total = 0
    for x in xs:
        if x < 0:
            continue
        total += x
    return total
