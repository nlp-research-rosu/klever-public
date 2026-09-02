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


# HumanEval/128 test cases (the dataset `check`); returns an int or None.
assert prod_signs([1, 2, 2, -4]) == -9
assert prod_signs([0, 1]) == 0
assert prod_signs([1, 1, 1, 2, 3, -1, 1]) == -10
assert prod_signs([]) is None
assert prod_signs([2, 4, 1, 2, -1, -1, 9]) == 20
assert prod_signs([-1, 1, -1, 1]) == 4
assert prod_signs([-1, 1, 1, 1]) == -4
assert prod_signs([-1, 1, 1, 0]) == 0
