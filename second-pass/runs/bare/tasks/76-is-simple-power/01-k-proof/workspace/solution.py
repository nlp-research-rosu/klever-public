def is_simple_power(x, n):
    if x == 1:
        return True
    if x < 1:
        return False
    if n < 2:
        return False
    power = n
    while power < x:
        power = power * n
    return power == x
