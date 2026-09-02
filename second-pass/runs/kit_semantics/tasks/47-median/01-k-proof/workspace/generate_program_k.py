#!/usr/bin/env python3
"""Generate the proof's exact closure value from solution.py."""

from __future__ import annotations

import ast
import re
import symtable
import sys
from pathlib import Path

import py2mpy


def main() -> int:
    if not 2 <= len(sys.argv) <= 4:
        raise SystemExit(
            "usage: generate_program_k.py SOLUTION.py [MODULE [SYMBOL]]"
        )

    source_path = Path(sys.argv[1])
    module_name = sys.argv[2] if len(sys.argv) >= 3 else "MEDIAN-PROGRAM"
    symbol_name = (
        sys.argv[3] if len(sys.argv) >= 4 else "solutionMedianClosure"
    )
    if not re.fullmatch(r"[A-Z][A-Z0-9-]*", module_name):
        raise SystemExit("invalid K module name")
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9-]*", symbol_name):
        raise SystemExit("invalid K symbol name")

    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(source_path))

    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
        raise SystemExit("solution.py must contain exactly one function definition")
    function = tree.body[0]
    if function.name != "median":
        raise SystemExit("solution.py must define median")

    py2mpy.SCOPES.clear()
    py2mpy._walk_symtable(symtable.symtable(source, str(source_path), "exec"))
    term = py2mpy.emit_stmt(function)
    if term.name != "FuncDef" or len(term.args) != 3:
        raise SystemExit("median must remain a capture-free function")

    params = term.args[1]
    body = term.args[2]
    if params.name != "Params" or len(params.args) != 1:
        raise SystemExit("median must retain its one-argument signature")

    param_text = py2mpy.render(params.args[0])
    body_text = py2mpy.render(body, 2)
    indented_body = "\n".join("      " + line for line in body_text.splitlines())

    print('requires "reference-semantics/semantics.k"')
    print()
    print(f"module {module_name}")
    print("  imports MPY")
    print()
    print(f'  syntax Val ::= "{symbol_name}" [function, total]')
    print(f"  rule {symbol_name}")
    print("    => closureVal(")
    print(f"      {param_text},")
    print(indented_body + ",")
    print("      0)")
    print("endmodule")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
