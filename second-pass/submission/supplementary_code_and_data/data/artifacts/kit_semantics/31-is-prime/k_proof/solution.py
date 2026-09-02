def is_prime(n):
    if n < 2:
        return False
    divisor = 2
    result = True
    while divisor < n:
        if n % divisor == 0:
            result = False
        divisor = divisor + 1
    return result
