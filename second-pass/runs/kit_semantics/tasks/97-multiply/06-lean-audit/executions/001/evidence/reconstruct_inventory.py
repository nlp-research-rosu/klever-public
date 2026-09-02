#!/usr/bin/env python3
import json
from pathlib import Path

from tools import k_rule_inventory, lemma_discovery_contract


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")

inventory = k_rule_inventory.inventory_verification(WORKSPACE)
manifest = json.loads(DISCOVERY.read_text())
validated = lemma_discovery_contract.validate_trust_boundary(
    WORKSPACE, DISCOVERY
)

checks = {
    "schema_version": inventory["schema_version"] == manifest["schema_version"],
    "inventory_sha256": inventory["inventory_sha256"] == manifest["inventory_sha256"],
    "rule_count": len(inventory["rules"]) == len(manifest["rules"]),
    "rule_identity_order": [
        rule["source_rule_id"] for rule in inventory["rules"]
    ] == [rule["source_rule_id"] for rule in manifest["rules"]],
    "unique_inventory_ids": len({
        rule["source_rule_id"] for rule in inventory["rules"]
    }) == len(inventory["rules"]),
    "unique_manifest_ids": len({
        rule["source_rule_id"] for rule in manifest["rules"]
    }) == len(manifest["rules"]),
    "validated_contract_inventory_matches_reconstruction": all(
        validated[key] == inventory[key]
        for key in (
            "schema_version",
            "verification_file",
            "verification_sha256",
            "verification_module",
            "verification_modules",
            "rules",
            "inventory_sha256",
        )
    ),
    "validated_classification_partition_is_empty": all(
        validated[key] == []
        for key in (
            "definitions",
            "operational_rules",
            "proved_derived_lemmas",
            "domain_lemmas",
        )
    ),
}

print(json.dumps({
    "reconstructed_inventory": inventory,
    "protected_manifest": manifest,
    "bijection_checks": checks,
    "all_checks_match": all(checks.values()),
}, indent=2, sort_keys=True))
raise SystemExit(0 if all(checks.values()) else 1)
