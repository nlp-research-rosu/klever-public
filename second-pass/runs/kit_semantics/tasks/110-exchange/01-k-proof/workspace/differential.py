from itertools import combinations
from random import Random

from solution import exchange


def exchange_oracle(lst1, lst2):
    """Enumerate every possible final lst1 selection from the combined pool."""
    pool = list(lst1) + list(lst2)
    width = len(lst1)
    possible = any(
        all(value % 2 == 0 for value in chosen)
        for chosen in combinations(pool, width)
    )
    return "YES" if possible else "NO"


def main():
    rng = Random(20260729)
    values = [-4, -3, -2, -1, 0, 1, 2, 3, 4,
              -2.0, -1.5, 0.0, 1.5, 2.0, False, True]
    cases = [
        ([1, 2, 3, 4], [1, 2, 3, 4]),
        ([1, 2, 3, 4], [1, 5, 3, 4]),
        ([2], [1]),
        ([1], [2]),
        ([1.0, 2.0], [4.0]),
        ([True, False], [2]),
        ([-3, -2], [0]),
    ]
    for _ in range(5000):
        left = [rng.choice(values) for _ in range(rng.randint(1, 4))]
        right = [rng.choice(values) for _ in range(rng.randint(1, 4))]
        cases.append((left, right))

    mismatches = []
    for left, right in cases:
        actual = exchange(left, right)
        expected = exchange_oracle(left, right)
        if actual != expected:
            mismatches.append((left, right, actual, expected))

    print(f"cases={len(cases)} mismatches={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:10]:
            print(mismatch)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
