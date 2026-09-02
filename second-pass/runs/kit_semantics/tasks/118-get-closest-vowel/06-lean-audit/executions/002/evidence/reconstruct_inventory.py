#!/usr/bin/env python3
"""Reconstruct and independently cross-check the frozen local rule inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
MANIFEST = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(WORKSPACE)
manifest = json.loads(MANIFEST.read_text())
validated = validate_trust_boundary(WORKSPACE, MANIFEST)

rule_checks = []
for index, rule in enumerate(inventory["rules"]):
    file_name = rule.get("file", inventory["verification_file"])
    source = (WORKSPACE / file_name).read_text()
    lines = source.splitlines()
    span = "\n".join(lines[rule["start_line"] - 1 : rule["end_line"]])
    normalized = " ".join(span.split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    rule_checks.append(
        {
            "index": index,
            "file": file_name,
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "attributes": rule["attributes"],
            "normalized_sha256": rule["normalized_sha256"],
            "source_rule_id": rule["source_rule_id"],
            "source_span_equals_inventory_text": span == rule["text"],
            "normalized_hash_recomputed": digest,
            "normalized_hash_matches": digest == rule["normalized_sha256"],
            "source_rule_id_matches": rule["source_rule_id"] == f"rule-{digest}",
            "text": rule["text"],
        }
    )

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
result = {
    "verification_file": inventory["verification_file"],
    "verification_sha256": inventory["verification_sha256"],
    "verification_module": inventory["verification_module"],
    "verification_modules": inventory["verification_modules"],
    "required_files_sha256": inventory.get("required_files_sha256", {}),
    "rule_count": len(inventory["rules"]),
    "manifest_rule_count": len(manifest["rules"]),
    "canonical_inventory_sha256": inventory["inventory_sha256"],
    "independently_recomputed_inventory_sha256": canonical_json_sha256(
        inventory["rules"]
    ),
    "manifest_inventory_sha256": manifest["inventory_sha256"],
    "inventory_hashes_match": (
        inventory["inventory_sha256"]
        == canonical_json_sha256(inventory["rules"])
        == manifest["inventory_sha256"]
    ),
    "identity_order_matches_exactly": canonical_ids == manifest_ids,
    "canonical_identity_count_unique": len(canonical_ids) == len(set(canonical_ids)),
    "manifest_identity_count_unique": len(manifest_ids) == len(set(manifest_ids)),
    "identity_sets_match": set(canonical_ids) == set(manifest_ids),
    "trusted_boundary_validation_rule_count": len(validated["rules"]),
    "trusted_boundary_validation_inventory_sha256": validated["inventory_sha256"],
    "rules": rule_checks,
}

print(json.dumps(result, indent=2, sort_keys=True))

if not (
    result["rule_count"] == result["manifest_rule_count"]
    and result["inventory_hashes_match"]
    and result["identity_order_matches_exactly"]
    and result["canonical_identity_count_unique"]
    and result["manifest_identity_count_unique"]
    and result["identity_sets_match"]
    and all(
        rule["source_span_equals_inventory_text"]
        and rule["normalized_hash_matches"]
        and rule["source_rule_id_matches"]
        for rule in rule_checks
    )
):
    raise SystemExit(1)
