from solution import fib4


def contract_oracle(n: int) -> int:
    values = [0, 0, 2, 0]
    for i in range(4, n + 1):
        values.append(
            values[i - 1]
            + values[i - 2]
            + values[i - 3]
            + values[i - 4]
        )
    return values[n]


def main() -> None:
    examples = {5: 4, 6: 8, 7: 14}
    for n, expected in examples.items():
        assert fib4(n) == expected

    mismatches = []
    for n in range(201):
        actual = fib4(n)
        expected = contract_oracle(n)
        if actual != expected:
            mismatches.append((n, actual, expected))

    print("domain: n = 0..200")
    print("oracle: direct prompt recurrence with stored prefix")
    print(f"mismatches: {len(mismatches)}")
    if mismatches:
        print(mismatches[:10])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
