#!/usr/bin/env python3
"""Independent Stage 3 structural reconstruction using the trusted inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
inventory = inventory_verification(workspace)
discovery = json.loads(discovery_path.read_text())

rules = inventory["rules"]
entries = discovery["rules"]
canonical_ids = [rule["source_rule_id"] for rule in rules]
discovery_ids = [entry["source_rule_id"] for entry in entries]

per_rule = []
for index, rule in enumerate(rules):
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    source_rule_id = f"rule-{normalized_sha256}"
    per_rule.append(
        {
            "index": index,
            "module": rule["module"],
            "source_span": {
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
            },
            "attributes": rule["attributes"],
            "normalized_source": normalized,
            "recomputed_normalized_sha256": normalized_sha256,
            "inventory_normalized_sha256": rule["normalized_sha256"],
            "recomputed_source_rule_id": source_rule_id,
            "inventory_source_rule_id": rule["source_rule_id"],
            "classification": entries[index]["classification"]
            if index < len(entries)
            else None,
            "normalized_hash_match": normalized_sha256
            == rule["normalized_sha256"],
            "source_rule_id_match": source_rule_id == rule["source_rule_id"],
        }
    )

result = {
    "verification_file": inventory["verification_file"],
    "verification_sha256": inventory["verification_sha256"],
    "verification_module": inventory["verification_module"],
    "local_module_closure": inventory["verification_modules"],
    "rule_count": len(rules),
    "discovery_rule_count": len(entries),
    "canonical_source_rule_ids": canonical_ids,
    "discovery_source_rule_ids": discovery_ids,
    "same_order": canonical_ids == discovery_ids,
    "canonical_ids_unique": len(set(canonical_ids)) == len(canonical_ids),
    "discovery_ids_unique": len(set(discovery_ids)) == len(discovery_ids),
    "same_id_set": set(canonical_ids) == set(discovery_ids),
    "recomputed_inventory_sha256": canonical_json_sha256(rules),
    "trusted_inventory_sha256": inventory["inventory_sha256"],
    "discovery_inventory_sha256": discovery["inventory_sha256"],
    "all_inventory_hashes_match": canonical_json_sha256(rules)
    == inventory["inventory_sha256"]
    == discovery["inventory_sha256"],
    "rules": per_rule,
}

print(json.dumps(result, indent=2, sort_keys=True))
