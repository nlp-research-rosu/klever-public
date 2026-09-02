def tri(n):
    if n == 0:
        return [1]
    my_tri = [1, 3]
    a = 1
    b = 3
    for i in range(2, n + 1):
        if i % 2 == 0:
            c = i // 2 + 1
        else:
            c = b + a + (i + 3) // 2
        my_tri = my_tri + [c]
        a = b
        b = c
    return my_tri
