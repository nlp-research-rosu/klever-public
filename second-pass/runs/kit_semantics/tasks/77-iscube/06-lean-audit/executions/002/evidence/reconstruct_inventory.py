#!/usr/bin/env python3
"""Reconstruct the canonical K inventory and compare it to Stage 3."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
audit_input_path = Path("/audit-input.json")

inventory = inventory_verification(workspace)
discovery = json.loads(discovery_path.read_text(encoding="utf-8"))
audit_input = json.loads(audit_input_path.read_text(encoding="utf-8"))

actual_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
recorded_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
normalized_id_checks = [
    {
        "source_rule_id": rule["source_rule_id"],
        "normalized_sha256": rule["normalized_sha256"],
        "id_matches_normalized_sha256": (
            rule["source_rule_id"] == "rule-" + rule["normalized_sha256"]
        ),
    }
    for rule in inventory["rules"]
]

comparison = {
    "actual_rule_count": len(actual_ids),
    "recorded_rule_count": len(recorded_ids),
    "actual_ids_unique": len(actual_ids) == len(set(actual_ids)),
    "recorded_ids_unique": len(recorded_ids) == len(set(recorded_ids)),
    "exact_ordered_identity_match": actual_ids == recorded_ids,
    "missing_from_discovery": sorted(set(actual_ids) - set(recorded_ids)),
    "extra_in_discovery": sorted(set(recorded_ids) - set(actual_ids)),
    "inventory_hash_recomputed": inventory["inventory_sha256"],
    "inventory_hash_recorded": discovery.get("inventory_sha256"),
    "inventory_hash_matches": (
        inventory["inventory_sha256"] == discovery.get("inventory_sha256")
    ),
    "all_rule_ids_bind_normalized_hash": all(
        item["id_matches_normalized_sha256"] for item in normalized_id_checks
    ),
    "discovery_file_sha256_recomputed": hashlib.sha256(
        discovery_path.read_bytes()
    ).hexdigest(),
    "discovery_file_sha256_audit_input": audit_input["resolution"]["hashes"][
        "discovery_manifest_sha256"
    ],
}
comparison["discovery_file_hash_matches"] = (
    comparison["discovery_file_sha256_recomputed"]
    == comparison["discovery_file_sha256_audit_input"]
)

document = {
    "inventory": inventory,
    "normalized_id_checks": normalized_id_checks,
    "stage3_classifications_in_inventory_order": discovery["rules"],
    "comparison": comparison,
}
print(json.dumps(document, indent=2, sort_keys=False))
