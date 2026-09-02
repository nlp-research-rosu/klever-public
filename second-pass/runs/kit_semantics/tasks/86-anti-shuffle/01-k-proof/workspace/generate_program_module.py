#!/usr/bin/env python3
"""Generate K aliases for the exact translated solution module and body."""

import argparse
import ast
import hashlib
import re
import symtable
from pathlib import Path

import py2mpy


def indent(text, spaces):
    pad = " " * spaces
    return "\n".join(pad + line if line else line for line in text.splitlines())


def explicit_empty_stmts(text):
    """Spell blank trailing Stmts arguments explicitly inside K rules."""
    return re.sub(r",\n(?P<pad>[ \t]*)\)", r",\n\g<pad>.Stmts)", text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="solution.py")
    parser.add_argument("--output", default="program-generated.k")
    args = parser.parse_args()

    input_path = Path(args.input)
    source = input_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(input_path))

    py2mpy.SCOPES.clear()
    py2mpy._walk_symtable(symtable.symtable(source, str(input_path), "exec"))

    targets = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "anti_shuffle"
    ]
    if len(targets) != 1:
        raise SystemExit("solution.py must define exactly one top-level anti_shuffle")

    module_term = explicit_empty_stmts(
        py2mpy.render(py2mpy.emit_module(tree))
    )
    body_term = explicit_empty_stmts(
        py2mpy.render(py2mpy.emit_stmts(targets[0].body))
    )
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()

    generated = f'''// Generated from {input_path.name}; sha256={digest}
// Regenerate with: python3 generate_program_module.py
requires "reference-semantics/semantics.k"

module PROGRAM-GENERATED
  imports MPY

  syntax Module ::= solutionModule() [function, total]
  rule solutionModule()
    =>
{indent(module_term, 6)}

  syntax Stmts ::= solutionBody() [function, total]
  rule solutionBody()
    =>
{indent(body_term, 6)}
endmodule
'''
    Path(args.output).write_text(generated, encoding="utf-8")


if __name__ == "__main__":
    main()
