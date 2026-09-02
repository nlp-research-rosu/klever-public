#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and claim program."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/rebuild")
solution_document = json.loads((SCRATCH / "solution.kast.json").read_text())
spec_document = json.loads((SCRATCH / "spec-claims.json").read_text())
solution_term = solution_document["term"]


def label(term: object) -> str:
    if not isinstance(term, dict):
        return ""
    return str(term.get("label", {}).get("name", ""))


def walk(term: object):
    yield term
    if isinstance(term, dict):
        for value in term.values():
            yield from walk(value)
    elif isinstance(term, list):
        for value in term:
            yield from walk(value)


loads = [
    term
    for term in walk(spec_document)
    if isinstance(term, dict)
    and term.get("node") == "KApply"
    and label(term) == "#loadAll(_)_MPY-CORE_KItem_Module"
]
claims = [
    term
    for term in walk(spec_document)
    if isinstance(term, dict) and term.get("node") == "KClaim"
]
assert len(claims) == 1, len(claims)
assert len(loads) == 1, len(loads)
claim_module_term = loads[0]["args"][0]
constructor_equal = claim_module_term == solution_term

claim = claims[0]
claim_label = claim["att"]["att"]["label"]
requires = claim["requires"]
ensures = claim["ensures"]
bool_true = {
    "node": "KToken",
    "sort": {"node": "KSort", "name": "Bool"},
    "token": "true",
}
assert claim_label == "SPEC.flip-case"
assert requires == bool_true
assert ensures == bool_true

serialized_solution = json.dumps(
    solution_term, sort_keys=True, separators=(",", ":")
).encode()
serialized_claim_module = json.dumps(
    claim_module_term, sort_keys=True, separators=(",", ":")
).encode()
print(f"claim_count={len(claims)}")
print(f"claim_label={claim_label}")
print(f"loadAll_module_count={len(loads)}")
print(
    "solution_constructor_sha256="
    + hashlib.sha256(serialized_solution).hexdigest()
)
print(
    "claim_module_constructor_sha256="
    + hashlib.sha256(serialized_claim_module).hexdigest()
)
print(f"constructor_level_identity={constructor_equal}")
print(f"requires_is_true={requires == bool_true}")
print(f"ensures_is_true={ensures == bool_true}")
if not constructor_equal:
    raise SystemExit(1)
print("PROGRAM_PINNING_STATUS=PASS")
