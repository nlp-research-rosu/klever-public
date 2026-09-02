def digits(n):
    result = 0
    while n > 0:
        digit = n % 10
        if digit % 2 == 1:
            if result == 0:
                result = digit
            else:
                result = result * digit
        n = n // 10
    return result
