#!/usr/bin/env python3
"""Check that the admitted loop summary is verbatim the proved loop claim."""

from __future__ import annotations

import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/52-below-threshold")
verification = (SCRATCH / "verification.k").read_text()
specification = (SCRATCH / "spec.k").read_text()


def normalize(text: str) -> str:
    text = re.sub(r"//[^\n]*", "", text)
    return "".join(text.split())


rule_module = verification[verification.index("module VERIFICATION\n") :]
rule_match = re.search(r"\brule\s+(.*?)\[priority\(40\)\]", rule_module, re.S)
if not rule_match:
    raise RuntimeError("derived loop rule not found")

loop_module = specification[
    specification.index("module LOOP-SPEC") : specification.index(
        "module SPEC", specification.index("module LOOP-SPEC")
    )
]
claim_match = re.search(
    r"\bclaim\s+(.*?)\[label\(loop-invariant\)\]", loop_module, re.S
)
if not claim_match:
    raise RuntimeError("loop claim not found")

normalized_rule = normalize(rule_match.group(1))
normalized_claim = normalize(claim_match.group(1))
base_module = verification[
    verification.index("module VERIFICATION-BASE") : verification.index(
        "module VERIFICATION\n"
    )
]

checks = {
    "derived_rule_body_equals_proved_claim_body": normalized_rule
    == normalized_claim,
    "derived_summary_absent_from_verification_base": "<k>#loop(list(intsToVals"
    not in normalize(base_module),
}
for name, result in checks.items():
    print(f"{name}={str(result).lower()}")
if not all(checks.values()):
    print("normalized rule:", normalized_rule)
    print("normalized claim:", normalized_claim)
    raise SystemExit(1)
