def f(xs):
    total = 0
    for x in xs:
        if x < 0:
            continue
        total += x
    return total


assert f([1, 2, 3]) == 6
assert f([1, -2, 3]) == 4
assert f([]) == 0
assert f([-1, -5]) == 0
assert f([-1, 5]) == 5
