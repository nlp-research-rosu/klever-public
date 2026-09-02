#!/usr/bin/env python3
"""Mechanical source-to-claim pinning checks and concrete claim witnesses."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


WORK = Path("/tmp/audit-work/124-valid-date")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize_k(text: str) -> str:
    text = re.sub(r"//[^\n]*", "", text)
    return re.sub(r"\s+", "", text)


solution_term = normalize_k((WORK / "regenerated-solution.mpy").read_text())
verification_text = (WORK / "verification.k").read_text()
verification_term = normalize_k(verification_text)
spec_text = (WORK / "spec.k").read_text()
operational_k_rules = len(re.findall(r"\brule\s+<k>", verification_text))
entry_claim_count = len(re.findall(r"(?m)^\s*claim\s*$", spec_text))

prefix = 'Module(FuncDef("valid_date",Params("date"),'
assert solution_term.startswith(prefix)
assert solution_term.endswith("))")
solution_body = solution_term[len(prefix) : -2]

body_match = re.search(
    r"rule\s+validDateBody\s*=>\s*(.*?)\n\s*syntax\s+Val\s*::=",
    verification_text,
    flags=re.DOTALL,
)
assert body_match is not None
verification_body = normalize_k(body_match.group(1))

# The translator emits an empty Stmts-list as an omitted list argument, while
# verification.k spells the same list unit explicitly as .Stmts.
verification_body_translator_form = verification_body.replace(",.Stmts)", ",)")
body_equal = verification_body_translator_form == solution_body

module_equation = (
    'rulevalidDateModule=>'
    'Module(FuncDef("valid_date",Params("date"),validDateBody))'
)
closure_equation = (
    'rulevalidDateClosure=>closureVal("date",validDateBody,0)'
)

print(f"regenerated_solution_outer_constructor={prefix[:-1]}")
print(f"solution_body_character_count={len(solution_body)}")
print(f"verification_body_character_count={len(verification_body)}")
print(f"body_equal_after_empty_stmts_normalization={body_equal}")
print(f"module_equation_exact={module_equation in verification_term}")
print(f"closure_equation_exact={closure_equation in verification_term}")
print(f"verification_operational_k_rules={operational_k_rules}")
print(f"spec_entry_claim_count={entry_claim_count}")
print(f"first_claim_has_length_not_ten={'requires isLen(CS) =/=Int 10' in spec_text}")
print(f"second_claim_explicit_iCons_count={spec_text.count('iCons(')}")

generated = load("generated_solution_pinning", WORK / "solution.py").valid_date
canonical = load("trusted_canonical_pinning", WORK / "trusted_canonical.py").valid_date


def prompt_formula(value: str) -> bool:
    if len(value) != 10 or value[2] != "-" or value[5] != "-":
        return False
    codes = [ord(char) for char in value]
    digit_positions = [0, 1, 3, 4, 6, 7, 8, 9]
    if any(not (48 <= codes[index] <= 57) for index in digit_positions):
        return False
    month = (codes[0] - 48) * 10 + codes[1] - 48
    day = (codes[3] - 48) * 10 + codes[4] - 48
    limit = 29 if month == 2 else 30 if month in (4, 6, 9, 11) else 31
    return 1 <= month <= 12 and 1 <= day <= limit


witnesses = [
    ("claim-length-not-ten", "", True),
    ("claim-length-ten-valid", "02-29-2000", True),
    ("claim-length-ten-invalid", "04-31-2040", True),
    ("claim-length-ten-canonical-disagreement", "01-31-2000", True),
]
for name, value, state_realizable in witnesses:
    precondition = (len(value) != 10) if name == "claim-length-not-ten" else (len(value) == 10)
    print(
        f"witness={name} input={value!r} realizable={state_realizable} "
        f"precondition={precondition} claimed_formula={prompt_formula(value)} "
        f"generated={generated(value)} canonical={canonical(value)}"
    )

assert body_equal
assert module_equation in verification_term
assert closure_equation in verification_term
assert operational_k_rules == 0
assert entry_claim_count == 2
assert all(state_realizable for _, _, state_realizable in witnesses)
assert len(witnesses[0][1]) != 10
assert all(len(value) == 10 for _, value, _ in witnesses[1:])
assert prompt_formula("") is False
assert prompt_formula("02-29-2000") is True
assert prompt_formula("04-31-2040") is False
assert generated("02-29-2000") == canonical("02-29-2000") == True
assert generated("04-31-2040") == canonical("04-31-2040") == False
print("PINNING_AND_WITNESSES=PASS")
