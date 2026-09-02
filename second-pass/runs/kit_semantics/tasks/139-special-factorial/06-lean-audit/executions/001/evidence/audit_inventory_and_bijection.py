#!/usr/bin/env python3
"""Independent Stage 3 inventory and Stage 4 zero-obligation bijection audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, klean_export


STAGE1 = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
AUDIT_INPUT = Path("/audit-input.json")


inventory = k_rule_inventory.inventory_verification(STAGE1)
discovery = json.loads(DISCOVERY.read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
generator_manifest = json.loads((GENERATION / "generator-manifest.json").read_text())
obligation_map = json.loads((GENERATED / "obligation-map.json").read_text())
audit_input = json.loads(AUDIT_INPUT.read_text())

rules = inventory["rules"]
inventory_ids = [rule["source_rule_id"] for rule in rules]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]

rule_checks = []
for rule in rules:
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    rule_checks.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "module": rule["module"],
            "source_span": {
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
            },
            "normalized_sha256": rule["normalized_sha256"],
            "normalized_hash_recomputed": normalized_sha256,
            "hash_matches": normalized_sha256 == rule["normalized_sha256"],
            "source_rule_id_matches": (
                rule["source_rule_id"] == f"rule-{normalized_sha256}"
            ),
        }
    )

inventory_document = [
    {
        "source_rule_id": rule["source_rule_id"],
        "module": rule["module"],
        "start_line": rule["start_line"],
        "end_line": rule["end_line"],
        "normalized_sha256": rule["normalized_sha256"],
        "attributes": rule["attributes"],
        "text": rule["text"],
    }
    for rule in rules
]
inventory_hash_recomputed = k_rule_inventory.canonical_json_sha256(
    inventory_document
)

# This mapping is the auditor's classification, derived from the frozen source
# and operational semantics, not copied from the Stage 3 rationale strings.
independent_classifications = {
    "rule-76c9fee7d31c7b9af2772f9513ebc29daf766162032c70206947d10685c8ab71": "DEFINITION",
    "rule-56984dfdcdf0ba8c027875164046db3a50319cd8bde210cf5869ac4eb5483d0b": "DEFINITION",
    "rule-7e43f2e0797b8ac08b474026ab65d98ed66d18b24b058dc65450b65246cf00b5": "DEFINITION",
    "rule-110b740de92d5388806b355cf84cbe138a0ae279db89595139a60295681df25c": "DEFINITION",
}
observed_classifications = {
    rule["source_rule_id"]: rule["classification"]
    for rule in discovery["rules"]
}
domain_ids = [
    source_rule_id
    for source_rule_id in inventory_ids
    if independent_classifications[source_rule_id] == "DOMAIN_LEMMA"
]
obligation_ids = [
    obligation["source_rule_id"] for obligation in obligation_map["obligations"]
]

expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)
target_statement = klean_export.target_statement(GENERATED)

checks = {
    "verification_module": inventory["verification_module"] == "VERIFICATION",
    "local_module_closure": inventory["verification_modules"] == ["VERIFICATION"],
    "all_rule_hashes_recomputed": all(item["hash_matches"] for item in rule_checks),
    "all_source_rule_ids_recomputed": all(
        item["source_rule_id_matches"] for item in rule_checks
    ),
    "whole_inventory_hash_recomputed": (
        inventory_hash_recomputed == inventory["inventory_sha256"]
    ),
    "discovery_inventory_hash_matches": (
        discovery["inventory_sha256"] == inventory["inventory_sha256"]
    ),
    "discovery_ordered_identity_bijection": discovery_ids == inventory_ids,
    "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
    "discovery_ids_unique": len(discovery_ids) == len(set(discovery_ids)),
    "classification_key_set_exact": (
        set(independent_classifications) == set(inventory_ids)
    ),
    "independent_classifications_match": (
        observed_classifications == independent_classifications
    ),
    "true_domain_set_empty": domain_ids == [],
    "input_source_rules_exact": input_manifest["source_rules"] == [],
    "obligation_map_source_rules_exact": obligation_map["source_rules"] == [],
    "obligation_ids_exact": obligation_ids == domain_ids,
    "obligation_ids_unique": len(obligation_ids) == len(set(obligation_ids)),
    "no_vacuous_conjuncts": obligation_map["obligations"] == [],
    "no_trust_parameters": obligation_map["trust_parameters"] == [],
    "generator_count_exact": generator_manifest["obligation_count"] == 0,
    "expected_target_absent": expected_target_definition is None,
    "observed_target_absent": target_statement is None,
    "generator_target_absent": generator_manifest["target"] is None,
    "audit_input_target_absent": audit_input["resolution"]["target"] is None,
}

report = {
    "inventory_sha256": inventory["inventory_sha256"],
    "inventory_sha256_recomputed": inventory_hash_recomputed,
    "inventory_order": inventory_ids,
    "rule_checks": rule_checks,
    "independent_classifications": independent_classifications,
    "true_domain_rule_ids": domain_ids,
    "generated_obligation_ids": obligation_ids,
    "expected_target_definition": expected_target_definition,
    "observed_target": target_statement,
    "checks": checks,
    "failed_checks": sorted(name for name, passed in checks.items() if not passed),
}
print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(1 if report["failed_checks"] else 0)
