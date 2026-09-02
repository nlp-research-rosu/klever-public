def special_factorial(n):
    factorial = 1
    result = 1
    i = 1
    while i <= n:
        factorial = factorial * i
        result = result * factorial
        i = i + 1
    return result


assert special_factorial(1) == 1
assert special_factorial(2) == 2
assert special_factorial(3) == 12
assert special_factorial(4) == 288
assert special_factorial(5) == 34560
assert special_factorial(6) == 24883200
