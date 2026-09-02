#!/usr/bin/env python3
"""Mechanical source/constructor/entry-claim pinning checks."""

from __future__ import annotations

import ast
import importlib.util
import json
import re
from pathlib import Path


WORK = Path("/tmp/audit-work/candidate-src")
EVIDENCE = Path("/audit-output/evidence/04-adequacy")


def squash(text: str) -> str:
    return re.sub(r"\s+", "", text)


def balanced_term(text: str, start: int) -> str:
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start:index + 1]
    raise AssertionError("unbalanced constructor term")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


solution_mpy = (WORK / "solution.mpy").read_text()
regenerated_mpy = (WORK / "regenerated-solution.mpy").read_text()
spec_text = (WORK / "spec.k").read_text()
verification_text = (WORK / "verification.k").read_text()
solution_source = (WORK / "solution.py").read_text()

assert solution_mpy == regenerated_mpy
load_start = spec_text.index("Module(", spec_text.index("#loadAll("))
claim_module = balanced_term(spec_text, load_start)
assert squash(claim_module) == squash(solution_mpy)

constructors = re.findall(r"\b([A-Z][A-Za-z0-9_]*)\s*\(", solution_mpy)
assert constructors == [
    "Module",
    "FuncDef",
    "Params",
    "Return",
    "BinOp",
    "Name",
    "Name",
]
assert 'Call(Name("car_race_collision"),Int(N:Int))' in squash(
    spec_text
)
assert "=>N*IntN" in squash(spec_text)
claim_text = spec_text[spec_text.index("claim [car-race-collision]:"):]
assert not re.search(r"(?m)^\s+requires\b", claim_text)

local_sentences = re.findall(
    r"(?m)^\s*(syntax|rule|claim|context|configuration)\b",
    verification_text,
)
assert local_sentences == []
assert 'imports MPY' in verification_text

solution_ast = ast.parse(solution_source)
function = solution_ast.body[0]
assert isinstance(function, ast.FunctionDef)
assert function.name == "car_race_collision"
assert [arg.arg for arg in function.args.args] == ["n"]
assert ast.dump(
    function.body[0],
    include_attributes=False,
) == (
    "Return(value=BinOp(left=Name(id='n', ctx=Load()), op=Mult(), "
    "right=Name(id='n', ctx=Load())))"
)

canonical = load(Path("/reference/canonical.py"), "canonical_for_pinning")
candidate = load(WORK / "solution.py", "candidate_for_pinning")
witness_n = 3
canonical_result = canonical.car_race_collision(witness_n)
candidate_result = candidate.car_race_collision(witness_n)
formal_result = witness_n * witness_n
assert canonical_result == candidate_result == formal_result == 9

state = {
    "substitution": {"N:Int": witness_n},
    "k": (
        "#loadAll(Module(FuncDef(\"car_race_collision\", Params(\"n\"), "
        "Return(BinOp(\"*\", Name(\"n\"), Name(\"n\")))))) "
        "~> Call(Name(\"car_race_collision\"), Int(3))"
    ),
    "env": 0,
    "scopes": {
        "0": "scope(.Map, parent(-1))",
        "-1": "builtinsScope",
    },
    "scopeLoc": 1,
    "heap": ".Map",
    "heapLoc": 0,
    "stack": ".List",
    "ret": "noRet",
    "exc": "NoExc",
    "exit-code": 0,
    "expected_k_result": 9,
    "canonical_python_result": canonical_result,
    "candidate_python_result": candidate_result,
}
(EVIDENCE / "satisfying_state.json").write_text(
    json.dumps(state, indent=2, sort_keys=True) + "\n"
)

print("trusted_regeneration_byte_equal: True")
print("claim_module_constructor_equal: True")
print("solution_constructors:", ",".join(constructors))
print("entry_call_pinned: car_race_collision(Int(N:Int))")
print("formal_domain: all K Int (no requires clause)")
print("postcondition: returned K item equals N *Int N")
print("verification_local_sentences:", len(local_sentences))
print("satisfying_witness_N:", witness_n)
print("canonical_result:", canonical_result)
print("candidate_result:", candidate_result)
print("formal_result:", formal_result)
print("PINNING_CHECK: PASS")
