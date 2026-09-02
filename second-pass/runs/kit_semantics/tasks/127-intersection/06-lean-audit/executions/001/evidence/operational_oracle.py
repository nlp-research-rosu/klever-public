#!/usr/bin/env python3
"""Independent executable oracle for the frozen K summary equations."""


def tmod(dividend: int, divisor: int) -> int:
    if divisor == 0:
        raise ZeroDivisionError("K INT.tmod is undefined at divisor zero")
    quotient = abs(dividend) // abs(divisor)
    if (dividend < 0) != (divisor < 0):
        quotient = -quotient
    return dividend - quotient * divisor


def py_mod(dividend: int, divisor: int) -> int:
    return tmod(tmod(dividend, divisor) + divisor, divisor)


def scan_has_divisor(seen: bool, number: int, divisor: int) -> bool:
    if seen:
        return True
    if divisor < 2:
        divisor = 2
    while divisor < number:
        if py_mod(number, divisor) == 0:
            return True
        divisor += 1
    return False


def main() -> None:
    print(("and-tt", True and True))
    print(("and-tf", True and False))
    print(("ge-2-2", 2 >= 2))
    print(("ge-neg", -3 >= 2))
    print(("lt-2-9", 2 < 9))
    print(("ne-4-0", 4 != 0))
    print(("add-neg", -5 + 8))
    for label, left, right in [
        ("pymod--7-3", -7, 3),
        ("pymod-7--3", 7, -3),
        ("pymod--7--3", -7, -3),
        ("pymod-9-2", 9, 2),
        ("pymod-9-3", 9, 3),
    ]:
        print((label, py_mod(left, right)))
    for label, seen, number, divisor in [
        ("scan-seen", True, 97, -10),
        ("scan-n2-d2", False, 2, 2),
        ("scan-prime3", False, 3, 2),
        ("scan-composite4", False, 4, 2),
        ("scan-prime5-dneg", False, 5, -4),
        ("scan-composite9-d2", False, 9, 2),
        ("scan-composite9-d3", False, 9, 3),
        ("scan-composite25-d4", False, 25, 4),
        ("scan-empty-dgt", False, 7, 9),
        ("scan-negative-n", False, -3, -9),
    ]:
        print((label, scan_has_divisor(seen, number, divisor)))


if __name__ == "__main__":
    main()
