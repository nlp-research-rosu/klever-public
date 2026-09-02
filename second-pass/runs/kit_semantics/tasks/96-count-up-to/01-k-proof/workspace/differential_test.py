from math import isqrt

from solution import count_up_to


def oracle(bound):
    return [
        candidate
        for candidate in range(2, bound)
        if all(
            candidate % divisor
            for divisor in range(2, isqrt(candidate) + 1)
        )
    ]


def main():
    mismatches = []
    for bound in range(0, 201):
        actual = count_up_to(bound)
        expected = oracle(bound)
        if actual != expected:
            mismatches.append((bound, actual, expected))

    print(f"differential inputs: 0..200; mismatches: {len(mismatches)}")
    if mismatches:
        raise AssertionError(mismatches[:3])


if __name__ == "__main__":
    main()
