def prod_signs(arr):
    sum_abs = 0
    sign_prod = 1
    n = 0
    x = 0
    for x in arr:
        n = n + 1
        if x < 0:
            sum_abs = sum_abs + (0 - x)
            sign_prod = sign_prod * (-1)
        elif x > 0:
            sum_abs = sum_abs + x
        else:
            sign_prod = sign_prod * 0
    result = None
    if n > 0:
        result = sign_prod * sum_abs
    return result
