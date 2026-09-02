#!/usr/bin/env python3
"""Reconstruct and compare the frozen verification-module rule inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
canonical_rules = inventory["rules"]
manifest_rules = manifest["rules"]

recomputed_rules = []
for rule in canonical_rules:
    normalized = " ".join(rule["text"].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    recomputed_rules.append(
        {
            **rule,
            "independent_normalized_text": normalized,
            "independent_normalized_sha256": digest,
            "independent_source_rule_id": f"rule-{digest}",
            "normalized_hash_matches": digest == rule["normalized_sha256"],
            "source_rule_id_matches": f"rule-{digest}" == rule["source_rule_id"],
        }
    )

canonical_ids = [rule["source_rule_id"] for rule in canonical_rules]
manifest_ids = [rule["source_rule_id"] for rule in manifest_rules]
result = {
    "command": (
        "PYTHONPATH=/reference python3 "
        "/audit-output/evidence/01_inventory_command.py"
    ),
    "verification_module": inventory["verification_module"],
    "verification_modules": inventory["verification_modules"],
    "verification_sha256": inventory["verification_sha256"],
    "rules": recomputed_rules,
    "inventory_sha256": inventory["inventory_sha256"],
    "independent_inventory_sha256": canonical_json_sha256(canonical_rules),
    "manifest_inventory_sha256": manifest["inventory_sha256"],
    "canonical_ids": canonical_ids,
    "manifest_ids": manifest_ids,
    "bijection": {
        "same_count": len(canonical_ids) == len(manifest_ids),
        "no_canonical_duplicates": len(canonical_ids) == len(set(canonical_ids)),
        "no_manifest_duplicates": len(manifest_ids) == len(set(manifest_ids)),
        "same_id_set": set(canonical_ids) == set(manifest_ids),
        "same_order": canonical_ids == manifest_ids,
        "inventory_hash_matches_manifest": (
            inventory["inventory_sha256"] == manifest["inventory_sha256"]
        ),
    },
    "manifest_classifications": [
        {
            "source_rule_id": entry["source_rule_id"],
            "classification": entry["classification"],
            "rationale": entry["rationale"],
        }
        for entry in manifest_rules
    ],
}
print(json.dumps(result, indent=2, sort_keys=True))
