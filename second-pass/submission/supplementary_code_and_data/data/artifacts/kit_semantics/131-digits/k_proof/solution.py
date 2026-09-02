def digits(n):
    product = 1
    found = 0
    while n > 0:
        if n % 2 == 1:
            product = product * (n % 10)
            found = 1
        n = n // 10
    return product * found
