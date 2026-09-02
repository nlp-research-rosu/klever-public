#!/usr/bin/env python3
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification

workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]

result = {
    "inventory": inventory,
    "manifest_inventory_sha256": manifest.get("inventory_sha256"),
    "canonical_ids": canonical_ids,
    "manifest_ids": manifest_ids,
    "same_order": canonical_ids == manifest_ids,
    "canonical_unique": len(canonical_ids) == len(set(canonical_ids)),
    "manifest_unique": len(manifest_ids) == len(set(manifest_ids)),
    "omitted_from_manifest": [
        source_rule_id
        for source_rule_id in canonical_ids
        if source_rule_id not in set(manifest_ids)
    ],
    "extra_in_manifest": [
        source_rule_id
        for source_rule_id in manifest_ids
        if source_rule_id not in set(canonical_ids)
    ],
    "inventory_hash_matches": (
        inventory["inventory_sha256"] == manifest.get("inventory_sha256")
    ),
    "bijection_and_order_pass": (
        canonical_ids == manifest_ids
        and len(canonical_ids) == len(set(canonical_ids))
        and inventory["inventory_sha256"] == manifest.get("inventory_sha256")
    ),
}

print(json.dumps(result, indent=2, sort_keys=True))
