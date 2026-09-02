def _all_digits_odd(n):
    result = True
    while n > 0:
        if n % 2 == 0:
            result = False
            break
        n //= 10
    return result


def unique_digits(x):
    result = []
    n = 0
    for n in x:
        if _all_digits_odd(n):
            result.append(n)
    return sorted(result)
