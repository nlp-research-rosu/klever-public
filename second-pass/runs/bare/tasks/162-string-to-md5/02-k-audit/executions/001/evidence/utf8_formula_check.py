#!/usr/bin/env python3
"""Exhaustively check the candidate's four UTF-8 code-point equations."""

from __future__ import annotations

import sys


def candidate_formula(code_point: int) -> bytes:
    if 0 <= code_point <= 127:
        return bytes((code_point,))
    if code_point <= 2047:
        return bytes((192 | (code_point >> 6), 128 | (code_point & 63)))
    if code_point <= 65535:
        return bytes(
            (
                224 | (code_point >> 12),
                128 | ((code_point >> 6) & 63),
                128 | (code_point & 63),
            )
        )
    if code_point <= 1114111:
        return bytes(
            (
                240 | (code_point >> 18),
                128 | ((code_point >> 12) & 63),
                128 | ((code_point >> 6) & 63),
                128 | (code_point & 63),
            )
        )
    raise ValueError(code_point)


def main() -> int:
    scalar_mismatches: list[tuple[int, str, str]] = []
    surrogate_fabrications: list[tuple[int, str, str]] = []
    scalar_count = 0
    for code_point in range(0x110000):
        formula = candidate_formula(code_point)
        try:
            python = chr(code_point).encode("utf-8")
        except UnicodeEncodeError as error:
            surrogate_fabrications.append(
                (code_point, formula.hex(), type(error).__name__)
            )
            continue
        scalar_count += 1
        if formula != python:
            scalar_mismatches.append((code_point, formula.hex(), python.hex()))
    print(f"valid Unicode scalar values checked: {scalar_count}")
    print(f"scalar mismatches: {len(scalar_mismatches)}")
    print(f"surrogate values where formula fabricates bytes: {len(surrogate_fabrications)}")
    print("first surrogate witness:", surrogate_fabrications[0])
    print("last surrogate witness:", surrogate_fabrications[-1])
    print("sample scalar mismatches:", scalar_mismatches[:10])
    # Formula correctness on Unicode scalar values passes. Surrogate fabrication
    # is deliberately reported as a language-domain discrepancy, not hidden as
    # a scalar mismatch.
    return 1 if scalar_mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
