#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


def main() -> int:
    inventory = inventory_verification(WORKSPACE)
    discovery = json.loads(DISCOVERY.read_text())
    source_lines = (WORKSPACE / "verification.k").read_text().splitlines()

    checks: dict[str, object] = {}
    rules = inventory["rules"]
    discovered_rules = discovery["rules"]
    inventory_ids = [rule["source_rule_id"] for rule in rules]
    discovery_ids = [rule["source_rule_id"] for rule in discovered_rules]

    per_rule = []
    for rule in rules:
        exact_span = "\n".join(
            source_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        normalized_hash = hashlib.sha256(
            " ".join(rule["text"].split()).encode()
        ).hexdigest()
        per_rule.append(
            {
                "source_rule_id": rule["source_rule_id"],
                "span_matches_frozen_source": exact_span == rule["text"],
                "recomputed_normalized_sha256": normalized_hash,
                "normalized_sha256_matches": (
                    normalized_hash == rule["normalized_sha256"]
                ),
                "source_rule_id_matches_hash": (
                    rule["source_rule_id"] == f"rule-{normalized_hash}"
                ),
            }
        )

    checks["inventory_rule_count"] = len(rules)
    checks["discovery_rule_count"] = len(discovered_rules)
    checks["inventory_ids_unique"] = len(inventory_ids) == len(set(inventory_ids))
    checks["discovery_ids_unique"] = len(discovery_ids) == len(set(discovery_ids))
    checks["ordered_identities_equal"] = inventory_ids == discovery_ids
    checks["omitted_from_discovery"] = sorted(set(inventory_ids) - set(discovery_ids))
    checks["extra_in_discovery"] = sorted(set(discovery_ids) - set(inventory_ids))
    checks["recomputed_inventory_sha256"] = canonical_json_sha256(rules)
    checks["inventory_self_hash_matches"] = (
        checks["recomputed_inventory_sha256"] == inventory["inventory_sha256"]
    )
    checks["discovery_inventory_hash_matches"] = (
        discovery["inventory_sha256"] == inventory["inventory_sha256"]
    )
    checks["every_rule_accounted_once"] = (
        len(rules) == len(discovered_rules)
        and inventory_ids == discovery_ids
        and checks["inventory_ids_unique"]
        and checks["discovery_ids_unique"]
    )
    checks["per_rule_recomputation"] = per_rule

    print(
        json.dumps(
            {
                "reconstructed_inventory": inventory,
                "protected_discovery": discovery,
                "bijection_and_hash_checks": checks,
            },
            indent=2,
            sort_keys=True,
        )
    )

    passed = (
        checks["every_rule_accounted_once"]
        and checks["inventory_self_hash_matches"]
        and checks["discovery_inventory_hash_matches"]
        and all(
            item["span_matches_frozen_source"]
            and item["normalized_sha256_matches"]
            and item["source_rule_id_matches_hash"]
            for item in per_rule
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
