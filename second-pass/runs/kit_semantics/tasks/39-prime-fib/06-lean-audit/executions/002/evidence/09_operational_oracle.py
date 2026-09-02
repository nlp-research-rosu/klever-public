#!/usr/bin/env python3


def scan(a: int, d: int, is_prime: bool) -> bool:
    d = max(d, 2)
    while is_prime and d * d <= a:
        if a % d == 0:
            is_prime = False
        d += 1
    return is_prime


def prime_fib(n: int) -> int:
    a, b, count = 0, 1, 0
    while count < n:
        a, b = b, a + b
        is_prime = scan(a, 2, a >= 2)
        count += int(is_prime)
    return a


false_flag_cases = [(-7, 2), (0, 2), (4, 2), (97, 2), (221, 2)]
scan_two_cases = [-7, 0, 1, 2, 3, 4, 5, 9, 25, 49, 97, 221]
suffix_cases = [(9, 3), (9, 4), (25, 3), (25, 6)]

print("false-flag absorption", [scan(a, d, False) for a, d in false_flag_cases])
print("scan from divisor 2", [scan(a, 2, True) for a in scan_two_cases])
print("suffix starts", [scan(a, d, True) for a, d in suffix_cases])
print("prime_fib(1..8)", [prime_fib(n) for n in range(1, 9)])
