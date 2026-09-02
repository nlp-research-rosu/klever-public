#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and entry claim."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


SOLUTION_JSON = Path("/tmp/audit-work/149-sorted-list-sum/solution-kast.json")
SPEC_JSON = Path("/tmp/audit-work/149-sorted-list-sum/spec-audit.json")


def applies(node, prefix: str):
    found = []
    if isinstance(node, dict):
        if node.get("node") == "KApply" and node.get("label", {}).get("name", "").startswith(prefix):
            found.append(node)
        for value in node.values():
            found.extend(applies(value, prefix))
    elif isinstance(node, list):
        for value in node:
            found.extend(applies(value, prefix))
    return found


solution_document = json.loads(SOLUTION_JSON.read_text())
spec_document = json.loads(SPEC_JSON.read_text())
solution_functions = applies(solution_document["term"], "FuncDef(_,_,_)_")

claims = []
for module in spec_document["term"]["term"]:
    claims.extend(
        sentence
        for sentence in module.get("localSentences", [])
        if sentence.get("node") == "KClaim"
    )
claim_functions = [(claim, applies(claim["body"], "FuncDef(_,_,_)_")) for claim in claims]
entry_claims = [(claim, funcs) for claim, funcs in claim_functions if funcs]

print(f"solution_funcdef_count={len(solution_functions)}")
print(f"spec_claim_count={len(claims)}")
print(f"entry_claim_count={len(entry_claims)}")
print(f"entry_funcdef_count={len(entry_claims[0][1]) if entry_claims else 0}")

if len(solution_functions) != 1 or len(entry_claims) != 1 or len(entry_claims[0][1]) != 1:
    raise SystemExit(1)

solution_term = solution_functions[0]
claim_term = entry_claims[0][1][0]
solution_bytes = json.dumps(solution_term, sort_keys=True, separators=(",", ":")).encode()
claim_bytes = json.dumps(claim_term, sort_keys=True, separators=(",", ":")).encode()
print(f"solution_funcdef_json_sha256={hashlib.sha256(solution_bytes).hexdigest()}")
print(f"claim_funcdef_json_sha256={hashlib.sha256(claim_bytes).hexdigest()}")
print(f"constructor_terms_equal={solution_term == claim_term}")
print(
    "function_name="
    + solution_term["args"][0]["token"]
    + " params_term="
    + json.dumps(solution_term["args"][1], sort_keys=True)
)
raise SystemExit(0 if solution_term == claim_term else 1)
