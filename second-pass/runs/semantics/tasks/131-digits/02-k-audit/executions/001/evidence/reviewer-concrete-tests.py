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


assert digits(0) == 0
assert digits(1) == 1
assert digits(2) == 0
assert digits(4) == 0
assert digits(9) == 9
assert digits(10) == 1
assert digits(11) == 1
assert digits(99) == 81
assert digits(100) == 1
assert digits(235) == 15
assert digits(2468) == 0
assert digits(10203) == 3
assert digits(13579) == 945
