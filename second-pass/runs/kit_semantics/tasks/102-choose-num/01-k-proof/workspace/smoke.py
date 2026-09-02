def choose_num(x, y):
    if x > y:
        return -1
    if y % 2 == 0:
        return y
    if y - 1 >= x:
        return y - 1
    return -1


assert choose_num(12, 15) == 14
assert choose_num(13, 12) == -1
assert choose_num(1, 1) == -1
assert choose_num(1, 2) == 2
assert choose_num(2, 2) == 2
assert choose_num(3, 4) == 4
assert choose_num(4, 5) == 4
