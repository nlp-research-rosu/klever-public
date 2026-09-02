def tri(n):
    if n == 0:
        return [1]

    result = [1, 3]
    a = 1
    b = 3
    value = 3
    i = 2

    while i <= n:
        if i % 2 == 0:
            value = 1 + i // 2
        else:
            value = b + a + 1 + (i + 1) // 2

        result.append(value)
        a = b
        b = value
        i += 1

    return result
