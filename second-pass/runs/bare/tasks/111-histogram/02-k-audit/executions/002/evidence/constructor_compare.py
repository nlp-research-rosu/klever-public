#!/usr/bin/env python3
"""Compare submitted/translated program trees at CPython-AST and K-constructor level."""

from __future__ import annotations

import ast
import subprocess
from pathlib import Path


fresh = Path("/tmp/audit-work/fresh")
regenerated = subprocess.run(
    ["python3", "/reference/py2mpy.py", str(fresh / "solution.py")],
    check=True,
    stdout=subprocess.PIPE,
).stdout
submitted = (fresh / "solution.mpy").read_bytes()
print(f"trusted_regeneration_byte_identity={regenerated == submitted}")
print(f"regenerated_bytes={len(regenerated)} submitted_bytes={len(submitted)}")
if regenerated != submitted:
    raise SystemExit(1)

solution_tree = ast.parse((fresh / "solution.py").read_text())
function = solution_tree.body[0]
assert isinstance(function, ast.FunctionDef)
print(f"python_entry_name={function.name}")
print(f"python_entry_parameters={[arg.arg for arg in function.args.args]}")
print(f"python_body_statement_types={[type(stmt).__name__ for stmt in function.body]}")

verification = (fresh / "verification.k").read_text()
prefix = "rule histogramProgram() =>"
suffix = "// Denotational"
if prefix not in verification or suffix not in verification:
    print("histogram_program_constructor_extracted=False")
    raise SystemExit(1)
constructor = verification.split(prefix, 1)[1].split(suffix, 1)[0].strip()
normalized_constructor = "".join(constructor.split())
normalized_submitted = "".join(submitted.decode().split())
normalizations = (
    (
        'Call(Attribute(Name("test"),"split"),)',
        'Call(Attribute(Name("test"),"split"),.Exprs)',
    ),
    ("DictExpr()", "DictExpr(.Entries)"),
    (
        'Assign(Name("maximum"),Subscript(Name("counts"),Name("letter"))),))'
        'Assign(Name("result")',
        'Assign(Name("maximum"),Subscript(Name("counts"),Name("letter"))),.Stmts))'
        'Assign(Name("result")',
    ),
    (
        'Subscript(Name("counts"),Name("letter"))),))Return(Name("result"))))',
        'Subscript(Name("counts"),Name("letter"))),.Stmts))Return(Name("result"))))',
    ),
)
for old, new in normalizations:
    occurrences = normalized_submitted.count(old)
    print(f"normalization_occurrences[{old}]={occurrences}")
    if occurrences == 0:
        raise SystemExit(1)
    normalized_submitted = normalized_submitted.replace(old, new)
print("histogram_program_constructor_extracted=True")
print(f"constructor_level_identity={normalized_constructor == normalized_submitted}")
if normalized_constructor != normalized_submitted:
    print(f"verification_constructor={normalized_constructor}")
    print(f"submitted_constructor={normalized_submitted}")
    raise SystemExit(1)
