#!/usr/bin/env python3
"""Read-only Stage 3 structural reconstruction using the trusted inventory."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
verification_path = workspace / "verification.k"

inventory = inventory_verification(workspace)
validated = validate_trust_boundary(workspace, manifest_path)
manifest = json.loads(manifest_path.read_text())

inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
manifest_ids = [entry["source_rule_id"] for entry in manifest["rules"]]
inventory_counts = Counter(inventory_ids)
manifest_counts = Counter(manifest_ids)

checks = {
    "verification_file_sha256_matches_reconstruction": (
        inventory["verification_sha256"]
        == hashlib.sha256(verification_path.read_bytes()).hexdigest()
    ),
    "each_source_rule_id_is_normalized_hash": all(
        entry["source_rule_id"] == f"rule-{entry['normalized_sha256']}"
        for entry in inventory["rules"]
    ),
    "each_normalized_hash_matches_text": all(
        entry["normalized_sha256"]
        == hashlib.sha256(" ".join(entry["text"].split()).encode()).hexdigest()
        for entry in inventory["rules"]
    ),
    "inventory_hash_matches_reconstructed_rules": (
        inventory["inventory_sha256"]
        == canonical_json_sha256(inventory["rules"])
    ),
    "manifest_inventory_hash_matches": (
        manifest["inventory_sha256"] == inventory["inventory_sha256"]
    ),
    "same_count": len(inventory_ids) == len(manifest_ids),
    "no_inventory_duplicates": all(count == 1 for count in inventory_counts.values()),
    "no_manifest_duplicates": all(count == 1 for count in manifest_counts.values()),
    "no_manifest_omissions": set(inventory_ids) <= set(manifest_ids),
    "no_manifest_extras": set(manifest_ids) <= set(inventory_ids),
    "exact_identity_order": manifest_ids == inventory_ids,
    "trusted_contract_validation_returned_same_inventory": (
        validated["rules"] == inventory["rules"]
        and validated["inventory_sha256"] == inventory["inventory_sha256"]
    ),
}

print("CHECKS")
for name, result in checks.items():
    print(f"{name}: {result}")
print()
print("RECONSTRUCTED_INVENTORY")
print(json.dumps(inventory, indent=2, sort_keys=True, ensure_ascii=False))
print()
print("MANIFEST_CLASSIFICATIONS_IN_CANONICAL_ORDER")
by_id = {entry["source_rule_id"]: entry for entry in manifest["rules"]}
for index, rule in enumerate(inventory["rules"]):
    classification = by_id[rule["source_rule_id"]]
    print(
        json.dumps(
            {
                "index": index,
                **rule,
                "classification": classification["classification"],
                "rationale": classification["rationale"],
            },
            sort_keys=True,
            ensure_ascii=False,
        )
    )
print()
print("ALL_STRUCTURAL_CHECKS_PASS:", all(checks.values()))
