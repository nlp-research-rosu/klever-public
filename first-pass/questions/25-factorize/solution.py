def factorize(n):
    fact = []
    i = 2
    while i <= n:
        if n % i == 0:
            fact = fact + [i]
            n = n // i
        else:
            i = i + 1
    return fact
