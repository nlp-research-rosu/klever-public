#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction using trusted code."""

from __future__ import annotations

import json
from pathlib import Path

from tools import k_rule_inventory


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")

computed = k_rule_inventory.inventory_verification(workspace)
discovery = json.loads(discovery_path.read_text())

expected_projection = {
    "schema_version": computed["schema_version"],
    "inventory_sha256": computed["inventory_sha256"],
    "rules": computed["rules"],
}

print("COMPUTED_INVENTORY")
print(json.dumps(computed, indent=2, sort_keys=True))
print("PROTECTED_DISCOVERY")
print(json.dumps(discovery, indent=2, sort_keys=True))

assert discovery == expected_projection, (
    "protected discovery is not the exact ordered projection of the "
    "reconstructed inventory"
)

rules = computed["rules"]
ids = [entry["source_rule_id"] for entry in rules]
hashes = [entry["normalized_sha256"] for entry in rules]
assert len(ids) == len(set(ids)), "duplicate source_rule_id"
assert len(hashes) == len(set(hashes)), "duplicate normalized rule hash"
assert computed["inventory_sha256"] == k_rule_inventory.canonical_json_sha256(rules)

print("BIJECTIVE_ORDERED_COMPARISON: PASS")
print(f"RULE_COUNT: {len(rules)}")
