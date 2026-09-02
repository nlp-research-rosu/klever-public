def prod_signs(arr):
    if arr == []:
        return None

    total = 0
    sign = 1
    x = 0
    for x in arr:
        if x < 0:
            total = total - x
            sign = -sign
        else:
            total = total + x
            if x == 0:
                sign = 0

    return total * sign
