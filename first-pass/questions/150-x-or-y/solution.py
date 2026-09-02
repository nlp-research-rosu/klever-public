def x_or_y(n, x, y):
    prime = n != 1
    k = 0
    for k in range(2, n):
        if n % k == 0:
            prime = False
    if prime:
        ans = x
    else:
        ans = y
    return ans
