#!/usr/bin/env python3
"""Create an operational-sensitivity mutant that changes the proved helper body."""

from __future__ import annotations

import ast
import re
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/119-match-parens")

source_path = ROOT / "solution.py"
mutant_source_path = ROOT / "body-mutated.py"
mutant_mpy_path = ROOT / "body-mutated.mpy"
mutant_verification_path = ROOT / "verification-body-mutated.k"
mutant_spec_path = ROOT / "spec-body-mutated.k"

tree = ast.parse(source_path.read_text(), filename=str(source_path))
changed = False
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "is_good":
        node.body = [ast.Return(value=ast.Constant(value=""))]
        changed = True
if not changed:
    raise RuntimeError("is_good function not found")
ast.fix_missing_locations(tree)
mutant_source_path.write_text(ast.unparse(tree) + "\n")

translated = subprocess.run(
    ["python3", str(ROOT / "py2mpy.py"), str(mutant_source_path)],
    check=True,
    capture_output=True,
    text=True,
).stdout
mutant_mpy_path.write_text(translated)

verification = (ROOT / "verification.k").read_text()
verification = verification.replace(
    "module MATCH-PARENS-VERIFICATION\n",
    "module MATCH-PARENS-VERIFICATION-BODY-MUTATED\n",
    1,
)
pattern = re.compile(
    r'  syntax Stmts ::= "isGoodBody" \[function\]\n'
    r"  rule isGoodBody\n"
    r".*?"
    r'(?=\n  syntax Stmts ::= "matchParensBody" \[function\])',
    re.DOTALL,
)
replacement = (
    '  syntax Stmts ::= "isGoodBody" [function]\n'
    '  rule isGoodBody => Return(Str("")) .Stmts\n'
)
verification, count = pattern.subn(replacement, verification)
if count != 1:
    raise RuntimeError(f"expected one isGoodBody replacement, got {count}")
mutant_verification_path.write_text(verification)

spec = (ROOT / "spec.k").read_text()
spec = spec.replace(
    'requires "verification.k"',
    'requires "verification-body-mutated.k"',
    1,
)
spec = spec.replace(
    "module MATCH-PARENS-SPEC\n",
    "module MATCH-PARENS-SPEC-BODY-MUTATED\n",
    1,
)
spec = spec.replace(
    "imports MATCH-PARENS-VERIFICATION\n",
    "imports MATCH-PARENS-VERIFICATION-BODY-MUTATED\n",
    1,
)
mutant_spec_path.write_text(spec)

print(f"mutant_source={mutant_source_path}")
print(f"mutant_mpy={mutant_mpy_path}")
print(f"mutant_verification={mutant_verification_path}")
print(f"mutant_spec={mutant_spec_path}")
print("mutation=is_good body is now exactly Return(Str(\"\"))")
