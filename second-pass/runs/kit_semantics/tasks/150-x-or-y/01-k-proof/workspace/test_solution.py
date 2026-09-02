from math import isqrt

from solution import x_or_y


def oracle(n, x, y):
    if n < 2:
        return y
    for divisor in range(2, isqrt(n) + 1):
        if n % divisor == 0:
            return y
    return x


def main():
    cases = [
        (n, 3 * n + 1, -2 * n - 5)
        for n in range(-20, 201)
    ]
    cases.extend([(7, 34, 12), (15, 8, 5)])

    mismatches = [
        (args, x_or_y(*args), oracle(*args))
        for args in cases
        if x_or_y(*args) != oracle(*args)
    ]
    print(f"cases={len(cases)} mismatches={len(mismatches)}")
    if mismatches:
        print(mismatches)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
