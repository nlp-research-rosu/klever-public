#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
validated = validate_trust_boundary(workspace, manifest_path)

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
unique_manifest_ids = set(manifest_ids)

comparisons = {
    "inventory_hash_matches": (
        inventory["inventory_sha256"] == manifest["inventory_sha256"]
    ),
    "identity_order_matches": canonical_ids == manifest_ids,
    "canonical_identity_count": len(canonical_ids),
    "manifest_identity_count": len(manifest_ids),
    "manifest_unique_identity_count": len(unique_manifest_ids),
    "omitted_ids": sorted(set(canonical_ids) - unique_manifest_ids),
    "extra_ids": sorted(unique_manifest_ids - set(canonical_ids)),
    "duplicate_ids": sorted(
        source_rule_id
        for source_rule_id in unique_manifest_ids
        if manifest_ids.count(source_rule_id) > 1
    ),
    "verification_sha256": inventory["verification_sha256"],
    "verification_module": inventory["verification_module"],
    "verification_modules": inventory["verification_modules"],
}

result = {
    "comparisons": comparisons,
    "inventory": inventory,
    "validated_classification_counts": {
        "DEFINITION": len(validated["definitions"]),
        "OPERATIONAL_RULE": len(validated["operational_rules"]),
        "PROVED_DERIVED_LEMMA": len(validated["proved_derived_lemmas"]),
        "DOMAIN_LEMMA": len(validated["domain_lemmas"]),
    },
}
result["bijection_and_order_pass"] = (
    comparisons["inventory_hash_matches"]
    and comparisons["identity_order_matches"]
    and not comparisons["omitted_ids"]
    and not comparisons["extra_ids"]
    and not comparisons["duplicate_ids"]
)
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["bijection_and_order_pass"] else 1)
