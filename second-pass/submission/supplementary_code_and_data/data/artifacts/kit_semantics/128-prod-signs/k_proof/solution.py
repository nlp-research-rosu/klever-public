def prod_signs(arr):
    total = 0
    sign = 1
    seen = 0
    for value in arr:
        seen = 1
        total = total + abs(value)
        if value < 0:
            sign = 0 - sign
        elif value > 0:
            sign = sign
        else:
            sign = 0

    if seen == 0:
        return None
    return total * sign
