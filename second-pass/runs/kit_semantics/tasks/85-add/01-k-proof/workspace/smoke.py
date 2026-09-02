def add(lst):
    result = 0
    odd = False
    value = 0
    for value in lst:
        if odd:
            if value % 2 == 0:
                result += value
        odd = not odd
    return result


example = add([4, 2, 6, 7])
singleton = add([10])
mixed_sign = add([1, -2, 3, -4, 5, 8])
