def sum_squares(lst):
    if lst == []:
        return 0
    else:
        index = len(lst) - 1
        value = lst[-1]
        if index % 3 == 0:
            contribution = value * value
        else:
            if index % 4 == 0:
                contribution = value * value * value
            else:
                contribution = value
        return sum_squares(lst[:-1]) + contribution
