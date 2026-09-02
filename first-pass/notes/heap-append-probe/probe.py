def build_squares(n):
    result = []
    i = 0
    for i in range(n):
        result.append(i * i)
    return result


def build_plus(n):
    out = []
    i = 0
    for i in range(n):
        out = out + [i]
    return out


assert build_squares(0) == []
assert build_squares(4) == [0, 1, 4, 9]
assert build_plus(0) == []
assert build_plus(3) == [0, 1, 2]
