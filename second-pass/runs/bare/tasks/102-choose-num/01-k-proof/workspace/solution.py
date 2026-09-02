def choose_num(x, y):
    return -1 if x > y else (y if y % 2 == 0 else (-1 if x == y else y - 1))
