def prod_signs(arr):
    """
    Return the sum of the magnitudes in arr multiplied by the product of
    their signs.  The empty input has no such product and returns None.
    """
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
