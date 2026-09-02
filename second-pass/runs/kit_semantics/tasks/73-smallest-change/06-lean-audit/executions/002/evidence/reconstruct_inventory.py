#!/usr/bin/env python3
"""Reconstruct and compare the Stage 1 K rule inventory with trusted code."""

from __future__ import annotations

import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
output_path = Path("/audit-output/evidence/reconstructed-inventory.json")

reconstructed = inventory_verification(workspace)
output_path.write_text(
    json.dumps(reconstructed, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

discovery = json.loads(discovery_path.read_text(encoding="utf-8"))
reconstructed_ids = [rule["source_rule_id"] for rule in reconstructed["rules"]]
discovery_ids = [rule.get("source_rule_id") for rule in discovery.get("rules", [])]

print(json.dumps({
    "reconstructed_summary": {
        "verification_file": reconstructed.get("verification_file"),
        "verification_sha256": reconstructed.get("verification_sha256"),
        "verification_module": reconstructed.get("verification_module"),
        "verification_modules": reconstructed.get("verification_modules"),
        "required_files_sha256": reconstructed.get("required_files_sha256"),
        "rule_count": len(reconstructed.get("rules", [])),
        "inventory_sha256": reconstructed.get("inventory_sha256"),
    },
    "discovery_summary": {
        "schema_version": discovery.get("schema_version"),
        "inventory_sha256": discovery.get("inventory_sha256"),
        "rule_count": len(discovery_ids),
    },
    "inventory_hash_equal": discovery.get("inventory_sha256") == reconstructed.get("inventory_sha256"),
    "source_rule_ids_exact_order_equal": discovery_ids == reconstructed_ids,
    "reconstructed_ids_unique": len(reconstructed_ids) == len(set(reconstructed_ids)),
    "discovery_ids_unique": len(discovery_ids) == len(set(discovery_ids)),
    "reconstructed_ids": reconstructed_ids,
    "discovery_ids": discovery_ids,
}, indent=2, sort_keys=True))
