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


assert digits(1) == 1
assert digits(4) == 0
assert digits(235) == 15
assert digits(2468) == 0
assert digits(13579) == 945
assert digits(10203) == 3
