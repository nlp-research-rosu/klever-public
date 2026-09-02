#!/usr/bin/env python3
"""Reconstruct and bijectively compare the local verification rule closure."""

from __future__ import annotations

import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
MANIFEST_PATH = Path("/reference/lemma-discovery.json")
INVENTORY_OUTPUT = Path(
    "/audit-output/evidence/02-reconstructed-rule-inventory.json"
)
COMPARISON_OUTPUT = Path(
    "/audit-output/evidence/02-inventory-manifest-comparison.json"
)

inventory = inventory_verification(WORKSPACE)
validated = validate_trust_boundary(WORKSPACE, MANIFEST_PATH)
manifest = json.loads(MANIFEST_PATH.read_text())

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [entry["source_rule_id"] for entry in manifest["rules"]]
canonical_by_id = {
    rule["source_rule_id"]: rule for rule in inventory["rules"]
}
manifest_by_id = {
    entry["source_rule_id"]: entry for entry in manifest["rules"]
}

rows = []
for index, source_rule_id in enumerate(canonical_ids):
    source = canonical_by_id[source_rule_id]
    classified = manifest_by_id.get(source_rule_id)
    rows.append(
        {
            "index": index,
            "source_rule_id": source_rule_id,
            "module": source["module"],
            "start_line": source["start_line"],
            "end_line": source["end_line"],
            "normalized_sha256": source["normalized_sha256"],
            "attributes": source["attributes"],
            "manifest_classification": (
                classified["classification"] if classified else None
            ),
            "manifest_rationale": (
                classified["rationale"] if classified else None
            ),
        }
    )

checks = {
    "manifest_schema_version": manifest.get("schema_version") == 2,
    "inventory_hash": (
        manifest.get("inventory_sha256") == inventory["inventory_sha256"]
    ),
    "identity_order": manifest_ids == canonical_ids,
    "no_duplicate_manifest_ids": len(set(manifest_ids)) == len(manifest_ids),
    "no_duplicate_canonical_ids": len(set(canonical_ids)) == len(canonical_ids),
    "same_identity_set": set(manifest_ids) == set(canonical_ids),
    "same_rule_count": len(manifest_ids) == len(canonical_ids),
    "contract_validation": (
        validated["inventory_sha256"] == inventory["inventory_sha256"]
    ),
}
failed_checks = sorted(name for name, passed in checks.items() if not passed)

INVENTORY_OUTPUT.write_text(
    json.dumps(inventory, indent=2, sort_keys=True) + "\n"
)
result = {
    "checks": checks,
    "failed_checks": failed_checks,
    "verification_file": inventory["verification_file"],
    "verification_sha256": inventory["verification_sha256"],
    "verification_module": inventory["verification_module"],
    "verification_modules": inventory["verification_modules"],
    "inventory_sha256": inventory["inventory_sha256"],
    "rule_count": len(inventory["rules"]),
    "classification_counts": {
        "DEFINITION": len(validated["definitions"]),
        "OPERATIONAL_RULE": len(validated["operational_rules"]),
        "PROVED_DERIVED_LEMMA": len(validated["proved_derived_lemmas"]),
        "DOMAIN_LEMMA": len(validated["domain_lemmas"]),
    },
    "rules": rows,
}
COMPARISON_OUTPUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n"
)
print(json.dumps(result, indent=2, sort_keys=True))
if failed_checks:
    raise SystemExit(1)
