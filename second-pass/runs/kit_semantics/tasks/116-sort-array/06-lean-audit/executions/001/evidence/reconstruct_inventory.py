#!/usr/bin/env python3
"""Reconstruct and compare the frozen verification-module rule inventory."""

from __future__ import annotations

import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


inventory = inventory_verification(WORKSPACE)
discovery = json.loads(DISCOVERY.read_text())

reconstructed_rules = inventory["rules"]
classified_rules = discovery["rules"]
reconstructed_ids = [rule["source_rule_id"] for rule in reconstructed_rules]
classified_ids = [rule["source_rule_id"] for rule in classified_rules]

checks = {
    "inventory_hash_matches": (
        inventory["inventory_sha256"] == discovery["inventory_sha256"]
    ),
    "ordered_identity_bijection": reconstructed_ids == classified_ids,
    "reconstructed_ids_unique": len(reconstructed_ids) == len(set(reconstructed_ids)),
    "classified_ids_unique": len(classified_ids) == len(set(classified_ids)),
    "every_id_commits_to_normalized_hash": all(
        rule["source_rule_id"] == f"rule-{rule['normalized_sha256']}"
        for rule in reconstructed_rules
    ),
    "every_rule_classified_once": (
        len(reconstructed_rules) == len(classified_rules)
        and set(reconstructed_ids) == set(classified_ids)
    ),
}

print(
    json.dumps(
        {
            "reconstructed_inventory": inventory,
            "discovery_inventory_sha256": discovery["inventory_sha256"],
            "classified_rules": classified_rules,
            "checks": checks,
            "overall": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
