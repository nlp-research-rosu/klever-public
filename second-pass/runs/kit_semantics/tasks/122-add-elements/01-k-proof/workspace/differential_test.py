from solution import add_elements


def oracle(arr, k):
    # Independent direct transcription of the contract.
    return sum(value for value in arr[:k] if -99 <= value <= 99)


BOUNDARIES = [
    -1000,
    -101,
    -100,
    -99,
    -98,
    -10,
    -1,
    0,
    1,
    9,
    10,
    98,
    99,
    100,
    101,
    1000,
]


def main():
    cases = 0
    mismatches = []

    example = [111, 21, 3, 4000, 5, 6, 7, 8, 9]
    got = add_elements(example, 4)
    expected = oracle(example, 4)
    cases += 1
    if got != expected:
        mismatches.append((example, 4, got, expected))

    for length in range(1, 101):
        arr = [
            BOUNDARIES[(index * 7 + length * 3) % len(BOUNDARIES)]
            for index in range(length)
        ]
        for k in range(1, length + 1):
            got = add_elements(arr, k)
            expected = oracle(arr, k)
            cases += 1
            if got != expected:
                mismatches.append((arr, k, got, expected))

    print(f"cases={cases} mismatches={len(mismatches)}")
    if mismatches:
        print(mismatches[:3])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
