#!/usr/bin/env python3
"""Reconstruct and compare the protected Stage 3 rule inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


reconstructed = inventory_verification(WORKSPACE)
protected = json.loads(DISCOVERY.read_text())

print("RECONSTRUCTED INVENTORY")
print(json.dumps(reconstructed, indent=2, sort_keys=True))
print("\nPROTECTED DISCOVERY")
print(json.dumps(protected, indent=2, sort_keys=True))

classifications = protected.get("rules")
if not isinstance(classifications, list):
    raise SystemExit("FAIL: protected rules/classifications is not a list")

reconstructed_rules = reconstructed["rules"]
print("\nBIJECTIVE ORDERED COMPARISON")
print(f"reconstructed_count={len(reconstructed_rules)}")
print(f"classification_count={len(classifications)}")

for index, actual in enumerate(reconstructed_rules):
    normalized = " ".join(actual["text"].split())
    independently_hashed = hashlib.sha256(normalized.encode()).hexdigest()
    print(
        json.dumps(
            {
                "index": index,
                "source_rule_id": actual["source_rule_id"],
                "span": [actual["start_line"], actual["end_line"]],
                "normalized_hash_recomputed": independently_hashed,
                "normalized_hash_matches": independently_hashed
                == actual["normalized_sha256"],
                "source_rule_id_matches_hash": actual["source_rule_id"]
                == f"rule-{independently_hashed}",
            },
            sort_keys=True,
        )
    )

actual_ids = [entry["source_rule_id"] for entry in reconstructed_rules]
classified_ids = [entry.get("source_rule_id") for entry in classifications]
print(f"actual_ids_unique={len(actual_ids) == len(set(actual_ids))}")
print(f"classified_ids_unique={len(classified_ids) == len(set(classified_ids))}")
print(f"classification_ids_ordered_equal={actual_ids == classified_ids}")
print(f"classification_id_sets_equal={set(actual_ids) == set(classified_ids)}")

computed_inventory_hash = canonical_json_sha256(reconstructed_rules)
print(f"computed_inventory_sha256={computed_inventory_hash}")
print(f"tool_inventory_sha256={reconstructed['inventory_sha256']}")
print(f"protected_inventory_sha256={protected.get('inventory_sha256')}")
print(
    "inventory_hashes_equal="
    + str(
        computed_inventory_hash
        == reconstructed["inventory_sha256"]
        == protected.get("inventory_sha256")
    )
)

checks = [
    len(reconstructed_rules) == len(classifications),
    len(actual_ids) == len(set(actual_ids)),
    len(classified_ids) == len(set(classified_ids)),
    actual_ids == classified_ids,
    computed_inventory_hash
    == reconstructed["inventory_sha256"]
    == protected.get("inventory_sha256"),
]
print("\nRESULT=" + ("PASS" if all(checks) else "FAIL"))
raise SystemExit(0 if all(checks) else 1)
