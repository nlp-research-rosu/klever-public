def digits(n):
    product = 0
    while n > 0:
        if n % 2 == 1:
            if product == 0:
                product = n % 10
            else:
                product *= n % 10
        n //= 10
    return product
