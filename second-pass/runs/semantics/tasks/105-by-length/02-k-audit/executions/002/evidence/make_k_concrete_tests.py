#!/usr/bin/env python3
"""Build independent fixed-semantics assertions around regenerated solution.mpy."""

from pathlib import Path


SCRATCH = Path("/tmp/audit-work/105-by-length/recon")
CASES = [
    (
        [2, 1, 1, 4, 5, 8, 2, 3],
        ["Eight", "Five", "Four", "Three", "Two", "Two", "One", "One"],
    ),
    ([], []),
    ([1, -1, 55], ["One"]),
    ([0, 1, 9, 10], ["Nine", "One"]),
    (list(range(1, 10)), [
        "Nine", "Eight", "Seven", "Six", "Five",
        "Four", "Three", "Two", "One",
    ]),
    ([9, 9, 1, 1, -1000000, 1000000], ["Nine", "Nine", "One", "One"]),
    ([5, 2, 8, 3, 5], ["Eight", "Five", "Five", "Three", "Two"]),
]


def integer(value: int) -> str:
    if value < 0:
        return f'UnaryOp("-", Int({-value}))'
    return f"Int({value})"


def integers(values: list[int]) -> str:
    return "ListExpr(" + ", ".join(integer(value) for value in values) + ")"


def strings(values: list[str]) -> str:
    return "ListExpr(" + ", ".join(f'Str("{value}")' for value in values) + ")"


program = (SCRATCH / "regenerated-solution.mpy").read_text(
    encoding="utf-8"
).rstrip()
assert program.startswith("Module(") and program.endswith(")")
assertions = [
    "Assert(Compare("
    f'Call(Name("by_length"), {integers(arguments)}), '
    f'CmpOp("==", {strings(expected)})))'
    for arguments, expected in CASES
]
(SCRATCH / "audit-concrete.mpy").write_text(
    program[:-1] + "\n  " + "\n  ".join(assertions) + ")\n",
    encoding="utf-8",
)
print(f"WROTE: {SCRATCH / 'audit-concrete.mpy'}")
print(f"ASSERTION_COUNT: {len(assertions)}")
