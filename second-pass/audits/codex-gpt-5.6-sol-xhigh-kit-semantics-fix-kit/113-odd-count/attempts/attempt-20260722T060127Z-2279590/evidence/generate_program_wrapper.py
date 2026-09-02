#!/usr/bin/env python3
"""Independently wrap a trusted-translator MPY term as a nullary K program symbol."""

import argparse
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("source", nargs="?", default="/tmp/audit-work/113-odd-count/solution.regenerated.mpy")
parser.add_argument("token", nargs="?", default="solutionProgram")
parser.add_argument("module", nargs="?", default="SOLUTION-PROGRAM")
args = parser.parse_args()

source = Path(args.source)
program = source.read_text(encoding="utf-8")
if program.count("ListExpr()") != 1:
    raise SystemExit("expected exactly one empty list constructor in solution.mpy")
program = program.replace("ListExpr()", "ListExpr(.Exprs)")

print('requires "reference-semantics/semantics.k"')
print()
print(f"module {args.module}")
print("  imports MPY-SYNTAX")
print(f'  syntax Module ::= "{args.token}" [function, total]')
print(f"  rule {args.token} =>")
for line in program.splitlines():
    print("    " + line)
print("endmodule")
