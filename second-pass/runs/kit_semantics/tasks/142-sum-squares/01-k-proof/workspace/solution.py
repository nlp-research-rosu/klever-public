def sum_squares(lst):
    result = 0
    index = 0
    value = 0
    for value in lst:
        if index % 3 == 0:
            result += value * value
        elif index % 4 == 0:
            result += value * value * value
        else:
            result += value
        index += 1
    return result
