def choose_num(x, y):
    if y % 2 == 0:
        if y >= x:
            return y
        return -1
    if y - 1 >= x:
        return y - 1
    return -1
