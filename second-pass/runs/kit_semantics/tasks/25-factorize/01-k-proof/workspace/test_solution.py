import math

from solution import factorize


def independent_oracle(n: int) -> list[int]:
    result: list[int] = []
    remaining = n
    candidate = 2
    while candidate * candidate <= remaining:
        while remaining % candidate == 0:
            result.append(candidate)
            remaining //= candidate
        candidate += 1
    if remaining > 1:
        result.append(remaining)
    return result


def main() -> None:
    checked = 0
    inputs = list(range(1, 2001)) + [9973, 65536, 99991]
    for n in inputs:
        actual = factorize(n)
        expected = independent_oracle(n)
        assert actual == expected, (n, actual, expected)
        assert actual == sorted(actual), (n, actual)
        assert all(p >= 2 and all(p % d for d in range(2, math.isqrt(p) + 1))
                   for p in actual), (n, actual)
        assert math.prod(actual) == n, (n, actual)
        checked += 1
    print(f"differential inputs={checked} mismatches=0")


if __name__ == "__main__":
    main()
