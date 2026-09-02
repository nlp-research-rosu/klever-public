#!/usr/bin/env python3
"""Embed a translated .mpy term as a nullary K function for proofs."""

from pathlib import Path
import sys


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: embed_mpy.py FILE.mpy")
    program = Path(sys.argv[1]).read_text(encoding="utf-8").strip()
    print('requires "semantic.k"')
    print()
    print("module SOLUTION")
    print("  imports MPY")
    print('  syntax Program ::= "solutionProgram" [function]')
    print(f"  rule solutionProgram => {program}")
    print("endmodule")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
