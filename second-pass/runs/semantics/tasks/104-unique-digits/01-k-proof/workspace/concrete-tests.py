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


assert unique_digits([15, 33, 1422, 1]) == [1, 15, 33]
assert unique_digits([152, 323, 1422, 10]) == []
assert unique_digits([97531, 11, 2468, 7, 13570, 3]) == [3, 7, 11, 97531]
