def greatest_common_divisor(a, b):
    while b:
        a, b = (b, a % b)
    return a


# Smoke checks from the prompt docstring (NOT hidden tests).
assert greatest_common_divisor(3, 5) == 1
assert greatest_common_divisor(25, 15) == 5
