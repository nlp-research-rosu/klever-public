#!/usr/bin/env python3
"""Append concrete assertions to the exact submitted Module term."""

from __future__ import annotations

import sys
from pathlib import Path


CASES = [
    (5, 6, 10, 11, 4),
    (4, 8, 9, 12, 1),
    (1, 10, 10, 11, 0),
    (2, 11, 5, 7, 0),
    (0, 0, 0, 0, 0),
    (1000, 0, 0, 1000, 0),
    (0, 1000, 1000, 1000, 0),
    (1000, 1000, 1000, 2000, 0),
    (37, 500, 499, 536, 0),
    (37, 500, 500, 537, 0),
    (37, 500, 501, 537, 1),
]


def assertion(case: tuple[int, int, int, int, int]) -> str:
    number, need, remaining, total, left = case
    return (
        "\n  Assert(Compare("
        f"Call(Name(\"eat\"), Int({number}), Int({need}), Int({remaining})), "
        f"CmpOp(\"==\", ListExpr(Int({total}), Int({left})))))"
    )


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {Path(sys.argv[0]).name} SOLUTION.mpy OUTPUT.mpy")
        return 2
    source = Path(sys.argv[1]).read_text(encoding="utf-8")
    stripped = source.rstrip()
    if not stripped.startswith("Module(") or not stripped.endswith(")"):
        raise ValueError("submitted term is not a single outer Module constructor")
    harness = stripped[:-1] + "".join(assertion(case) for case in CASES) + ")\n"
    Path(sys.argv[2]).write_text(harness, encoding="utf-8")
    print(f"source={sys.argv[1]}")
    print(f"output={sys.argv[2]}")
    print(f"assertions={len(CASES)}")
    print("submitted_module_prefix_preserved=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
