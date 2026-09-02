def double_the_difference(lst):
    total = 0
    for value in lst:
        if isinstance(value, int):
            if value >= 0:
                if value % 2 == 1:
                    total = total + value * value
    return total
