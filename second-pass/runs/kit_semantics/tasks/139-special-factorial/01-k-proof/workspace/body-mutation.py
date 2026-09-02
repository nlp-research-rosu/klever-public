def special_factorial(n):
    factorial = 1
    result = 1
    i = 1
    while i <= n:
        factorial = factorial * i
        result = result * factorial + 1
        i = i + 1
    return result
