from solution import modp


def main():
    cases = set()
    for n in range(257):
        for p in range(-64, 65):
            if p != 0:
                cases.add((n, p))

    cases.update(
        {
            (0, 1),
            (0, 101),
            (3, 5),
            (3, 11),
            (100, 101),
            (1101, 101),
            (10000, 65537),
            (10000, -65537),
        }
    )

    mismatches = []
    for n, p in sorted(cases):
        actual = modp(n, p)
        expected = pow(2, n, p)
        if actual != expected:
            mismatches.append((n, p, actual, expected))

    print(f"cases={len(cases)} mismatches={len(mismatches)}")
    if mismatches:
        print(mismatches[:10])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
