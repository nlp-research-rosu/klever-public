#!/usr/bin/env python3
import json
from pathlib import Path

from tools import k_rule_inventory, lemma_discovery_contract


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
manifest = json.loads(manifest_path.read_text())
reconstructed = k_rule_inventory.inventory_verification(workspace)
validated = lemma_discovery_contract.validate_trust_boundary(
    workspace, manifest_path
)

observed_records = manifest.get("rules", [])
observed_ids = [record.get("source_rule_id") for record in observed_records]
expected_ids = [record["source_rule_id"] for record in reconstructed["rules"]]
comparison = {
    "inventory_hash_matches": manifest.get("inventory_sha256")
    == reconstructed["inventory_sha256"],
    "ordered_ids_match": observed_ids == expected_ids,
    "no_duplicate_manifest_ids": len(observed_ids) == len(set(observed_ids)),
    "manifest_rule_count": len(observed_ids),
    "reconstructed_rule_count": len(expected_ids),
    "omitted_ids": [item for item in expected_ids if item not in observed_ids],
    "extra_ids": [item for item in observed_ids if item not in expected_ids],
}
comparison["bijection_and_order_match"] = all(
    comparison[key]
    for key in (
        "inventory_hash_matches",
        "ordered_ids_match",
        "no_duplicate_manifest_ids",
    )
) and comparison["manifest_rule_count"] == comparison["reconstructed_rule_count"]

print(json.dumps({
    "comparison": comparison,
    "reconstructed": reconstructed,
    "validated_trust_boundary": validated,
}, indent=2, sort_keys=True))
