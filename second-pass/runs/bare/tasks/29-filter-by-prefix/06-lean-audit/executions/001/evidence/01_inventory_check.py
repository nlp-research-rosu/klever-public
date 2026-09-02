#!/usr/bin/env python3
"""Reconstruct and compare the exact Stage 1 verification rule inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, lemma_discovery_contract


workspace = Path("/reference/k-proof")
verification = workspace / "verification.k"
manifest_path = Path("/reference/lemma-discovery.json")
inventory = k_rule_inventory.inventory_verification(workspace)
validated = lemma_discovery_contract.validate_trust_boundary(
    workspace, manifest_path
)
manifest = json.loads(manifest_path.read_text())

canonical_rules = inventory["rules"]
classified_rules = manifest["rules"]
canonical_ids = [entry["source_rule_id"] for entry in canonical_rules]
classified_ids = [entry["source_rule_id"] for entry in classified_rules]
assert classified_ids == canonical_ids
assert len(classified_ids) == len(set(classified_ids))
assert len(classified_ids) == len(canonical_rules)
assert manifest["inventory_sha256"] == inventory["inventory_sha256"]
assert inventory["inventory_sha256"] == (
    k_rule_inventory.canonical_json_sha256(canonical_rules)
)
assert inventory["verification_sha256"] == hashlib.sha256(
    verification.read_bytes()
).hexdigest()
assert inventory["verification_module"] == "VERIFICATION"
assert inventory["verification_modules"] == ["VERIFICATION"]

lines = verification.read_text().splitlines()
for rule in canonical_rules:
    source_slice = "\n".join(
        lines[rule["start_line"] - 1 : rule["end_line"]]
    ).rstrip()
    assert source_slice == rule["text"]
    normalized = " ".join(rule["text"].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    assert digest == rule["normalized_sha256"]
    assert rule["source_rule_id"] == f"rule-{digest}"

expected_roles = ["DEFINITION"] * 6
observed_roles = [entry["classification"] for entry in classified_rules]
assert observed_roles == expected_roles
assert len(validated["definitions"]) == 6
assert validated["operational_rules"] == []
assert validated["proved_derived_lemmas"] == []
assert validated["domain_lemmas"] == []
for rule, role in zip(canonical_rules, observed_roles, strict=True):
    if "simplification" in rule["attributes"]:
        assert role == "DEFINITION"

print(
    json.dumps(
        {
            "status": "PASS",
            "verification_sha256": inventory["verification_sha256"],
            "verification_module": inventory["verification_module"],
            "verification_modules": inventory["verification_modules"],
            "inventory_sha256": inventory["inventory_sha256"],
            "manifest_order_exact": classified_ids == canonical_ids,
            "rule_count": len(canonical_rules),
            "domain_rule_count": len(validated["domain_lemmas"]),
            "rules": [
                {
                    **rule,
                    "classification": role,
                }
                for rule, role in zip(
                    canonical_rules, observed_roles, strict=True
                )
            ],
        },
        indent=2,
        sort_keys=True,
    )
)
