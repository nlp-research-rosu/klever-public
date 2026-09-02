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


results = [
    is_prime(-7),
    is_prime(0),
    is_prime(1),
    is_prime(2),
    is_prime(3),
    is_prime(4),
    is_prime(6),
    is_prime(9),
    is_prime(11),
    is_prime(25),
    is_prime(31),
    is_prime(61),
    is_prime(101),
    is_prime(997),
]
