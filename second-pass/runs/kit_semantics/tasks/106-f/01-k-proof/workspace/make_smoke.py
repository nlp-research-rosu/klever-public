#!/usr/bin/env python3
"""Append a concrete call to solution.py's AST and emit one .mpy program."""

import ast
import sys

import py2mpy


def main():
    n = int(sys.argv[1])
    source = open("solution.py", encoding="utf-8").read()
    tree = ast.parse(source, filename="solution.py")
    tree.body.append(
        ast.Assign(
            targets=[ast.Name(id="answer", ctx=ast.Store())],
            value=ast.Call(
                func=ast.Name(id="f", ctx=ast.Load()),
                args=[ast.Constant(value=n)],
                keywords=[],
            ),
        )
    )
    ast.fix_missing_locations(tree)
    py2mpy.SCOPES.clear()
    py2mpy._walk_symtable(symtable_for(source))
    print(py2mpy.render(py2mpy.emit_module(tree)))


def symtable_for(source):
    import symtable

    return symtable.symtable(source, "solution.py", "exec")


if __name__ == "__main__":
    main()
