import math
import random

from solution import greatest_common_divisor


def check(a: int, b: int) -> None:
    actual = greatest_common_divisor(a, b)
    expected = math.gcd(a, b)
    assert actual == expected, (a, b, actual, expected)


def main() -> None:
    checked = 0

    for a in range(-50, 51):
        for b in range(-50, 51):
            check(a, b)
            checked += 1

    rng = random.Random(20260724)
    for _ in range(1000):
        check(rng.randint(-10**12, 10**12), rng.randint(-10**12, 10**12))
        checked += 1

    print(f"differential cases: {checked}; mismatches: 0")


if __name__ == "__main__":
    main()
