#!/usr/bin/env python3
"""Check that program.k embeds exactly the constructor term in solution.mpy."""

from pathlib import Path
import re
import sys


def expected_program_module(mpy_text):
    # Empty statement lists have no surface text in a standalone .mpy file.
    # K's inner rule parser requires their generated unit constructor.
    inner_term = re.sub(r"(?m)^(\s*)\)(,?)$", r"\1.Stmts)\2", mpy_text.rstrip())
    indented = "\n".join("    " + line for line in inner_term.splitlines())
    return (
        'module SOLUTION-PROGRAM\n'
        '  imports MPY-SYNTAX\n'
        '  syntax Module ::= "solutionProgram" [function]\n'
        '  rule solutionProgram =>\n'
        f'{indented}\n'
        'endmodule\n'
    )


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: check_program_module.py solution.mpy program.k")
    mpy_path, module_path = map(Path, sys.argv[1:])
    expected = expected_program_module(mpy_path.read_text(encoding="utf-8"))
    actual = module_path.read_text(encoding="utf-8")
    if actual != expected:
        raise SystemExit(f"{module_path} is not generated from {mpy_path}")


if __name__ == "__main__":
    main()
