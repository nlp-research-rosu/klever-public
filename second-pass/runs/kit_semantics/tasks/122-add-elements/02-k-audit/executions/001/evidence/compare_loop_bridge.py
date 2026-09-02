#!/usr/bin/env python3
"""Compare the compiled operational bridge to its bridge-free claim."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def walk(term: Any):
    if isinstance(term, dict):
        yield term
        for value in term.values():
            yield from walk(value)
    elif isinstance(term, list):
        for value in term:
            yield from walk(value)


def canonical_hash(term: Any) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def first_differences(left: Any, right: Any, path: str = "$", limit: int = 20):
    differences: list[str] = []

    def visit(a: Any, b: Any, here: str) -> None:
        if len(differences) >= limit:
            return
        if type(a) is not type(b):
            differences.append(f"{here}: type {type(a).__name__} != {type(b).__name__}")
            return
        if isinstance(a, dict):
            if a.keys() != b.keys():
                differences.append(
                    f"{here}: keys {sorted(a.keys())} != {sorted(b.keys())}"
                )
                return
            for key in a:
                visit(a[key], b[key], f"{here}.{key}")
            return
        if isinstance(a, list):
            if len(a) != len(b):
                differences.append(f"{here}: list lengths {len(a)} != {len(b)}")
                return
            for index, (a_item, b_item) in enumerate(zip(a, b)):
                visit(a_item, b_item, f"{here}[{index}]")
            return
        if a != b:
            differences.append(f"{here}: {a!r} != {b!r}")

    visit(left, right, path)
    return differences


compiled = json.loads(
    Path(
        "/tmp/audit-work/122-add-elements/verification-json-kompiled/compiled.json"
    ).read_text()
)
claim_doc = json.loads(
    Path("/tmp/audit-work/122-add-elements/loop-claim.json").read_text()
)

bridge_rules = []
for node in walk(compiled):
    if node.get("node") != "KRule":
        continue
    att = node.get("att", {}).get("att", {})
    source = att.get("org.kframework.attributes.Source")
    if source == "/tmp/audit-work/122-add-elements/verification.k":
        bridge_rules.append(node)

claims = [node for node in walk(claim_doc) if node.get("node") == "KClaim"]
print(f"compiled_rules_sourced_from_verification_k={len(bridge_rules)}")
print(f"loop_claim_nodes={len(claims)}")
if len(bridge_rules) != 1 or len(claims) != 1:
    raise SystemExit(1)

bridge = bridge_rules[0]
claim = claims[0]
for field in ("body", "requires", "ensures"):
    bridge_hash = canonical_hash(bridge[field])
    claim_hash = canonical_hash(claim[field])
    print(f"{field}_bridge_hash={bridge_hash}")
    print(f"{field}_claim_hash={claim_hash}")
    print(f"{field}_identity={bridge[field] == claim[field]}")
    if bridge[field] != claim[field]:
        print(f"{field}_first_differences:")
        for difference in first_differences(bridge[field], claim[field]):
            print(f"- {difference}")
        if field == "body":
            print("bridge_generated_counter_cell=" + json.dumps(bridge[field]["args"][10], sort_keys=True))
            print("claim_generated_counter_cell=" + json.dumps(claim[field]["args"][10], sort_keys=True))

bridge_att = bridge["att"]["att"]
claim_att = claim["att"]["att"]
print(f"bridge_priority={bridge_att.get('priority')}")
print(f"bridge_source={bridge_att.get('org.kframework.attributes.Source')}")
print(f"claim_source={claim_att.get('org.kframework.attributes.Source')}")
visible_body_equal = (
    bridge["body"].get("label") == claim["body"].get("label")
    and bridge["body"].get("args", [])[:10] == claim["body"].get("args", [])[:10]
)
logical_equal = bridge["requires"] == claim["requires"] and bridge["ensures"] == claim["ensures"]
print(f"program_visible_cells_identity={visible_body_equal}")
print(f"logical_side_conditions_identity={logical_equal}")
print(
    "FULL_COMPILED_CONTEXT_IDENTITY="
    + ("PASS" if bridge["body"] == claim["body"] and logical_equal else "FAIL")
)
print(
    "BRIDGE_CLAIM_PROGRAM_VISIBLE_CONTEXT_IDENTITY="
    + ("PASS" if visible_body_equal and logical_equal else "FAIL")
)
raise SystemExit(0 if visible_body_equal and logical_equal else 1)
