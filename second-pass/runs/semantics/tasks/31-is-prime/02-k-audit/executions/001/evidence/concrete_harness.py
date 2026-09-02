def is_prime(n):
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


# Prompt examples.
assert is_prime(6) == False
assert is_prime(101) == True
assert is_prime(11) == True
assert is_prime(13441) == True
assert is_prime(61) == True
assert is_prime(4) == False
assert is_prime(1) == False

# Entry and loop boundaries.
assert is_prime(-1) == False
assert is_prime(0) == False
assert is_prime(2) == True
assert is_prime(3) == True
assert is_prime(9) == False
assert is_prime(25) == False
