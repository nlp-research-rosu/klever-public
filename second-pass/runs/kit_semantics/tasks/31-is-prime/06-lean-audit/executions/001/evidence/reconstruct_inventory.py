#!/usr/bin/env python3
"""Independent Stage 1 inventory reconstruction and Stage 3 bijection checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


def main() -> None:
    inventory = inventory_verification(WORKSPACE)
    discovery = json.loads(DISCOVERY.read_text())
    source_lines = (WORKSPACE / "verification.k").read_text().splitlines()

    independent_rule_checks = []
    for rule in inventory["rules"]:
        span_text = "\n".join(
            source_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        normalized = " ".join(rule["text"].split())
        normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
        checks = {
            "source_rule_id": rule["source_rule_id"],
            "span_text_exact": span_text == rule["text"],
            "normalized_sha256_recomputed": normalized_sha256,
            "normalized_sha256_exact": normalized_sha256
            == rule["normalized_sha256"],
            "source_rule_id_exact": rule["source_rule_id"]
            == f"rule-{normalized_sha256}",
        }
        independent_rule_checks.append(checks)

    discovered_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
    inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
    result = {
        "inventory": inventory,
        "independent_rule_checks": independent_rule_checks,
        "inventory_hash_recomputed": canonical_json_sha256(inventory["rules"]),
        "inventory_hash_internal_exact": canonical_json_sha256(inventory["rules"])
        == inventory["inventory_sha256"],
        "protected_inventory_hash_exact": discovery["inventory_sha256"]
        == inventory["inventory_sha256"],
        "ordered_identity_bijection": discovered_ids == inventory_ids,
        "protected_ids_unique": len(discovered_ids) == len(set(discovered_ids)),
        "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
        "protected_rule_count": len(discovered_ids),
        "inventory_rule_count": len(inventory_ids),
    }
    required = [
        result["inventory_hash_internal_exact"],
        result["protected_inventory_hash_exact"],
        result["ordered_identity_bijection"],
        result["protected_ids_unique"],
        result["inventory_ids_unique"],
        all(
            check["span_text_exact"]
            and check["normalized_sha256_exact"]
            and check["source_rule_id_exact"]
            for check in independent_rule_checks
        ),
    ]
    result["all_checks_pass"] = all(required)
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
