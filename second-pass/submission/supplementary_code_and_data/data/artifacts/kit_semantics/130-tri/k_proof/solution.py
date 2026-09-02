def tri(n):
    values = []
    i = 0
    while i <= n:
        if i == 0:
            values.append(1)
        elif i == 1:
            values.append(3)
        elif i % 2 == 0:
            values.append(1 + i // 2)
        else:
            values.append((i // 2 + 1) * (i // 2 + 3))
        i += 1
    return values
