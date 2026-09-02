#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction and exact-order comparison."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


inventory = inventory_verification(WORKSPACE)
discovery = json.loads(DISCOVERY.read_text())
rules = inventory["rules"]
entries = discovery["rules"]

print("RECONSTRUCTED_INVENTORY")
print(json.dumps(inventory, indent=2, sort_keys=True))
print("INDEPENDENT_COMPARISON")
print(f"verification_file_sha256={hashlib.sha256((WORKSPACE / 'verification.k').read_bytes()).hexdigest()}")
print(f"recomputed_inventory_sha256={canonical_json_sha256(rules)}")
print(f"recorded_inventory_sha256={discovery.get('inventory_sha256')}")
print(f"canonical_rule_count={len(rules)}")
print(f"classified_rule_count={len(entries)}")

canonical_ids = [rule["source_rule_id"] for rule in rules]
classified_ids = [entry.get("source_rule_id") for entry in entries]
print(f"canonical_ids={json.dumps(canonical_ids)}")
print(f"classified_ids={json.dumps(classified_ids)}")
print(f"exact_order_match={canonical_ids == classified_ids}")
print(f"canonical_ids_unique={len(canonical_ids) == len(set(canonical_ids))}")
print(f"classified_ids_unique={len(classified_ids) == len(set(classified_ids))}")
print(f"omitted_ids={json.dumps([item for item in canonical_ids if item not in classified_ids])}")
print(f"extra_ids={json.dumps([item for item in classified_ids if item not in canonical_ids])}")

all_rule_checks = True
for index, (rule, entry) in enumerate(zip(rules, entries, strict=False)):
    normalized = " ".join(rule["text"].split())
    normalized_hash = hashlib.sha256(normalized.encode()).hexdigest()
    expected_id = f"rule-{normalized_hash}"
    span_text = "\n".join(
        (WORKSPACE / "verification.k").read_text().splitlines()[
            rule["start_line"] - 1 : rule["end_line"]
        ]
    )
    checks = {
        "source_rule_id_from_normalized_hash": rule["source_rule_id"] == expected_id,
        "normalized_sha256": rule["normalized_sha256"] == normalized_hash,
        "source_span_text": span_text == rule["text"],
        "classified_identity": rule["source_rule_id"] == entry.get("source_rule_id"),
    }
    all_rule_checks = all_rule_checks and all(checks.values())
    print(
        "RULE_CHECK "
        + json.dumps(
            {
                "index": index,
                "module": rule["module"],
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
                "normalized_source": normalized,
                "recomputed_normalized_sha256": normalized_hash,
                "recomputed_source_rule_id": expected_id,
                "recorded_classification": entry.get("classification"),
                "checks": checks,
            },
            sort_keys=True,
        )
    )

overall = (
    discovery.get("schema_version") == 2
    and inventory["inventory_sha256"] == discovery.get("inventory_sha256")
    and canonical_ids == classified_ids
    and len(canonical_ids) == len(set(canonical_ids))
    and len(classified_ids) == len(set(classified_ids))
    and all_rule_checks
)
print(f"BIJECTIVE_EXACT_ORDER_AND_HASH_MATCH={overall}")
