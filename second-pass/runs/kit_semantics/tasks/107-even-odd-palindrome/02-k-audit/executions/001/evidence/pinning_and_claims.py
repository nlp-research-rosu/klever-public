#!/usr/bin/env python3
"""Mechanical program pinning and claim-domain audit."""

from __future__ import annotations

import csv
import importlib.util
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.even_odd_palindrome


def balanced_call_contents(text: str, name: str, start: int = 0) -> str:
    match = re.search(rf"\b{re.escape(name)}\s*\(", text[start:])
    if match is None:
        raise AssertionError(f"missing {name}(...)")
    open_index = start + match.end() - 1
    depth = 0
    quote = False
    escaped = False
    for index in range(open_index, len(text)):
        char = text[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[open_index + 1 : index]
    raise AssertionError(f"unterminated {name}(...)")


def split_top_level(text: str) -> list[str]:
    pieces: list[str] = []
    begin = 0
    depth = 0
    quote = False
    escaped = False
    for index, char in enumerate(text):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            pieces.append(text[begin:index].strip())
            begin = index + 1
    pieces.append(text[begin:].strip())
    return pieces


TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|'
    r"-?[0-9]+|"
    r"\.[A-Za-z][A-Za-z0-9-]*|"
    r"[A-Za-z#][A-Za-z0-9#-]*|"
    r"[(),]"
)


def constructor_tokens(text: str) -> list[str]:
    tokens = TOKEN.findall(text)
    residue = TOKEN.sub("", text)
    if residue.strip():
        raise AssertionError(f"unlexed constructor text: {residue[:100]!r}")
    return tokens


solution_mpy = (SCRATCH / "solution.mpy").read_text(encoding="utf-8")
verification = (SCRATCH / "verification.k").read_text(encoding="utf-8")
spec_text = (SCRATCH / "spec.k").read_text(encoding="utf-8")

module_args = split_top_level(balanced_call_contents(solution_mpy, "Module"))
assert len(module_args) == 1
function_args = split_top_level(balanced_call_contents(module_args[0], "FuncDef"))
assert len(function_args) == 3
function_name, source_params, source_body = function_args
assert function_name == '"even_odd_palindrome"'
assert constructor_tokens(source_params) == ["Params", "(", '"n"', ")"]

closure_start = verification.index("=> closureVal(")
closure_args = split_top_level(
    balanced_call_contents(verification, "closureVal", closure_start)
)
assert len(closure_args) == 3
proof_params, proof_body, definition_environment = closure_args
expected_proof_params = ["(", '"n"', ",", ".ParamNames", ")"]
assert constructor_tokens(proof_params) == expected_proof_params
assert definition_environment.strip() == "0"
body_tokens_equal = constructor_tokens(source_body) == constructor_tokens(proof_body)
assert body_tokens_equal

assert verification.count('syntax Val ::= "solutionClosure"') == 1
assert verification.count("rule solutionClosure()") == 1
assert verification.count("=> closureVal(") == 1

claim_pattern = re.compile(
    r"claim \[(?P<label>[^\]]+)\]:\s*"
    r"<k>\s*Call\(solutionClosure\(\), Int\(N\)\)\s*"
    r"=> tuple\(vCons\((?P<even>\d+), "
    r"vCons\((?P<odd>\d+), \.ValSeq\)\)\)\s*</k>"
    r"(?P<cells>.*?)"
    r"requires (?P<lower>\d+) <=Int N andBool "
    r"N (?P<upper_op><=Int|<Int) (?P<upper>\d+)",
    re.DOTALL,
)
claims = list(claim_pattern.finditer(spec_text))
assert len(claims) == 108
assert spec_text.count("claim [") == len(claims)

required_cells = {
    "<env> 0 </env>",
    "<scopeLoc> 1 </scopeLoc>",
    "<heap> .Map </heap>",
    "<heapLoc> 0 </heapLoc>",
    "<stack> .List </stack>",
    "<ret> noRet </ret>",
    "<exc> NoExc </exc>",
    "<exit-code> 0 </exit-code>",
}

canonical = load_entry("pinning_canonical", Path("/reference/canonical.py"))
generated = load_entry("pinning_generated", SCRATCH / "solution.py")
covered: dict[int, str] = {}
rows: list[dict[str, object]] = []
for claim in claims:
    cells_compact = re.sub(r"\s+", " ", claim.group("cells")).strip()
    for cell in required_cells:
        assert cell in cells_compact, (claim.group("label"), cell)
    assert "0 |-> scope(.Map, parent(-1))" in cells_compact
    assert "-1 |-> builtinsScope" in cells_compact

    lower = int(claim.group("lower"))
    stated_upper = int(claim.group("upper"))
    upper = stated_upper + 1 if claim.group("upper_op") == "<=Int" else stated_upper
    expected = (int(claim.group("even")), int(claim.group("odd")))
    assert lower < upper
    witness = lower
    assert lower <= witness < upper
    canonical_result = canonical(witness)
    generated_result = generated(witness)
    assert expected == canonical_result == generated_result
    for n in range(lower, upper):
        assert n not in covered, (n, covered.get(n), claim.group("label"))
        covered[n] = claim.group("label")
        assert canonical(n) == expected
        assert generated(n) == expected
    rows.append(
        {
            "label": claim.group("label"),
            "lower": lower,
            "upper_exclusive": upper,
            "witness": witness,
            "target": expected,
            "canonical": canonical_result,
            "generated": generated_result,
            "satisfies_precondition": True,
        }
    )

assert sorted(covered) == list(range(1, 1001))
with Path("/audit-output/evidence/claim_witnesses.csv").open(
    "w", newline="", encoding="utf-8"
) as stream:
    writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"function_binding_name={function_name}")
print(f"source_params={source_params}")
print(f"proof_closure_params={proof_params}")
print(f"definition_environment={definition_environment.strip()}")
print(f"source_body_constructor_tokens={len(constructor_tokens(source_body))}")
print(f"proof_body_constructor_tokens={len(constructor_tokens(proof_body))}")
print(f"constructor_body_identity={str(body_tokens_equal).lower()}")
print("spec_lhs=Call(solutionClosure(), Int(N))")
print(f"claims={len(claims)}")
print("claim_preconditions_satisfiable=108/108")
print("witness_results_match_both_python_implementations=108/108")
print("interval_result_checks_match_both_python_implementations=1000/1000")
print("coverage=1..1000 exact_disjoint=true")
print("witness_csv=/audit-output/evidence/claim_witnesses.csv")
