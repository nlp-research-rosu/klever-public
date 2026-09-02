#!/usr/bin/env python3
"""Mechanically check the proof helper's AST pinning and list claim witnesses."""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate-src")
verification = (ROOT / "verification.k").read_text()
submitted_mpy = (ROOT / "solution.mpy").read_text()
spec_text = (ROOT / "spec.k").read_text()

def extract_rule_term(rule_name: str, head: str) -> str:
    start_match = re.search(
        rf"rule\s+{re.escape(rule_name)}\s*=>\s*{re.escape(head)}\(",
        verification,
    )
    if start_match is None:
        raise RuntimeError(f"{rule_name} equation not found")
    start = verification.index(head + "(", start_match.start())
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(verification[start:], start=start):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return verification[start : index + 1]
    raise RuntimeError(f"unterminated {rule_name} term")


equation_rhs = extract_rule_term("solutionProgram", "Module")
loop_rhs = extract_rule_term("collatzLoop", "While")
branch_rhs = extract_rule_term("collatzBranch", "If")

token_pattern = re.compile(r'"(?:[^"\\]|\\.)*"|[A-Za-z_][A-Za-z0-9_]*|-?\d+|[(),]')


def implicit_list_form(term: str) -> str:
    # solution.mpy uses the concrete List{...} surface syntax, which omits
    # explicit list-unit terms that are written in verification.k claims.
    return re.sub(r"(?:,\s*)?\.(?:Ids|Exprs|CmpOps|Stmts)", "", term)


rhs_tokens = token_pattern.findall(implicit_list_form(equation_rhs))
loop_tokens = token_pattern.findall(implicit_list_form(loop_rhs))
branch_tokens = token_pattern.findall(implicit_list_form(branch_rhs))


def expand(tokens: list[str]) -> list[str]:
    result: list[str] = []
    for token in tokens:
        if token == "collatzLoop":
            result.extend(loop_tokens)
        elif token == "collatzBranch":
            result.extend(branch_tokens)
        else:
            result.append(token)
    return result


rhs_tokens = expand(expand(rhs_tokens))
mpy_tokens = token_pattern.findall(submitted_mpy)

print(f"solutionProgram_rhs_token_count={len(rhs_tokens)}")
print(f"submitted_mpy_token_count={len(mpy_tokens)}")
print(f"solutionProgram_matches_submitted_mpy={rhs_tokens == mpy_tokens}")
print(
    "solutionProgram_token_sha256="
    + hashlib.sha256("\n".join(rhs_tokens).encode()).hexdigest()
)
print(
    "submitted_mpy_token_sha256="
    + hashlib.sha256("\n".join(mpy_tokens).encode()).hexdigest()
)
if rhs_tokens != mpy_tokens:
    raise SystemExit(1)

entry_inputs = [
    int(value)
    for value in re.findall(
        r"<k>\s*run\(solutionProgram\)\s*=>\s*\.K\s*</k>\s*"
        r"<input>\s*(\d+)\s*</input>",
        spec_text,
        re.DOTALL,
    )
]
print(f"entry_claim_inputs={entry_inputs!r}")
print(f"entry_claim_count={len(entry_inputs)}")
print("entry_claim_domain_is_finite=" + str(entry_inputs == [1, 2, 3, 5, 6, 7, 19, 27]))


def load_entry(name: str, path: Path):
    module_spec = importlib.util.spec_from_file_location(name, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module.get_odd_collatz


canonical = load_entry("trusted", Path("/tmp/audit-work/reference/canonical.py"))
candidate = load_entry("candidate", ROOT / "solution.py")
for n in entry_inputs:
    print(f"entry_witness n={n} canonical={canonical(n)!r} candidate={candidate(n)!r}")

print('even_step_witness=M=1, OS=.Ints, initial env={"n":vi(2),"odds":vl(.Ints)}')
print('odd_step_witness=M=1, OS=.Ints, initial env={"n":vi(3),"odds":vl(.Ints)}')
print("observer_witnesses=their exact fully-ground initial configurations")
