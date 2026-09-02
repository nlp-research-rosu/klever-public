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


# Contract examples, branch boundaries, a zero extension case, and larger cases.
assert digits(1) == 1
assert digits(4) == 0
assert digits(235) == 15
assert digits(0) == 0
assert digits(10) == 1
assert digits(11) == 1
assert digits(19) == 9
assert digits(10203) == 3
assert digits(2468) == 0
assert digits(13579) == 945
assert digits(99999999999999999999) == 12157665459056928801
