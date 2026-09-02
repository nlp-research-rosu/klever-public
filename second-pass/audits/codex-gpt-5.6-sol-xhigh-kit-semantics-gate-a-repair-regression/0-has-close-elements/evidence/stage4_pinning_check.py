#!/usr/bin/env python3
"""Check proof macros against constructor trees emitted by the trusted translator."""

from __future__ import annotations

import ast
import importlib.util
import re
from pathlib import Path


TRANSLATOR = Path("/reference/py2mpy.py")
SOLUTION = Path("/tmp/audit-work/reconstruction/solution.py")
VERIFICATION = Path("/tmp/audit-work/reconstruction/verification.k")


def load_translator():
    spec = importlib.util.spec_from_file_location("trusted_py2mpy_for_pinning", TRANSLATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(TRANSLATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalized(text: str) -> str:
    # Empty generated statement sequences parse as .Stmts; the proof spells
    # that list unit explicitly.
    return re.sub(r"\s+", "", text).replace(".Stmts", "")


def macro_rhs(source: str, name: str, following: str) -> str:
    pattern = rf"rule\s+{re.escape(name)}\s*=>\s*(.*?)(?=\n\s*{following})"
    match = re.search(pattern, source, flags=re.DOTALL)
    if match is None:
        raise RuntimeError(f"cannot extract macro {name}")
    return match.group(1).strip()


def main() -> int:
    tr = load_translator()
    module_tree = tr.emit_module(ast.parse(SOLUTION.read_text(encoding="utf-8")))
    statements = module_tree.args[0].items
    if [stmt.name for stmt in statements] != ["ImportFrom", "FuncDef"]:
        raise RuntimeError("unexpected module statement structure")
    func = statements[1]
    func_name, params_node, body = func.args
    if func_name != '"has_close_elements"' or params_node.name != "Params":
        raise RuntimeError("unexpected function identity")
    params = "(" + ",".join(params_node.args) + ")"

    assigns = body.items[:3]
    outer_while = body.items[3]
    final_return = body.items[4]
    outer_condition, outer_body = outer_while.args
    outer_assign_j, inner_while, outer_increment_i = outer_body.items
    inner_condition, inner_body = inner_while.args

    expected_target = (
        f"closureVal({params},{tr.render(body)},0)"
    )
    expected_outer = (
        f"#while({tr.render(outer_condition)},{tr.render(outer_body)})"
        f"~>{tr.render(final_return)}~>#endcall"
    )
    expected_inner = (
        f"#while({tr.render(inner_condition)},{tr.render(inner_body)})"
        f"~>{tr.render(outer_increment_i)}"
        f"~>#loopLbl(#while({tr.render(outer_condition)},{tr.render(outer_body)}))"
        f"~>{tr.render(final_return)}~>#endcall"
    )

    source = VERIFICATION.read_text(encoding="utf-8")
    actual_target = macro_rhs(source, "targetClosure", "syntax K ::= \"innerRun\"")
    actual_inner = macro_rhs(source, "innerRun", "syntax K ::= \"outerRun\"")
    actual_outer = macro_rhs(source, "outerRun", "endmodule")

    comparisons = [
        ("targetClosure", expected_target, actual_target),
        ("innerRun", expected_inner, actual_inner),
        ("outerRun", expected_outer, actual_outer),
    ]
    print(f"translator={TRANSLATOR}")
    print(f"solution={SOLUTION}")
    print(f"verification={VERIFICATION}")
    print("module_statements=ImportFrom,FuncDef")
    print("body_statements=Assign(i),Assign(j),Assign(n),While(i<n),Return(false)")
    print(
        "outer_body=Assign(j=i+1),While(j<n),AugAssign(i+=1); "
        "inner_body=If(close:return true),AugAssign(j+=1)"
    )
    failed = False
    for name, expected, actual in comparisons:
        match = normalized(expected) == normalized(actual)
        print(f"{name}_normalized_constructor_identity={match}")
        if not match:
            failed = True
            print(f"{name}_expected={normalized(expected)}")
            print(f"{name}_actual={normalized(actual)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
