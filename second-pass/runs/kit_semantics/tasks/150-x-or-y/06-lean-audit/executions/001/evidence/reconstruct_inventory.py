#!/usr/bin/env python3
"""Reconstruct and compare the frozen verification-module rule inventory."""

from __future__ import annotations

import json
from pathlib import Path

from tools.lemma_discovery_contract import validate_trust_boundary
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
validated = validate_trust_boundary(workspace, manifest_path)

rules = inventory["rules"]
entries = manifest["rules"]
canonical_ids = [rule["source_rule_id"] for rule in rules]
manifest_ids = [entry["source_rule_id"] for entry in entries]

checks = {
    "inventory_hash_recomputed_from_rule_documents": (
        canonical_json_sha256(rules) == inventory["inventory_sha256"]
    ),
    "inventory_hash_matches_protected_manifest": (
        inventory["inventory_sha256"] == manifest["inventory_sha256"]
    ),
    "identity_order_exact": canonical_ids == manifest_ids,
    "canonical_id_unique": len(canonical_ids) == len(set(canonical_ids)),
    "manifest_id_unique": len(manifest_ids) == len(set(manifest_ids)),
    "no_omissions": set(canonical_ids) <= set(manifest_ids),
    "no_extras": set(manifest_ids) <= set(canonical_ids),
    "same_rule_count": len(rules) == len(entries),
    "trusted_schema_and_partition_validation_passed": (
        sum(
            len(validated[key])
            for key in (
                "definitions",
                "operational_rules",
                "proved_derived_lemmas",
                "domain_lemmas",
            )
        )
        == len(rules)
    ),
    "all_classifications_accounted_for": (
        {
            entry["classification"]
            for entry in entries
        }
        <= {
            "DEFINITION",
            "OPERATIONAL_RULE",
            "PROVED_DERIVED_LEMMA",
            "DOMAIN_LEMMA",
        }
    ),
    "simplification_class_constraint_holds": all(
        "simplification" not in rule["attributes"]
        or entries[index]["classification"] in {"DEFINITION", "DOMAIN_LEMMA"}
        for index, rule in enumerate(rules)
    ),
}

result = {
    "workspace": str(workspace),
    "protected_manifest": str(manifest_path),
    "verification_file": inventory["verification_file"],
    "verification_sha256": inventory["verification_sha256"],
    "verification_module": inventory["verification_module"],
    "verification_modules": inventory["verification_modules"],
    "inventory_sha256": inventory["inventory_sha256"],
    "rules": rules,
    "protected_classifications_in_recorded_order": entries,
    "validated_partition_counts": {
        key: len(validated[key])
        for key in (
            "definitions",
            "operational_rules",
            "proved_derived_lemmas",
            "domain_lemmas",
        )
    },
    "checks": checks,
    "all_checks_pass": all(checks.values()),
}
print(json.dumps(result, indent=2, sort_keys=True))
