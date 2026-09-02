#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction and bijection checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
verification_path = workspace / "verification.k"

inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
validated = validate_trust_boundary(workspace, manifest_path)
source_lines = verification_path.read_text().splitlines()

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [entry["source_rule_id"] for entry in manifest["rules"]]

rule_checks = []
for rule in inventory["rules"]:
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    source_span_text = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    rule_checks.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "source_span": [rule["start_line"], rule["end_line"]],
            "span_text_exact": source_span_text == rule["text"],
            "normalized_sha256_recomputed": normalized_sha256,
            "normalized_sha256_exact": normalized_sha256
            == rule["normalized_sha256"],
            "source_rule_id_exact": rule["source_rule_id"]
            == f"rule-{normalized_sha256}",
        }
    )

classified_ids = {
    role: [rule["source_rule_id"] for rule in validated[role]]
    for role in (
        "definitions",
        "operational_rules",
        "proved_derived_lemmas",
        "domain_lemmas",
    )
}

report = {
    "reconstructed_inventory": inventory,
    "independent_rule_checks": rule_checks,
    "bijection_checks": {
        "manifest_schema_version": manifest.get("schema_version"),
        "inventory_hash_recomputed": canonical_json_sha256(inventory["rules"]),
        "inventory_hash_matches_manifest": inventory["inventory_sha256"]
        == manifest.get("inventory_sha256"),
        "same_count": len(inventory_ids) == len(manifest_ids),
        "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
        "manifest_ids_unique": len(manifest_ids) == len(set(manifest_ids)),
        "same_ids_in_same_order": inventory_ids == manifest_ids,
        "omitted_ids": [item for item in inventory_ids if item not in manifest_ids],
        "extra_ids": [item for item in manifest_ids if item not in inventory_ids],
        "unaccounted_after_contract": [
            item
            for item in inventory_ids
            if item
            not in {
                source_rule_id
                for values in classified_ids.values()
                for source_rule_id in values
            }
        ],
        "contract_validation": "PASS",
    },
    "contract_classification_buckets": classified_ids,
}

print(json.dumps(report, indent=2, sort_keys=True))
