#!/usr/bin/env python3
"""Compare the semantic body of the sole loop rule with its base proof claim."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


def normalized_semantic_body(text: str) -> str:
    start = text.index("<k>")
    end = text.rindex("</scopes>") + len("</scopes>")
    return re.sub(r"\s+", "", text[start:end])


verification_lines = Path("/reference/k-proof/verification.k").read_text().splitlines()
spec_lines = Path("/reference/k-proof/spec.k").read_text().splitlines()

# The spans are independently reconstructed by the trusted inventory and by
# inspection of the unique LOOP-SPEC claim in the frozen source.
rule_sentence = "\n".join(verification_lines[65:94])
claim_sentence = "\n".join(spec_lines[5:33])
rule_body = normalized_semantic_body(rule_sentence)
claim_body = normalized_semantic_body(claim_sentence)

print("rule_source_span=verification.k:66-94")
print("claim_source_span=spec.k:6-33")
print("rule_body_sha256=" + hashlib.sha256(rule_body.encode()).hexdigest())
print("claim_body_sha256=" + hashlib.sha256(claim_body.encode()).hexdigest())
print("semantic_bodies_equal=" + str(rule_body == claim_body).lower())
print(
    "rule_only_syntax=rule sentence marker plus [priority(40)] scheduling attribute"
)
print("claim_only_syntax=claim [loop-invariant]: sentence marker")

if rule_body != claim_body:
    raise SystemExit("loop rule and connection claim differ")
