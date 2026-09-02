def string_sequence(n):
    result = str(0)
    x = 0
    for x in range(1, n + 1):
        result = result + ' ' + str(x)
    return result
