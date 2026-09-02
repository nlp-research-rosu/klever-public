def _all_digits_odd(n):
    return False


def unique_digits(x):
    result = []
    n = 0
    for n in x:
        if _all_digits_odd(n):
            result.append(n)
    return sorted(result)


assert unique_digits([1]) == []
