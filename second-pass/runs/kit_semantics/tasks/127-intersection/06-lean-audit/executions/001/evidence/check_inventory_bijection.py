#!/usr/bin/env python3
"""Strictly compare trusted inventory reconstruction with Stage 3 identities."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


def main() -> int:
    inventory = inventory_verification(Path("/reference/k-proof"))
    discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
    rules = inventory["rules"]
    classifications = discovery["rules"]
    inventory_ids = [rule["source_rule_id"] for rule in rules]
    discovery_ids = [rule["source_rule_id"] for rule in classifications]

    checks = {
        "schema_version": discovery.get("schema_version")
        == inventory.get("schema_version"),
        "inventory_sha256": discovery.get("inventory_sha256")
        == inventory.get("inventory_sha256"),
        "inventory_unique": len(inventory_ids) == len(set(inventory_ids)),
        "discovery_unique": len(discovery_ids) == len(set(discovery_ids)),
        "same_count": len(inventory_ids) == len(discovery_ids),
        "same_ordered_identities": inventory_ids == discovery_ids,
        "same_identity_set": set(inventory_ids) == set(discovery_ids),
    }
    allowed_keys = {"source_rule_id", "classification", "rationale"}
    checks["classification_entry_keys"] = all(
        set(entry) == allowed_keys for entry in classifications
    )

    print(f"verification_file={inventory['verification_file']}")
    print(f"verification_sha256={inventory['verification_sha256']}")
    print(f"verification_module={inventory['verification_module']}")
    print(f"verification_modules={inventory['verification_modules']}")
    print(f"inventory_sha256={inventory['inventory_sha256']}")
    print(f"rule_count={len(rules)}")
    for index, (rule, classified) in enumerate(
        zip(rules, classifications), start=1
    ):
        normalized_text = " ".join(rule["text"].split())
        normalized = hashlib.sha256(normalized_text.encode()).hexdigest()
        hash_ok = normalized == rule["normalized_sha256"]
        id_ok = (
            rule["source_rule_id"]
            == f"rule-{rule['normalized_sha256']}"
        )
        print(
            f"{index:02d} {rule['source_rule_id']} "
            f"{rule['module']}:{rule['start_line']}-{rule['end_line']} "
            f"attributes={rule['attributes']} "
            f"classification={classified['classification']} "
            f"normalized_hash={'MATCH' if hash_ok else 'MISMATCH'} "
            f"id_hash={'MATCH' if id_ok else 'MISMATCH'}"
        )
        checks[f"rule_{index:02d}_normalized_hash"] = hash_ok
        checks[f"rule_{index:02d}_id_hash"] = id_ok

    for name, ok in checks.items():
        print(f"{name}: {'PASS' if ok else 'FAIL'}")
    overall = all(checks.values())
    print("OVERALL:", "PASS" if overall else "FAIL")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
