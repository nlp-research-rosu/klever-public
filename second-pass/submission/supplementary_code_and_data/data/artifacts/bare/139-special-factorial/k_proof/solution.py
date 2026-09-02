def factorial(n):
    if n <= 1:
        return 1
    old_n = n
    n = n - 1
    return old_n * factorial(n)


def special_factorial(n):
    if n <= 1:
        return 1
    factorial_n = factorial(n)
    n = n - 1
    return factorial_n * special_factorial(n)
