def rolling_max(numbers):
    result = []
    m = 0
    first = True
    n = 0
    for n in numbers:
        if first:
            m = n
            first = False
        else:
            if n > m:
                m = n
        result = result + [m]
    return result
