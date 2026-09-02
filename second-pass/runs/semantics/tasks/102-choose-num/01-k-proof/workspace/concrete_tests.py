def choose_num(x, y):
    if y % 2 == 0:
        if y >= x:
            return y
        return -1
    if y - 1 >= x:
        return y - 1
    return -1


assert choose_num(12, 15) == 14
assert choose_num(13, 12) == -1
assert choose_num(13, 13) == -1
assert choose_num(14, 14) == 14
assert choose_num(1, 1) == -1
assert choose_num(1, 2) == 2
assert choose_num(2, 1) == -1
assert choose_num(7, 10) == 10
