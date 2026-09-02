from itertools import product
from random import Random

from solution import smallest_change


def exhaustive_palindrome_oracle(arr, alphabet):
    """Search every palindromic target over the input alphabet."""
    if not arr:
        return 0

    half_len = (len(arr) + 1) // 2
    best = len(arr)
    for half in product(alphabet, repeat=half_len):
        if len(arr) % 2:
            target = half + half[-2::-1]
        else:
            target = half + half[::-1]
        distance = sum(left != right for left, right in zip(arr, target))
        best = min(best, distance)
    return best


def check(arr, alphabet):
    expected = exhaustive_palindrome_oracle(arr, alphabet)
    actual = smallest_change(list(arr))
    if actual != expected:
        raise AssertionError(
            f"input={list(arr)!r} actual={actual} expected={expected}"
        )


def main():
    exhaustive_alphabet = (-2, 0, 3)
    cases = 0

    for length in range(9):
        for arr in product(exhaustive_alphabet, repeat=length):
            check(arr, exhaustive_alphabet)
            cases += 1

    random_alphabet = (-5, -1, 0, 2)
    rng = Random(20260729)
    for _ in range(500):
        length = rng.randrange(13)
        arr = tuple(rng.choice(random_alphabet) for _ in range(length))
        check(arr, random_alphabet)
        cases += 1

    examples = (
        ([1, 2, 3, 5, 4, 7, 9, 6], 4),
        ([1, 2, 3, 4, 3, 2, 2], 1),
        ([1, 2, 3, 2, 1], 0),
        ([], 0),
        ([9], 0),
        ([1, 2], 1),
    )
    for arr, expected in examples:
        actual = smallest_change(arr)
        if actual != expected:
            raise AssertionError(
                f"example={arr!r} actual={actual} expected={expected}"
            )
        cases += 1

    print(f"cases={cases} mismatches=0")


if __name__ == "__main__":
    main()
