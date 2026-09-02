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
assert factorize(8) == [2, 2, 2]
assert factorize(25) == [5, 5]
assert factorize(70) == [2, 5, 7]
