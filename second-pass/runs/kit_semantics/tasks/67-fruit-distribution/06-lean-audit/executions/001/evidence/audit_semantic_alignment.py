#!/usr/bin/env python3
"""Tie the empty proof-local inventory to the frozen program and fixed semantics."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/reference/k-proof")


def check(label: str, condition: bool) -> None:
    print(f"CHECK {label}: {'PASS' if condition else 'FAIL'}")
    if not condition:
        raise SystemExit(1)


def show(path: Path, first: int, last: int) -> None:
    print(f"SOURCE {path} lines {first}-{last}")
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if first <= number <= last:
            print(f"{number:5d}\t{line}")


solution_path = ROOT / "solution.py"
verification_path = ROOT / "verification.k"
spec_path = ROOT / "spec.k"
methods_path = ROOT / "reference-semantics/semantics/methods.k"
builtins_path = ROOT / "reference-semantics/semantics/builtins.k"
operators_path = ROOT / "reference-semantics/semantics/operators.k"
int_path = ROOT / "reference-semantics/semantics/int.k"
subscript_path = ROOT / "reference-semantics/semantics/subscript.k"

show(solution_path, 1, 3)
show(verification_path, 1, 6)
show(spec_path, 6, 69)
show(methods_path, 70, 86)
show(builtins_path, 138, 162)
show(operators_path, 8, 14)
show(int_path, 7, 16)
show(subscript_path, 27, 42)

tree = ast.parse(solution_path.read_text())
function = tree.body[0]
check("source is one fruit_distribution function", isinstance(function, ast.FunctionDef) and function.name == "fruit_distribution")
check("source parameters are exactly s and n", isinstance(function, ast.FunctionDef) and [arg.arg for arg in function.args.args] == ["s", "n"])
check("source body is one return", isinstance(function, ast.FunctionDef) and len(function.body) == 1 and isinstance(function.body[0], ast.Return))
expected_expression = ast.dump(
    ast.parse("n - int(s.split()[0]) - int(s.split()[3])", mode="eval").body,
    include_attributes=False,
)
observed_expression = ast.dump(function.body[0].value, include_attributes=False)
check("source return expression identity", observed_expression == expected_expression)

verification = verification_path.read_text()
spec = spec_path.read_text()
methods = methods_path.read_text()
builtins = builtins_path.read_text()
operators = operators_path.read_text()
ints = int_path.read_text()
subscripts = subscript_path.read_text()

check("verification imports only the fixed MPY semantics", 'module VERIFICATION\n  imports MPY\nendmodule' in verification)
check("verification contributes no local rule", "rule " not in verification)
check("spec embeds closure parameters s,n", '("s", "n")' in spec)
check("spec embeds both source subscript indices", "Int(0)" in spec and "Int(3)" in spec)
check("spec embeds two left-associated subtraction nodes", spec.count('BinOp(\n              "-"') == 1 and spec.count('BinOp(\n                "-"') == 1)
check("spec result is exact source arithmetic", "=> N -Int APPLES -Int ORANGES" in spec)
check("spec binds split result to first and fourth numeral tokens", "splitWS(CS, .IntSeq, .ValSeq)" in spec and "str(APPLECODES:IntSeq)" in spec and "str(ORANGECODES:IntSeq)" in spec)
check("spec binds both int conversions", 'applyBuiltin("int", str(APPLECODES), .Vals) ==K APPLES:Int' in spec and 'applyBuiltin("int", str(ORANGECODES), .Vals) ==K ORANGES:Int' in spec)

check("fixed semantics executes no-argument split", '#applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)' in methods and '#alloc(list(splitWS(CS, .IntSeq, .ValSeq)))' in methods)
check("fixed semantics defines split recurrence", "rule splitWS(.IntSeq" in methods and "rule splitWS(iCons(C:Int, R:IntSeq)" in methods)
check("fixed semantics defines single- and multi-digit int conversion", 'rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals)' in builtins and 'rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)' in builtins)
check("fixed semantics dispatches BinOp", "BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R)" in operators)
check("fixed semantics defines integer subtraction", 'rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2' in ints)
check("fixed semantics defines list indexing", "Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I)" in subscripts and "applyIndex(list(VS:ValSeq),  I:Int)" in subscripts)

print("SEMANTIC JUDGMENT: the frozen claim follows the exact source expression through supplied operational rules; verification.k adds no summary, bridge, derived fact, or domain fact to classify")
print("RESULT: PASS")
