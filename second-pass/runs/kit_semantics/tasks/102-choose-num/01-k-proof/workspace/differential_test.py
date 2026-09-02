from solution import choose_num


def brute_force_oracle(x, y):
    candidates = [n for n in range(x, y + 1) if n % 2 == 0]
    return max(candidates) if candidates else -1


def main():
    checked = 0
    for x in range(1, 201):
        for y in range(1, 201):
            expected = brute_force_oracle(x, y)
            actual = choose_num(x, y)
            assert actual == expected, (x, y, actual, expected)
            checked += 1
    print(f"differential: {checked} positive-integer pairs, 0 mismatches")


if __name__ == "__main__":
    main()
