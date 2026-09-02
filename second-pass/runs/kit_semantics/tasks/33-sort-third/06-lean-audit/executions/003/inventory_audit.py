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

inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
discovery_ids = [entry["source_rule_id"] for entry in discovery["rules"]]

comparison = {
    "inventory_hash_matches": (
        inventory["inventory_sha256"] == discovery.get("inventory_sha256")
    ),
    "identity_order_matches": inventory_ids == discovery_ids,
    "inventory_count": len(inventory_ids),
    "discovery_count": len(discovery_ids),
    "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
    "discovery_ids_unique": len(discovery_ids) == len(set(discovery_ids)),
    "omitted_from_discovery": sorted(set(inventory_ids) - set(discovery_ids)),
    "extra_in_discovery": sorted(set(discovery_ids) - set(inventory_ids)),
}

print("RECONSTRUCTED_INVENTORY")
print(json.dumps(inventory, indent=2, sort_keys=True))
print("BIJECTIVE_COMPARISON")
print(json.dumps(comparison, indent=2, sort_keys=True))

if not all(
    (
        comparison["inventory_hash_matches"],
        comparison["identity_order_matches"],
        comparison["inventory_ids_unique"],
        comparison["discovery_ids_unique"],
        not comparison["omitted_from_discovery"],
        not comparison["extra_in_discovery"],
    )
):
    raise SystemExit(1)
