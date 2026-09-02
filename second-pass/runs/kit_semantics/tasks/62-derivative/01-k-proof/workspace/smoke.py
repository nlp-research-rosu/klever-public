def derivative(xs: list):
    result = []
    i = 0
    x = None
    for x in xs:
        if i > 0:
            result.append(i * x)
        i = i + 1
    return result


assert derivative([]) == []
assert derivative([7]) == []
assert derivative([1, 2, 3]) == [2, 6]
assert derivative([3, 1, 2, 4, 5]) == [1, 4, 12, 20]
assert derivative([0, -2, 4, -3]) == [-2, 8, -9]
assert derivative([1.0, 2.5, -3.0]) == [2.5, -6.0]
