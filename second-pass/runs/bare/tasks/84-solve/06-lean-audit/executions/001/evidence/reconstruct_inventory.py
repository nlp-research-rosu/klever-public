#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction and strict-order comparison."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, lemma_discovery_contract


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
verification_path = workspace / "verification.k"

inventory = k_rule_inventory.inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
validated = lemma_discovery_contract.validate_trust_boundary(
    workspace, manifest_path
)

source_lines = verification_path.read_text().splitlines()
per_rule_checks: list[dict[str, object]] = []
for rule in inventory["rules"]:
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    span_text = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    checks = {
        "source_rule_id": rule["source_rule_id"],
        "module": rule["module"],
        "start_line": rule["start_line"],
        "end_line": rule["end_line"],
        "span_text_exact": span_text == rule["text"],
        "normalized_sha256_recomputed": normalized_sha256,
        "normalized_sha256_matches": (
            normalized_sha256 == rule["normalized_sha256"]
        ),
        "source_rule_id_matches": (
            rule["source_rule_id"] == f"rule-{normalized_sha256}"
        ),
        "attributes": rule["attributes"],
        "text": rule["text"],
    }
    per_rule_checks.append(checks)

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
whole_inventory_recomputed = k_rule_inventory.canonical_json_sha256(
    inventory["rules"]
)
strict_comparison = {
    "canonical_rule_count": len(canonical_ids),
    "manifest_rule_count": len(manifest_ids),
    "canonical_ids_unique": len(canonical_ids) == len(set(canonical_ids)),
    "manifest_ids_unique": len(manifest_ids) == len(set(manifest_ids)),
    "missing_ids": [item for item in canonical_ids if item not in manifest_ids],
    "extra_ids": [item for item in manifest_ids if item not in canonical_ids],
    "identity_order_exact": canonical_ids == manifest_ids,
    "inventory_sha256_recomputed": whole_inventory_recomputed,
    "inventory_sha256_tool": inventory["inventory_sha256"],
    "inventory_sha256_manifest": manifest["inventory_sha256"],
    "inventory_hashes_match": (
        whole_inventory_recomputed
        == inventory["inventory_sha256"]
        == manifest["inventory_sha256"]
    ),
    "all_spans_exact": all(
        item["span_text_exact"] for item in per_rule_checks
    ),
    "all_rule_hashes_exact": all(
        item["normalized_sha256_matches"]
        and item["source_rule_id_matches"]
        for item in per_rule_checks
    ),
    "contract_validation_rule_count": len(validated["rules"]),
}

print("STRICT_COMPARISON")
print(json.dumps(strict_comparison, indent=2, sort_keys=True))
print("RECONSTRUCTED_RULES")
print(json.dumps(per_rule_checks, indent=2, sort_keys=True))
print("CANONICAL_INVENTORY")
print(json.dumps(inventory, indent=2, sort_keys=True))
