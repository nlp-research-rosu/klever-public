#!/usr/bin/env python3
"""Append reviewer-authored assertions to the trusted regeneration of solution.mpy."""

from pathlib import Path


SOURCE = Path("/tmp/audit-work/105-by-length/solution.regenerated.mpy")
TARGET = Path("/tmp/audit-work/105-by-length/reviewer-concrete-tests.mpy")

NAMES = {
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
}

CASES = [
    [2, 1, 1, 4, 5, 8, 2, 3],
    [],
    [1, -1, 55],
    [0, 1, 9, 10],
    [9, 9, 1, 1, 0, 10],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [10**20, 9, -(10**20), 1],
]


def integer(value: int) -> str:
    return f'UnaryOp("-", Int({-value}))' if value < 0 else f"Int({value})"


def integer_list(values: list[int]) -> str:
    return "ListExpr(" + ", ".join(integer(value) for value in values) + ")"


def string_list(values: list[str]) -> str:
    return "ListExpr(" + ", ".join(f'Str("{value}")' for value in values) + ")"


def expected(values: list[int]) -> list[str]:
    return [NAMES[value] for value in sorted(values, reverse=True) if 1 <= value <= 9]


def main() -> None:
    program = SOURCE.read_text(encoding="utf-8").rstrip()
    if not program.startswith("Module(") or not program.endswith(")"):
        raise SystemExit("regenerated program is not a Module term")
    assertions = [
        "Assert(Compare("
        f'Call(Name("by_length"), {integer_list(values)}), '
        f'CmpOp("==", {string_list(expected(values))})))'
        for values in CASES
    ]
    TARGET.write_text(
        program[:-1] + "\n  " + "\n  ".join(assertions) + ")\n",
        encoding="utf-8",
    )
    print(f"source={SOURCE}")
    print(f"target={TARGET}")
    print(f"case_count={len(CASES)}")
    for values in CASES:
        print(f"{values!r} -> {expected(values)!r}")


if __name__ == "__main__":
    main()
