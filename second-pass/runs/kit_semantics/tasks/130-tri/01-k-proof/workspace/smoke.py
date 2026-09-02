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


assert tri(0) == [1]
assert tri(1) == [1, 3]
assert tri(2) == [1, 3, 2]
assert tri(3) == [1, 3, 2, 8]
assert tri(4) == [1, 3, 2, 8, 3]
assert tri(5) == [1, 3, 2, 8, 3, 15]
