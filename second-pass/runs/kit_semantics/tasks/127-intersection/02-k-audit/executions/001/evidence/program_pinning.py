#!/usr/bin/env python3
"""Mechanical constructor-level check from trusted translation to claim term."""

import hashlib
import re
from pathlib import Path


scratch = Path("/tmp/audit-work/127-intersection")
translated = (scratch / "regenerated-solution.mpy").read_text().strip()
solution_module = (scratch / "solution-module.k").read_text()
spec = (scratch / "spec.k").read_text()

# The standalone MPY parser accepts an omitted final Stmts-list argument as the
# empty list. The in-rule spelling makes that value explicit as `.Stmts`.
translated_explicit = re.sub(
    r",\n(?P<indent> *)\)", r",\n\g<indent>.Stmts)", translated
)

rhs_match = re.search(
    r"\brule\s+solutionModule\s*=>\s*(Module\([\s\S]*\))\s*endmodule\s*$",
    solution_module,
)
assert rhs_match is not None, "could not extract solutionModule RHS"
rhs = rhs_match.group(1)


def constructor_normal_form(text: str) -> str:
    return re.sub(r"\s+", "", text)


translated_normal = constructor_normal_form(translated_explicit)
rhs_normal = constructor_normal_form(rhs)
assert translated_normal == rhs_normal, "solutionModule RHS differs from trusted translation"
assert solution_module.count("rule solutionModule") == 1
assert translated_normal.count('FuncDef("intersection"') == 1

assert "#loadAll(solutionModule)" in spec
assert 'Call(Name("intersection")' in spec
assert spec.count("claim [intersection-correct]") == 1

digest = hashlib.sha256(translated_normal.encode()).hexdigest()
print("trusted_translation_to_solutionModule_constructor_identity=true")
print("entry_claim_loads_solutionModule=true")
print("entry_claim_calls_intersection=true")
print(f"normalized_constructor_sha256={digest}")
print("normalization=whitespace removal plus explicit .Stmts for omitted empty list arguments")
