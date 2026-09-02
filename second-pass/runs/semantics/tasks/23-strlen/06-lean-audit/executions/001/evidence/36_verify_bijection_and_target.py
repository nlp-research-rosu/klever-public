#!/usr/bin/env python3
"""Independent Stage 3 partition and Stage 4 obligation/target checks."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools import k_rule_inventory, klean_export


WORKSPACE = Path("/reference/k-proof")
DISCOVERY_PATH = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"

inventory = k_rule_inventory.inventory_verification(WORKSPACE)
discovery = json.loads(DISCOVERY_PATH.read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
generator_manifest = json.loads((GENERATION / "generator-manifest.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
preflight = json.loads((GENERATION / "preflight.json").read_text())
obligation_map = json.loads((GENERATED / "obligation-map.json").read_text())
audit_input = json.loads(Path("/audit-input.json").read_text())["resolution"]

# These roles are the auditor's source/semantics judgment, not copied from Stage 3.
independent_roles = {
    "rule-b71ea096f6e92dea97adefa58c521bb4aab0f25d49e84fa784b5a0cb3ceee82d": "DEFINITION",
    "rule-b40bd3d53d30e1797dff4bda42d1500c65a0af4579226f8b93f6d759be42af3f": "OPERATIONAL_RULE",
}
ordered_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
true_domain_ids = [
    rule_id
    for rule_id in ordered_ids
    if independent_roles[rule_id] == "DOMAIN_LEMMA"
]
manifest_roles = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}

input_partitions = {
    "DEFINITION": [entry["source_rule_id"] for entry in input_manifest["definitions"]],
    "OPERATIONAL_RULE": [
        entry["source_rule_id"] for entry in input_manifest["operational_rules"]
    ],
    "PROVED_DERIVED_LEMMA": [
        entry["source_rule_id"] for entry in input_manifest["proved_derived_lemmas"]
    ],
    "DOMAIN_LEMMA": [
        entry["source_rule_id"] for entry in input_manifest["source_rules"]
    ],
}
expected_partitions = {
    role: [
        rule_id for rule_id in ordered_ids if independent_roles[rule_id] == role
    ]
    for role in (
        "DEFINITION",
        "OPERATIONAL_RULE",
        "PROVED_DERIVED_LEMMA",
        "DOMAIN_LEMMA",
    )
}

lean_texts = {
    path.relative_to(GENERATED).as_posix(): path.read_text()
    for path in GENERATED.rglob("*.lean")
}
raw_targets = sum(
    len(re.findall(r"(?m)^\s*def\s+targetStatement\b", text))
    for text in lean_texts.values()
)
proof_finals = sum(text.count("Proof.final") for text in lean_texts.values())
obligation_ids = [
    entry.get("source_rule_id")
    for entry in obligation_map["obligations"]
]

checks = {
    "independent_roles_cover_inventory_in_order": (
        list(independent_roles) == ordered_ids
    ),
    "stage3_roles_match_independent_roles": (
        manifest_roles == independent_roles
    ),
    "input_manifest_partition_matches_independent_roles": (
        input_partitions == expected_partitions
    ),
    "true_domain_set_is_empty": true_domain_ids == [],
    "obligation_source_rules_equal_true_domain_set": (
        [
            entry["source_rule_id"]
            for entry in obligation_map["source_rules"]
        ]
        == true_domain_ids
    ),
    "obligations_biject_true_domain_set": (
        obligation_ids == true_domain_ids
        and len(obligation_ids) == len(set(obligation_ids))
    ),
    "no_vacuous_generated_conjunct": obligation_map["obligations"] == [],
    "no_trust_parameters_without_obligations": (
        obligation_map["trust_parameters"] == []
    ),
    "all_obligation_counts_zero": (
        generator_manifest["obligation_count"]
        == export_result["obligation_count"]
        == preflight["obligation_count"]
        == audit_input["stage4_preflight"]["obligation_count"]
        == 0
    ),
    "all_statuses_no_obligations": (
        export_result["status"]
        == preflight["status"]
        == audit_input["stage4_preflight"]["status"]
        == audit_input["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
    ),
    "expected_target_definition_absent": (
        klean_export.expected_target_definition(obligation_map) is None
    ),
    "trusted_target_parser_finds_no_target": (
        klean_export.target_statement(GENERATED) is None
    ),
    "independent_source_scan_finds_no_target": raw_targets == 0,
    "no_proof_final_in_generated_project": proof_finals == 0,
    "all_target_bindings_null": (
        generator_manifest["target"]
        is export_result.get("target")
        is preflight["target"]
        is audit_input["target"]
        is audit_input["stage4_preflight"]["target"]
        is None
    ),
    "stage5_absent": (
        audit_input["mode"] == "CLASSIFICATION_ONLY"
        and audit_input["lean_workspace"] is None
        and audit_input["lean_invocation"] is None
        and audit_input["stage5_result"] is None
    ),
}

print(
    json.dumps(
        {
            "all_checks_pass": all(checks.values()),
            "checks": checks,
            "ordered_inventory_ids": ordered_ids,
            "independent_roles": independent_roles,
            "true_domain_ids": true_domain_ids,
            "input_partitions": input_partitions,
            "obligation_ids": obligation_ids,
            "raw_target_declaration_count": raw_targets,
            "proof_final_reference_count": proof_finals,
        },
        indent=2,
        sort_keys=True,
    )
)
