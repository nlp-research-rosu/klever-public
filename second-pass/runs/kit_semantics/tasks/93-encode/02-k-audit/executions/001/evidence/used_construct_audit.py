#!/usr/bin/env python3
"""Mechanical checks supporting the focused reachable-rule review."""

from __future__ import annotations

import re
from pathlib import Path


solution = Path("/candidate/solution.mpy").read_text(encoding="utf-8")
spec = Path("/candidate/spec.k").read_text(encoding="utf-8")
verification = Path("/candidate/verification.k").read_text(encoding="utf-8")
semantics_files = sorted(Path("/reference/reference-semantics").rglob("*.k"))
semantics = "\n".join(path.read_text(encoding="utf-8") for path in semantics_files)

constructors = sorted(set(re.findall(r"\b([A-Z][A-Za-z0-9]*)\s*\(", solution)))
expected = ["Attribute", "Call", "FuncDef", "Module", "Name", "Params", "Return", "Str"]
assert constructors == expected
print(f"solution_constructors={constructors}")

local_syntax = re.findall(r"^\s*syntax\b", verification, flags=re.MULTILINE)
local_rules = re.findall(r"^\s*rule\b", verification, flags=re.MULTILINE)
local_claims = re.findall(r"^\s*claim\b", verification, flags=re.MULTILINE)
spec_claims = re.findall(r"^\s*claim\b", spec, flags=re.MULTILINE)
print(f"verification_local_syntax={len(local_syntax)}")
print(f"verification_local_rules={len(local_rules)}")
print(f"verification_local_claims={len(local_claims)}")
print(f"spec_target_claims={len(spec_claims)}")
assert not local_syntax and not local_rules and not local_claims
assert len(spec_claims) == 1

opaque_names: list[str] = []
opaque_pattern = re.compile(
    r"^\s*syntax\s+\w+\s*::=\s*([A-Za-z][A-Za-z0-9-]*)\s*\([^\n]*"
    r"\[[^\n]*no-evaluators[^\n]*\]",
    flags=re.MULTILINE,
)
for match in opaque_pattern.finditer(semantics):
    opaque_names.append(match.group(1))
opaque_names = sorted(set(opaque_names))
assert len(opaque_names) == 22
opaque_hits = [name for name in opaque_names if re.search(rf"\b{re.escape(name)}\s*\(", solution + spec)]
print(f"opaque_symbols={opaque_names}")
print(f"opaque_symbols_in_solution_or_spec={opaque_hits}")
assert not opaque_hits

required_snippets = {
    "module/load": ("semantics/core.k", "#loadAll(Module(SS:Stmts))"),
    "function definition": ("semantics/functions.k", "FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts)"),
    "name lookup": ("semantics/core.k", "Name(X:String) => #look(X, L)"),
    "call evaluation": ("semantics/call.k", "Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS)"),
    "argument order": ("semantics/core.k", "#evalArgs((A:Expr, REST:Exprs), ACC:Vals"),
    "closure call": ("semantics/call.k", "#applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int))"),
    "parameter binding": ("semantics/functions.k", "#bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))"),
    "attribute cooling": ("semantics/call.k", "Attribute(V:Val, M:String) => boundMethodV(V, M)"),
    "method dispatch": ("semantics/call.k", "#applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals)"),
    "ASCII literal": ("semantics/str.k", "Str(S:String) => str(strToCodes(S))"),
    "swapcase": ("semantics/methods.k", 'applyMethod(str(CS:IntSeq), "swapcase", .Vals)'),
    "mapSwap": ("semantics/methods.k", "mapSwap(iCons(C:Int, S:IntSeq))"),
    "swapC": ("semantics/methods.k", "swapC(C:Int) => C +Int 32"),
    "replace": ("semantics/methods.k", 'applyMethod(str(CS:IntSeq), "replace"'),
    "replaceC": ("semantics/methods.k", "replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int)"),
    "return": ("semantics/functions.k", "Return(V:Val) ~> _ => #pop"),
    "frame pop": ("semantics/functions.k", "#pop => V ~> CONT"),
}

for role, (relative, snippet) in required_snippets.items():
    path = Path("/reference/reference-semantics") / relative
    text = path.read_text(encoding="utf-8")
    assert snippet in text, (role, path, snippet)
    line = text[: text.index(snippet)].count("\n") + 1
    print(f"{role}: {path}:{line}: {snippet}")

print("USED_CONSTRUCT_AUDIT=PASS")
