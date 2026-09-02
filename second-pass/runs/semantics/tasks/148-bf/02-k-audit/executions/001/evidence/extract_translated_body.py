#!/usr/bin/env python3
"""Render the translated body of the candidate's sole top-level function."""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path


TRANSLATOR = Path("/reference/py2mpy.py")
SOLUTION = Path("/candidate/solution.py")


def main() -> None:
    module_spec = importlib.util.spec_from_file_location(
        "trusted_py2mpy_for_audit", TRANSLATOR
    )
    assert module_spec is not None and module_spec.loader is not None
    translator = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(translator)

    tree = ast.parse(SOLUTION.read_text(), filename=str(SOLUTION))
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    assert len(functions) == 1
    function = functions[0]
    assert function.name == "bf"
    print(translator.render(translator.emit_stmts(function.body)))


if __name__ == "__main__":
    main()
