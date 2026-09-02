#!/usr/bin/env python3
from pathlib import Path


claim = Path("/reference/k-proof/connection-spec.k").read_text().splitlines()
rule = Path("/reference/k-proof/connection-rule.k").read_text().splitlines()
claim_transition = claim[9:47]
rule_transition = rule[8:46]

print("claim_body_lines=10-47")
print("rule_body_lines=9-46")
print(f"exact_transition_equal={claim_transition == rule_transition}")
if claim_transition != rule_transition:
    for index, (left, right) in enumerate(
        zip(claim_transition, rule_transition), start=1
    ):
        if left != right:
            print(f"first_difference_relative_line={index}")
            print(f"claim={left!r}")
            print(f"rule={right!r}")
            break
