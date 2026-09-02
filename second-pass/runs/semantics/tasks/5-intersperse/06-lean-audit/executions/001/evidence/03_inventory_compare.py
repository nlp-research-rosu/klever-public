#!/usr/bin/env python3
"""Independent Stage 1 inventory reconstruction and Stage 3 identity audit."""

from __future__ import annotations

import json
from pathlib import Path

from tools import k_rule_inventory


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")

inventory = k_rule_inventory.inventory_verification(workspace)
discovery = json.loads(discovery_path.read_text())

rules = inventory["rules"]
classified = discovery["rules"]
observed_ids = [entry["source_rule_id"] for entry in rules]
classified_ids = [entry["source_rule_id"] for entry in classified]

checks = {
    "schema_version_is_2": discovery.get("schema_version") == 2,
    "inventory_hash_matches": (
        discovery.get("inventory_sha256") == inventory["inventory_sha256"]
    ),
    "same_rule_count": len(rules) == len(classified),
    "no_inventory_duplicates": len(observed_ids) == len(set(observed_ids)),
    "no_classification_duplicates": (
        len(classified_ids) == len(set(classified_ids))
    ),
    "ordered_identity_bijection": observed_ids == classified_ids,
    "identity_set_bijection": set(observed_ids) == set(classified_ids),
}

print("RECONSTRUCTED_INVENTORY")
print(json.dumps(inventory, indent=2, sort_keys=True))
print("STAGE3_ORDERED_CLASSIFICATIONS")
print(json.dumps(classified, indent=2, sort_keys=True))
print("BIJECTION_CHECKS")
print(json.dumps(checks, indent=2, sort_keys=True))

if not all(checks.values()):
    raise SystemExit("FAIL: Stage 3 is not bijective with reconstructed inventory")
print("PASS: Stage 3 identities are a duplicate-free ordered bijection")
