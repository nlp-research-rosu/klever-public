#!/usr/bin/env python3
"""Generate explicit-oracle assertions for concrete execution in supplied K."""

from __future__ import annotations

import random


def expected(values: list[int]) -> list[int]:
    result = values.copy()
    result[::2] = sorted(values[::2])
    return result


def main() -> None:
    print("def sort_even(l: list):")
    print("    result = list(l)")
    print("    evens = sorted(l[::2])")
    print("    i = 0")
    print("    for i in range((len(l) + 1) // 2):")
    print("        result[2 * i] = evens[i]")
    print("    return result")
    print()

    cases = [
        [],
        [7],
        [2, 1],
        [9, 8, 3],
        [5, 6, 3, 4],
        [5, -9, -1, 8, 0],
    ]
    rng = random.Random(0x37E)
    for _ in range(20):
        length = rng.randrange(0, 13)
        cases.append([rng.randrange(-50, 51) for _ in range(length)])
    for values in cases:
        print(f"assert sort_even({values!r}) == {expected(values)!r}")
    print()
    print(f"# cases={len(cases)} seed={0x37E} lengths=0..12 values=-50..50")


if __name__ == "__main__":
    main()
