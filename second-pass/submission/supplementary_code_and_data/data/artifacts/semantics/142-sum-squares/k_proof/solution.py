def sum_squares(lst):
    total = 0
    index = 0
    for value in lst:
        if index % 3 == 0:
            total += value * value
        else:
            if index % 4 == 0:
                total += value * value * value
            else:
                total += value
        index += 1
    return total
