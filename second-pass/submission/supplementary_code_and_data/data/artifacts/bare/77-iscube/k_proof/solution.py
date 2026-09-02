def iscube(a):
    if a < 0:
        a = -a
    n = 0
    while n * n * n < a:
        n = n + 1
    return n * n * n == a
