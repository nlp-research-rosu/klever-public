#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction using the trusted inventory code."""

from __future__ import annotations

import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(workspace)
discovery = json.loads(discovery_path.read_text())

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]

checks = {
    "schema_version_matches": inventory["schema_version"] == discovery["schema_version"],
    "inventory_sha256_matches": inventory["inventory_sha256"] == discovery["inventory_sha256"],
    "same_ordered_source_rule_ids": inventory_ids == discovery_ids,
    "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
    "discovery_ids_unique": len(discovery_ids) == len(set(discovery_ids)),
    "no_omissions": set(inventory_ids) <= set(discovery_ids),
    "no_extras": set(discovery_ids) <= set(inventory_ids),
    "every_rule_classified_once": len(inventory_ids) == len(discovery_ids),
}

print("RECONSTRUCTED_INVENTORY")
print(json.dumps(inventory, indent=2, sort_keys=True))
print("\nDISCOVERY_CLASSIFICATIONS")
print(json.dumps(discovery, indent=2, sort_keys=True))
print("\nBIJECTION_CHECKS")
print(json.dumps(checks, indent=2, sort_keys=True))

if not all(checks.values()):
    raise SystemExit("inventory/discovery bijection failed")

print("INVENTORY_BIJECTION=PASS")
