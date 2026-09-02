from solution import starts_one_ends


def brute_force_count(n):
    lower = 10 ** (n - 1)
    upper = 10 ** n
    return sum(
        str(value).startswith("1") or str(value).endswith("1")
        for value in range(lower, upper)
    )


def main():
    checked = []
    for n in range(1, 7):
        actual = starts_one_ends(n)
        expected = brute_force_count(n)
        assert actual == expected, (n, actual, expected)
        checked.append((n, actual))
    print("validated n=1..6:", checked)
    print("mismatches: 0")


if __name__ == "__main__":
    main()
