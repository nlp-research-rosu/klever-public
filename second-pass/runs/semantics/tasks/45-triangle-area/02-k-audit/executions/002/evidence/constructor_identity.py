#!/usr/bin/env python3
"""Mechanical whitespace-insensitive constructor comparison."""

from __future__ import annotations

import re
from pathlib import Path


generated = Path("/tmp/audit-work/proof/regenerated-solution.mpy").read_text()
verification = Path("/tmp/audit-work/proof/verification.k").read_text()
specification = Path("/tmp/audit-work/proof/spec.k").read_text()

match = re.search(
    r"rule\s+triangleAreaProgram\s*=>\s*(Module\s*\(.*?\))\s*endmodule",
    verification,
    re.DOTALL,
)
if match is None:
    raise SystemExit("triangleAreaProgram rule not found")
program_rhs = match.group(1)


def constructor_normal_form(text: str) -> str:
    text = re.sub(r"//[^\n]*", "", text)
    return re.sub(r"\s+", "", text)


generated_nf = constructor_normal_form(generated)
rule_nf = constructor_normal_form(program_rhs)
print(f"generated_constructor_nf={generated_nf}")
print(f"verification_constructor_nf={rule_nf}")
print(f"constructor_identity={generated_nf == rule_nf}")

required_spec_fragments = [
    "#loadAll(triangleAreaProgram)",
    'Call(Name("triangle_area"), Int(A), Int(H))',
    "=> divII(A *Int H, 2)",
    '<env> 0 </env>',
    "<heap> .Map </heap>",
    "<stack> .List </stack>",
    "<ret> noRet </ret>",
    "<exc> NoExc </exc>",
]
for fragment in required_spec_fragments:
    present = fragment in specification
    print(f"spec_fragment[{fragment!r}]={present}")
    if not present:
        raise SystemExit(f"missing spec fragment: {fragment}")

if generated_nf != rule_nf:
    raise SystemExit("constructor mismatch")
print("PROGRAM_PINNING_CHECK=PASS")
