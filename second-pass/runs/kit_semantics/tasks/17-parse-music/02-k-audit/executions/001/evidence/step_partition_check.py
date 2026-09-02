#!/usr/bin/env python3
"""Check every guard partition of the proof-local one-character summary."""

from __future__ import annotations


def source_step(acc: tuple[int, ...], code: int, current: int):
    if code == 111:  # "o"
        current = 4
    elif code == 46:  # "."
        current = 1
    elif code == 124:  # "|"
        if current == 4:
            current = 2
        acc += (current,)
        current = 0
    else:
        if current == 4:
            acc += (current,)
        current = 0
    return acc, current


def proof_summary_step(acc: tuple[int, ...], code: int, current: int):
    if code == 124 and current == 4:
        result = acc + (2,)
    elif code == 124 and current != 4:
        result = acc + (current,)
    elif code not in (111, 46, 124) and current == 4:
        result = acc + (4,)
    else:
        result = acc

    if code == 111:
        next_current = 4
    elif code == 46:
        next_current = 1
    else:
        next_current = 0
    return result, next_current


code_classes = {
    "o": 111,
    "dot": 46,
    "pipe": 124,
    "other": 32,
}
current_classes = (4, 0, 1, 2, 5)
accumulator = (7, 8)
checked = 0
for code_name, code in code_classes.items():
    for current in current_classes:
        source = source_step(accumulator, code, current)
        summary = proof_summary_step(accumulator, code, current)
        assert source == summary
        checked += 1
        print(
            f"class={code_name:5s} current={current} "
            f"result={source[0]} next_current={source[1]}"
        )
print(f"partitions_checked={checked} mismatches=0")
