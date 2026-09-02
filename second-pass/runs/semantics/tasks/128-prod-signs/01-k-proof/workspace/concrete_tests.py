def prod_signs(arr):
    if arr == []:
        return None

    total = 0
    sign = 1
    for value in arr:
        if value < 0:
            total = total - value
            sign = 0 - sign
        else:
            total = total + value
            if value == 0:
                sign = 0

    return total * sign


assert prod_signs([1, 2, 2, -4]) == -9
assert prod_signs([0, 1]) == 0
assert prod_signs([]) is None
assert prod_signs([-2, -3]) == 5
assert prod_signs([-2, 0, -3]) == 0
assert prod_signs([5]) == 5
assert prod_signs([-5]) == -5
