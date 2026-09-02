"""Mechanical source-to-claim pinning checks for the fibfib entry theorem."""

from __future__ import annotations

import ast
import importlib.util
import re
from pathlib import Path


WORK = Path("/tmp/audit-work")


def balanced_argument(text: str, marker: str) -> str:
    start = text.index(marker) + len(marker)
    if text[start] != "(":
        raise AssertionError("marker is not immediately followed by '('")
    depth = 0
    quote = None
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {'"', "'"}:
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start + 1 : index]
    raise AssertionError("unbalanced marker")


def constructor_normal_form(text: str) -> str:
    # `.Stmts` is the explicit unit of K's Stmts list.  The trusted translator
    # omits it where the hand-written claim spells it out.
    return re.sub(r"\s+", "", text).replace(".Stmts", "")


def load_function(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fibfib


spec_text = (WORK / "spec.k").read_text(encoding="utf-8")
solution_term = (WORK / "solution.mpy").read_text(encoding="utf-8")
loaded_term = balanced_argument(spec_text, "#loadAll")

solution_nf = constructor_normal_form(solution_term)
loaded_nf = constructor_normal_form(loaded_term)
assert solution_nf == loaded_nf
assert spec_text.count("#loadAll(") == 1

solution_ast = ast.parse((WORK / "solution.py").read_text(encoding="utf-8"))
concrete_ast = ast.parse((WORK / "concrete_audit.py").read_text(encoding="utf-8"))
assert ast.dump(solution_ast.body[0], include_attributes=False) == ast.dump(
    concrete_ast.body[0], include_attributes=False
)

canonical = load_function("pin_canonical", WORK / "canonical.py")
generated = load_function("pin_generated", WORK / "solution.py")

print("entry_load_occurrences: 1")
print("constructor_normal_form_equal: true")
print(f"constructor_normal_form_length: {len(solution_nf)}")
print("only_normalization: whitespace plus explicit .Stmts list units")
print("concrete_harness_function_ast_equal: true")
print("satisfying_precondition_witnesses:")
for n in (0, 1, 2, 3, 5, 8):
    expected = canonical(n)
    actual = generated(n)
    assert expected == actual
    print(
        f"  N={n}: N>=0=true; fibfibSpec={expected}; "
        f"canonical={expected}; generated={actual}"
    )
