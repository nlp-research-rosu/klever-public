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


# Documented examples.
assert unique_digits([15, 33, 1422, 1]) == [1, 15, 33]
assert unique_digits([152, 323, 1422, 10]) == []

# Empty list, smallest positive inputs, both helper branches, later even digit.
assert unique_digits([]) == []
assert unique_digits([1]) == [1]
assert unique_digits([2]) == []
assert unique_digits([11, 12, 21, 22]) == [11]

# Sorting, duplicates, break on an even digit at different positions.
assert unique_digits([99, 1, 99, 13, 2, 13]) == [1, 13, 13, 99, 99]
assert unique_digits([111112, 211111, 111211, 111111]) == [111111]
