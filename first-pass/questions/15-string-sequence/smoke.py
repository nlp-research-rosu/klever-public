def string_sequence(n):
    result = str(0)
    x = 0
    for x in range(1, n + 1):
        result = result + ' ' + str(x)
    return result


# Smoke checks: the prompt docstring cases + a multi-digit case (exercises str(x) for x >= 10).
assert string_sequence(0) == '0'
assert string_sequence(5) == '0 1 2 3 4 5'
assert string_sequence(12) == '0 1 2 3 4 5 6 7 8 9 10 11 12'
