def is_prime(n):
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


assert is_prime(-5) == False
assert is_prime(0) == False
assert is_prime(1) == False
assert is_prime(2) == True
assert is_prime(3) == True
assert is_prime(4) == False
assert is_prime(5) == True
assert is_prime(8) == False
assert is_prime(9) == False
assert is_prime(25) == False
assert is_prime(29) == True
assert is_prime(31) == True
assert is_prime(49) == False
assert is_prime(97) == True
assert is_prime(121) == False
assert is_prime(13441) == True
