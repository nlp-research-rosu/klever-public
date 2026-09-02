#!/usr/bin/env python3
"""Compare the parsed program with the parsed entry-claim program term."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


SCRATCH = Path("/tmp/audit-work/66-digitsum-audit")


def digest_json(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def find_k_cell(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        label = value.get("label")
        if (
            value.get("node") == "KApply"
            and isinstance(label, dict)
            and label.get("name") == "<k>"
        ):
            return value
        for child in value.values():
            found = find_k_cell(child)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_k_cell(child)
            if found is not None:
                return found
    return None


solution_document = json.loads((SCRATCH / "solution.json").read_text())
spec_document = json.loads((SCRATCH / "spec-labeled.json").read_text())
solution_term = solution_document["term"]

modules = spec_document["term"]["term"]
spec_module = next(module for module in modules if module["name"] == "SPEC-LABELED")
entry_claim = spec_module["localSentences"][0]
assert entry_claim["node"] == "KClaim"
k_cell = find_k_cell(entry_claim["body"])
assert k_cell is not None
k_content = k_cell["args"][0]
assert k_content["node"] == "KRewrite"
claim_program_term = k_content["lhs"]

solution_digest = digest_json(solution_term)
claim_digest = digest_json(claim_program_term)
print("COMMAND: python3 /audit-output/evidence/constructor_compare.py")
print(f"solution_constructor_sha256={solution_digest}")
print(f"entry_claim_lhs_constructor_sha256={claim_digest}")
print(f"constructor_terms_equal={'yes' if solution_term == claim_program_term else 'NO'}")
assert solution_term == claim_program_term
print("CONSTRUCTOR_PINNING=PASS")
