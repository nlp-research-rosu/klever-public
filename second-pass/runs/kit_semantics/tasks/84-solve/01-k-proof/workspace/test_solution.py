from solution import solve


def oracle(n):
    return format(sum(int(char) for char in str(n)), "b")


def main():
    mismatches = []
    for n in range(10001):
        expected = oracle(n)
        actual = solve(n)
        if actual != expected:
            mismatches.append((n, actual, expected))

    represented = set()
    representation_count = 0
    for d4 in range(2):
        for d3 in range(10):
            for d2 in range(10):
                for d1 in range(10):
                    for d0 in range(10):
                        if d4 == 1 and (d0 != 0 or d1 != 0 or d2 != 0 or d3 != 0):
                            continue
                        represented.add(d0 + 10 * d1 + 100 * d2 + 1000 * d3 + 10000 * d4)
                        representation_count += 1

    expected_domain = set(range(10001))
    if represented != expected_domain or representation_count != 10001:
        raise AssertionError(
            (
                "digit-domain coverage mismatch",
                representation_count,
                len(represented),
                sorted(expected_domain - represented)[:10],
                sorted(represented - expected_domain)[:10],
            )
        )
    if mismatches:
        raise AssertionError(("solution mismatches", mismatches[:10]))

    print("digit-domain-check: 10001 unique representations cover 0..10000")
    print("python-differential-check: 10001/10001 passed; mismatches=0")


if __name__ == "__main__":
    main()
