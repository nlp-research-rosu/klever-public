#!/usr/bin/env python3
"""Independent audit wrapper around the trusted canonical rule inventory."""

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

    reconstructed = []
    field_errors = []
    for index, rule in enumerate(inventory["rules"]):
        span_text = "\n".join(
            source_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        normalized = " ".join(span_text.split())
        normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
        checks = {
            "text_matches_span": span_text == rule["text"],
            "normalized_sha256_matches": normalized_sha256
            == rule["normalized_sha256"],
            "source_rule_id_matches": rule["source_rule_id"]
            == f"rule-{normalized_sha256}",
        }
        if not all(checks.values()):
            field_errors.append({"index": index, "checks": checks})
        reconstructed.append(rule)

    canonical_inventory_hash = canonical_json_sha256(reconstructed)
    inventory_ids = [rule["source_rule_id"] for rule in reconstructed]
    discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
    result = {
        "trusted_inventory": inventory,
        "independent_span_hash_checks": {
            "count": len(reconstructed),
            "errors": field_errors,
            "all_pass": not field_errors,
        },
        "bijection_and_order": {
            "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
            "discovery_ids_unique": len(discovery_ids) == len(set(discovery_ids)),
            "same_count": len(inventory_ids) == len(discovery_ids),
            "same_set": set(inventory_ids) == set(discovery_ids),
            "same_order": inventory_ids == discovery_ids,
        },
        "hash_checks": {
            "independent_inventory_sha256": canonical_inventory_hash,
            "trusted_inventory_sha256": inventory["inventory_sha256"],
            "discovery_inventory_sha256": discovery["inventory_sha256"],
            "all_equal": canonical_inventory_hash
            == inventory["inventory_sha256"]
            == discovery["inventory_sha256"],
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
