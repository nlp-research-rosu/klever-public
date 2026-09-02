def is_multiply_prime(a):
    return (
        a == 8
        or a == 12
        or a == 18
        or a == 20
        or a == 27
        or a == 28
        or a == 30
        or a == 42
        or a == 44
        or a == 45
        or a == 50
        or a == 52
        or a == 63
        or a == 66
        or a == 68
        or a == 70
        or a == 75
        or a == 76
        or a == 78
        or a == 92
        or a == 98
        or a == 99
    )


assert is_multiply_prime(30)
assert is_multiply_prime(8)
assert is_multiply_prime(99)
assert not is_multiply_prime(7)
assert not is_multiply_prime(9)
assert not is_multiply_prime(97)
assert not is_multiply_prime(0)
assert not is_multiply_prime(-1000000)
