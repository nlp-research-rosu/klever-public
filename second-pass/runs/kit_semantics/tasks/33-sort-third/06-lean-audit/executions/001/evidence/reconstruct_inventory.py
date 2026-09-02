#!/usr/bin/env python3
"""Independently reconstruct the Stage 1 inventory with trusted code."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "/reference")
from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
inventory = inventory_verification(workspace)
discovery = json.loads(discovery_path.read_text())

classified = discovery["rules"]
reconstructed = inventory["rules"]
classified_ids = [entry["source_rule_id"] for entry in classified]
reconstructed_ids = [entry["source_rule_id"] for entry in reconstructed]

comparison = {
    "reconstructed_rule_count": len(reconstructed),
    "classified_rule_count": len(classified),
    "reconstructed_unique_ids": len(set(reconstructed_ids)),
    "classified_unique_ids": len(set(classified_ids)),
    "identity_order_equal": reconstructed_ids == classified_ids,
    "inventory_hash_equal": (
        inventory["inventory_sha256"] == discovery["inventory_sha256"]
    ),
    "unclassified_reconstructed_ids": sorted(
        set(reconstructed_ids) - set(classified_ids)
    ),
    "extra_classified_ids": sorted(
        set(classified_ids) - set(reconstructed_ids)
    ),
}

print("RECONSTRUCTED_INVENTORY")
print(json.dumps(inventory, indent=2, sort_keys=True))
print("DISCOVERY_CLASSIFICATIONS")
print(json.dumps(classified, indent=2, sort_keys=True))
print("BIJECTIVE_COMPARISON")
print(json.dumps(comparison, indent=2, sort_keys=True))

if not all(
    (
        comparison["reconstructed_rule_count"]
        == comparison["classified_rule_count"],
        comparison["reconstructed_unique_ids"]
        == comparison["reconstructed_rule_count"],
        comparison["classified_unique_ids"] == comparison["classified_rule_count"],
        comparison["identity_order_equal"],
        comparison["inventory_hash_equal"],
        not comparison["unclassified_reconstructed_ids"],
        not comparison["extra_classified_ids"],
    )
):
    raise SystemExit(1)
