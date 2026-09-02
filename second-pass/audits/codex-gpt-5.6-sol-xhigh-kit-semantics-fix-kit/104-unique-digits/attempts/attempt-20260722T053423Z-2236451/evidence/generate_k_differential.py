#!/usr/bin/env python3
"""Generate deterministic K-executable assertions from an arithmetic oracle."""

from __future__ import annotations

import hashlib
import random
import sys
from pathlib import Path


def has_only_odd_digits(number: int) -> bool:
    while number > 0:
        digit = number % 10
        if digit % 2 == 0:
            return False
        number //= 10
    return True


def insertion_sort(values: list[int]) -> list[int]:
    result: list[int] = []
    for value in values:
        index = 0
        while index < len(result) and result[index] <= value:
            index += 1
        result.insert(index, value)
    return result


def oracle(values: list[int]) -> list[int]:
    return insertion_sort([value for value in values if has_only_odd_digits(value)])


def cases() -> list[list[int]]:
    result = [
        [],
        [1],
        [2],
        [15, 33, 1422, 1],
        [152, 323, 1422, 10],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [101],
        [121],
        [141],
        [161],
        [181],
        [13579, 97531, 11111],
        [33, 1, 33, 20, 15, 3, 15],
        [211, 121, 112, 411, 141, 114],
        [611, 161, 116, 811, 181, 118],
        [999999999, 777777777, 135790864, 2468],
        list(range(1, 31)),
        list(reversed(range(95, 126))),
        [111111111, 222222222, 333333333, 444444444],
        [97531, 97531, 86420, 13579, 13579],
    ]
    rng = random.Random(104104)
    lengths = [0, 1, 2, 5, 10, 20]
    while len(result) < 151:
        length = lengths[len(result) % len(lengths)]
        values = [rng.randint(1, 10**9) for _ in range(length)]
        if len(result) % 13 == 0 and values:
            values[-1] = values[0]
        result.append(values)
    return result


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} CANDIDATE_SOLUTION.py OUTPUT.py", file=sys.stderr)
        return 64
    solution = Path(sys.argv[1]).read_text(encoding="utf-8")
    output = Path(sys.argv[2])
    selected = cases()
    lines = [solution.rstrip(), ""]
    for index, values in enumerate(selected):
        expected = oracle(values)
        lines.append(f"assert unique_digits({values!r}) == {expected!r}")
    lines.append("")
    data = "\n".join(lines).encode("utf-8")
    output.write_bytes(data)
    print("ORACLE: arithmetic digit extraction plus reviewer insertion sort")
    print("SCOPE: 20 directed cases plus deterministic random cases; seed=104104; positive values 1..10**9")
    print(f"K_CASES: {len(selected)}")
    print(f"GENERATED_SHA256: {hashlib.sha256(data).hexdigest()}")
    print(f"OUTPUT: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
