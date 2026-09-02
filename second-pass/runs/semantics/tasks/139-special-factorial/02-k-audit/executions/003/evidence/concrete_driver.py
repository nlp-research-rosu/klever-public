def special_factorial(n):
    factorial = 1
    result = 1
    i = 1
    while i <= n:
        factorial *= i
        result *= factorial
        i += 1
    return result


# Intended-domain lower boundary, documented example, and a larger normal case.
assert special_factorial(1) == 1
assert special_factorial(4) == 288
assert special_factorial(6) == 24883200

# Robustness boundary just outside the stated n > 0 contract.
assert special_factorial(0) == 1
