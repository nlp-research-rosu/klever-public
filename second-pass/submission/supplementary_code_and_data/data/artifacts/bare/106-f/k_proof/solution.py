def f(n):
    result = []
    factorial = 1
    total = 0
    i = 1
    while i <= n:
        factorial = factorial * i
        total = total + i
        if i % 2 == 0:
            result = result + [factorial]
        else:
            result = result + [total]
        i = i + 1
    return result
