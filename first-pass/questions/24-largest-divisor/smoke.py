def largest_divisor(n):
    result = 1
    for i in range(1, n):
        if n % i == 0:
            result = i
    return result


# Smoke checks from the prompt docstring (NOT hidden tests).
assert largest_divisor(15) == 5
