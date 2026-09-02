def digits(n):
    product = 1
    found = 0
    while n > 0:
        if n % 2 == 1:
            product = product * (n % 10)
            found = 1
        n = n // 10
    return product * found


result_1 = digits(1)
result_4 = digits(4)
result_235 = digits(235)
result_2468 = digits(2468)
result_97531 = digits(97531)

assert result_1 == 1
assert result_4 == 0
assert result_235 == 15
assert result_2468 == 0
assert result_97531 == 945
