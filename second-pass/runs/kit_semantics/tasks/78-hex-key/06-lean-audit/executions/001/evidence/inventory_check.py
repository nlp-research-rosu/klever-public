#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction and bijection report."""

from __future__ import annotations

import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(workspace)
discovery = json.loads(discovery_path.read_text(encoding="utf-8"))

rules = inventory["rules"]
classified = discovery.get("rules")
if not isinstance(classified, list):
    classified = []

inventory_ids = [rule["source_rule_id"] for rule in rules]
classified_ids = [entry.get("source_rule_id") for entry in classified]

checks = {
    "inventory_rule_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
    "classified_rule_ids_unique": len(classified_ids) == len(set(classified_ids)),
    "same_count": len(rules) == len(classified),
    "same_ordered_identities": inventory_ids == classified_ids,
    "same_inventory_hash": (
        inventory["inventory_sha256"] == discovery.get("inventory_sha256")
    ),
    "no_omissions": set(inventory_ids) <= set(classified_ids),
    "no_extras": set(classified_ids) <= set(inventory_ids),
    "all_classifications_accounted": all(
        entry.get("classification")
        in {
            "DEFINITION",
            "OPERATIONAL_RULE",
            "PROVED_DERIVED_LEMMA",
            "DOMAIN_LEMMA",
        }
        and isinstance(entry.get("rationale"), str)
        and bool(entry["rationale"].strip())
        for entry in classified
    ),
}

print(json.dumps({"reconstructed_inventory": inventory}, indent=2, sort_keys=True))
print(json.dumps({"discovery": discovery}, indent=2, sort_keys=True))
print(json.dumps({"bijection_checks": checks}, indent=2, sort_keys=True))
print("BIJECTION_PASS", all(checks.values()))
