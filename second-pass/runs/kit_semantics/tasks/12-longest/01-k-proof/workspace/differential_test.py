#!/usr/bin/env python3
import itertools
import random

from solution import longest


def oracle(strings):
    if not strings:
        return None
    maximum_length = max(map(len, strings))
    return next(string for string in strings if len(string) == maximum_length)


def main():
    checked = 0
    pool = ["", "a", "b", "bb", "cc", "ddd"]

    for size in range(6):
        for strings in itertools.product(pool, repeat=size):
            strings = list(strings)
            assert longest(strings) == oracle(strings), strings
            checked += 1

    rng = random.Random(20260729)
    unicode_pool = ["", "é", "猫", "🙂", "ab", "éé", "猫猫猫"]
    for _ in range(2000):
        strings = [
            rng.choice(unicode_pool)
            for _ in range(rng.randrange(0, 13))
        ]
        assert longest(strings) == oracle(strings), strings
        checked += 1

    print(f"differential: {checked}/{checked} passed")


if __name__ == "__main__":
    main()
