#!/usr/bin/env python3
"""Independent structural comparison of frozen K inventory and Stage 3 JSON."""

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

facts = {
    "verification_file_sha256": inventory["verification_sha256"],
    "verification_module": inventory["verification_module"],
    "verification_modules": inventory["verification_modules"],
    "inventory_rule_count": len(inventory_ids),
    "discovery_rule_count": len(discovery_ids),
    "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
    "discovery_ids_unique": len(discovery_ids) == len(set(discovery_ids)),
    "ordered_ids_equal": inventory_ids == discovery_ids,
    "omitted_from_discovery": sorted(set(inventory_ids) - set(discovery_ids)),
    "extra_in_discovery": sorted(set(discovery_ids) - set(inventory_ids)),
    "reconstructed_inventory_sha256": inventory["inventory_sha256"],
    "recorded_inventory_sha256": discovery["inventory_sha256"],
    "inventory_hash_equal": (
        inventory["inventory_sha256"] == discovery["inventory_sha256"]
    ),
}

print(json.dumps(facts, indent=2))
print("ORDERED RULE RECORDS")
for index, (source, classified) in enumerate(
    zip(inventory["rules"], discovery["rules"], strict=True), start=1
):
    print(
        json.dumps(
            {
                "index": index,
                "source_rule_id": source["source_rule_id"],
                "normalized_sha256": source["normalized_sha256"],
                "module": source["module"],
                "span": [source["start_line"], source["end_line"]],
                "attributes": source["attributes"],
                "classification": classified["classification"],
            },
            sort_keys=True,
        )
    )

if not all(
    (
        facts["inventory_ids_unique"],
        facts["discovery_ids_unique"],
        facts["ordered_ids_equal"],
        facts["inventory_hash_equal"],
        not facts["omitted_from_discovery"],
        not facts["extra_in_discovery"],
    )
):
    raise SystemExit("STRUCTURAL_COMPARISON: FAIL")

print("STRUCTURAL_COMPARISON: PASS")
