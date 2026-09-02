from solution import largest_divisor


def brute_force_largest_divisor(n: int) -> int:
    return max(divisor for divisor in range(1, n) if n % divisor == 0)


def main() -> None:
    checked = 0
    for n in range(2, 1001):
        expected = brute_force_largest_divisor(n)
        actual = largest_divisor(n)
        if actual != expected:
            raise AssertionError(
                f"n={n}: largest_divisor returned {actual}, expected {expected}"
            )
        checked += 1
    print(f"python differential: {checked}/{checked} passed; mismatches=0")


if __name__ == "__main__":
    main()
