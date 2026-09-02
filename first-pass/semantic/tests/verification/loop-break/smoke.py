def f(xs):
    total = 0
    for x in xs:
        if x < 0:
            break
        total += x
    return total


assert f([1, 2, 3]) == 6
assert f([1, 2, -1, 5]) == 3
assert f([]) == 0
assert f([-1, 5]) == 0
