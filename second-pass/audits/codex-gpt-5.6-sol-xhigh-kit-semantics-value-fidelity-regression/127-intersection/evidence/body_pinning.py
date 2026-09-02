#!/usr/bin/env python3
"""Independently pin the proof closure to the trusted translation's exact body."""

from __future__ import annotations

import ast
import importlib.util
import re
import symtable
from pathlib import Path


def load_translator(path: Path):
    spec = importlib.util.spec_from_file_location("trusted_translator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


root = Path("/tmp/audit-work/127-intersection")
translator = load_translator(Path("/reference/py2mpy.py"))
source = (root / "solution.py").read_text(encoding="utf-8")
tree = ast.parse(source, filename="solution.py")
translator.SCOPES.clear()
translator._walk_symtable(symtable.symtable(source, "solution.py", "exec"))

regenerated = translator.render(translator.emit_module(tree)) + "\n"
submitted = (root / "solution.mpy").read_text(encoding="utf-8")
assert regenerated == submitted

assert len(tree.body) == 1 and isinstance(tree.body[0], ast.FunctionDef)
function_term = translator.emit_stmt(tree.body[0])
assert function_term.name == "FuncDef"
assert function_term.args[0] == '"intersection"'
assert translator.render(function_term.args[1]) == 'Params("interval1", "interval2")'
body = translator.render(function_term.args[-1])

verification = (root / "verification.k").read_text(encoding="utf-8")
match = re.search(
    r"rule\s+intersectionClosure\s*=>\s*(closureVal\(.*\))\s*endmodule",
    verification,
    flags=re.DOTALL,
)
assert match is not None

normalize = lambda value: re.sub(r"\s+", "", value)
# K spells an empty Stmts argument explicitly, while the translator renders an
# empty Seq as the empty field between a comma and a closing parenthesis.
normalized_body = normalize(body).replace(",)", ",.Stmts)")
expected_closure = (
    'closureVal(("interval1","interval2"),' + normalized_body + ",0)"
)
actual_closure = normalize(match.group(1))
assert actual_closure == expected_closure

print("trusted translation byte-equals submitted solution.mpy: YES")
print("proof parameter list exactly matches translated function: YES")
print("intersectionClosure body and defining environment exactly match: YES")
print(f"normalized body characters compared: {len(normalized_body)}")
