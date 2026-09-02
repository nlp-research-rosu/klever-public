import random

from solution import eat


def oracle(number, need, remaining):
    consumed = min(need, remaining)
    return [number + consumed, remaining - consumed]


def main():
    boundaries = (0, 1, 2, 5, 10, 999, 1000)
    cases = [
        (5, 6, 10),
        (4, 8, 9),
        (1, 10, 10),
        (2, 11, 5),
    ]
    cases.extend(
        (number, need, remaining)
        for number in boundaries
        for need in boundaries
        for remaining in boundaries
    )

    generator = random.Random(20260725)
    cases.extend(
        (
            generator.randint(0, 1000),
            generator.randint(0, 1000),
            generator.randint(0, 1000),
        )
        for _ in range(10000)
    )

    mismatches = []
    for args in cases:
        actual = eat(*args)
        expected = oracle(*args)
        if actual != expected:
            mismatches.append((args, actual, expected))

    print(
        "differential cases:",
        len(cases),
        "mismatches:",
        len(mismatches),
    )
    if mismatches:
        print("first mismatch:", mismatches[0])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
