def special_factorial(n):
    factorial = 1
    result = 1
    i = 1
    while i <= n:
        factorial *= i
        result *= factorial
        i += 1
    return result
