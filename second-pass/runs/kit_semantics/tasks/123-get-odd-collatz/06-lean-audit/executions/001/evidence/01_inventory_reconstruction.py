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

comparison = {
    "inventory_sha256_matches": (
        inventory["inventory_sha256"] == manifest.get("inventory_sha256")
    ),
    "rule_count": len(canonical_ids),
    "manifest_rule_count": len(manifest_ids),
    "exact_ordered_identity_match": canonical_ids == manifest_ids,
    "duplicate_canonical_ids": sorted(
        source_rule_id
        for source_rule_id in set(canonical_ids)
        if canonical_ids.count(source_rule_id) > 1
    ),
    "duplicate_manifest_ids": sorted(
        source_rule_id
        for source_rule_id in set(manifest_ids)
        if manifest_ids.count(source_rule_id) > 1
    ),
    "missing_from_manifest": [
        source_rule_id
        for source_rule_id in canonical_ids
        if source_rule_id not in manifest_ids
    ],
    "extra_in_manifest": [
        source_rule_id
        for source_rule_id in manifest_ids
        if source_rule_id not in canonical_ids
    ],
}

print(
    json.dumps(
        {"inventory": inventory, "manifest_comparison": comparison},
        indent=2,
        sort_keys=True,
    )
)
