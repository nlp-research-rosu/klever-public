#!/usr/bin/env python3
"""Independently check the embedded K program against trusted translation.

This checker does not import or invoke the candidate's checker.  It constructs
the only expected SOLUTION-PROGRAM module from the freshly translated MPY term,
including explicit empty Stmts list units required by K's inner parser.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def expected_module(mpy_text: str) -> str:
    with_units = re.sub(r"(?m)^(\s*)\)(,?)$", r"\1.Stmts)\2", mpy_text.rstrip())
    body = "\n".join(f"    {line}" for line in with_units.splitlines())
    return (
        "module SOLUTION-PROGRAM\n"
        "  imports MPY-SYNTAX\n"
        '  syntax Module ::= "solutionProgram" [function]\n'
        "  rule solutionProgram =>\n"
        f"{body}\n"
        "endmodule\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fresh_mpy", type=Path)
    parser.add_argument("program_k", type=Path)
    args = parser.parse_args()
    expected = expected_module(args.fresh_mpy.read_text(encoding="utf-8"))
    actual = args.program_k.read_text(encoding="utf-8")
    print(f"fresh_mpy={args.fresh_mpy}")
    print(f"program_k={args.program_k}")
    print(f"byte_identical_expected_module={actual == expected}")
    if actual != expected:
        expected_path = args.program_k.with_name("reviewer-expected-program.k")
        expected_path.write_text(expected, encoding="utf-8")
        print(f"expected_written={expected_path}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
