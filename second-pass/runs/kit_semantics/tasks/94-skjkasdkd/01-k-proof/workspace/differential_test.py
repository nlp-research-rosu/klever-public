import itertools
import random

from solution import skjkasdkd


def oracle(values):
    primes = [
        value
        for value in values
        if value >= 2
        and all(value % divisor for divisor in range(2, value))
    ]
    largest = max(primes, default=0)
    return sum(int(character) for character in str(largest))


def main():
    tested = 0
    mismatches = []

    alphabet = range(-2, 13)
    for length in range(5):
        for values in itertools.product(alphabet, repeat=length):
            expected = oracle(values)
            actual = skjkasdkd(list(values))
            tested += 1
            if actual != expected:
                mismatches.append((values, expected, actual))

    generator = random.Random(20260730)
    for _ in range(500):
        values = [
            generator.randint(-100, 6000)
            for _ in range(generator.randint(0, 12))
        ]
        expected = oracle(values)
        actual = skjkasdkd(values)
        tested += 1
        if actual != expected:
            mismatches.append((values, expected, actual))

    print(f"tested={tested}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(f"first_mismatch={mismatches[0]}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
