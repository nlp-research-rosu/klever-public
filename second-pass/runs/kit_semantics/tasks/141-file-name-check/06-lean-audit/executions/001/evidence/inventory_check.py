#!/usr/bin/env python3
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(WORKSPACE)
validated = validate_trust_boundary(WORKSPACE, DISCOVERY)
discovery = json.loads(DISCOVERY.read_text())

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
classified_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
checks = {
    "inventory_hash_matches_manifest": (
        inventory["inventory_sha256"] == discovery["inventory_sha256"]
    ),
    "ordered_ids_match": canonical_ids == classified_ids,
    "canonical_ids_unique": len(canonical_ids) == len(set(canonical_ids)),
    "classified_ids_unique": len(classified_ids) == len(set(classified_ids)),
    "same_rule_count": len(canonical_ids) == len(classified_ids),
    "contract_validation_completed": True,
}
print(
    json.dumps(
        {
            "inventory": inventory,
            "manifest_rules": discovery["rules"],
            "validated_partition": {
                key: [
                    rule["source_rule_id"] for rule in validated[key]
                ]
                for key in (
                    "definitions",
                    "operational_rules",
                    "proved_derived_lemmas",
                    "domain_lemmas",
                )
            },
            "checks": checks,
            "overall": "PASS" if all(checks.values()) else "FAIL",
        },
        indent=2,
        sort_keys=True,
    )
)
raise SystemExit(0 if all(checks.values()) else 1)
