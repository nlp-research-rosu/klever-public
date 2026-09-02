#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, "/reference")
from tools.k_rule_inventory import inventory_verification

workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(workspace)
discovery = json.loads(discovery_path.read_text())

inventory_rules = inventory["rules"]
discovery_rules = discovery["rules"]
inventory_ids = [entry["source_rule_id"] for entry in inventory_rules]
discovery_ids = [entry["source_rule_id"] for entry in discovery_rules]
allowed = {
    "DEFINITION",
    "OPERATIONAL_RULE",
    "PROVED_DERIVED_LEMMA",
    "DOMAIN_LEMMA",
}

checks = {
    "schema_version_is_2": discovery.get("schema_version") == 2,
    "inventory_sha256_matches": (
        discovery.get("inventory_sha256") == inventory["inventory_sha256"]
    ),
    "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
    "discovery_ids_unique": len(discovery_ids) == len(set(discovery_ids)),
    "same_rule_count": len(inventory_ids) == len(discovery_ids),
    "same_ids_same_order": inventory_ids == discovery_ids,
    "no_omitted_rules": set(inventory_ids) <= set(discovery_ids),
    "no_extra_rules": set(discovery_ids) <= set(inventory_ids),
    "all_classifications_accounted": all(
        entry.get("classification") in allowed for entry in discovery_rules
    ),
    "all_rationales_nonempty": all(
        isinstance(entry.get("rationale"), str) and bool(entry["rationale"].strip())
        for entry in discovery_rules
    ),
}

result = {
    "trusted_reconstruction": inventory,
    "discovery_order": [
        {
            "source_rule_id": entry["source_rule_id"],
            "classification": entry["classification"],
        }
        for entry in discovery_rules
    ],
    "checks": checks,
    "all_checks_pass": all(checks.values()),
}
print(json.dumps(result, indent=2, sort_keys=True))
