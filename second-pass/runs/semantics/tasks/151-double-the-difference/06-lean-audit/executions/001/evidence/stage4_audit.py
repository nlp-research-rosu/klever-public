#!/usr/bin/env python3
"""Independent Stage 4 manifest, obligation, and fixed-target audit."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, lemma_discovery_contract


K_WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


validated = lemma_discovery_contract.validate_trust_boundary(
    K_WORKSPACE, DISCOVERY
)
input_manifest = load_json(GENERATION / "input-manifest.json")
generator_manifest = load_json(GENERATION / "generator-manifest.json")
export_result = load_json(GENERATION / "export-result.json")
preflight = load_json(GENERATION / "preflight.json")
trust_inventory = load_json(GENERATION / "trust-inventory.json")
obligation_map = load_json(GENERATED / "obligation-map.json")
toolchain_lock = load_json(Path("/reference/klean-toolchain.lock.json"))

discovery_hash = sha256_file(DISCOVERY)
domain_rules = klean_export._domain_source_rules(
    validated, discovery_hash
)
resolution = klean_export.resolve_definition_closure(K_WORKSPACE)
_module, functions = klean_export.parse_verification(
    (K_WORKSPACE / "verification.k").read_text()
)
summary_functions = [
    {
        "name": function.name,
        "return_sort": function.ret,
        "argument_sorts": function.args,
    }
    for function in functions
]

expected_relative_k_files = [
    path.relative_to(K_WORKSPACE).as_posix()
    for path in resolution.required_files
]
recorded_relative_k_files = [
    Path(path).relative_to("/frozen-k").as_posix()
    for path in input_manifest["required_k_files"]
]

source_ids = [rule["source_rule_id"] for rule in domain_rules]
input_ids = [
    rule["source_rule_id"] for rule in input_manifest["source_rules"]
]
mapped_source_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]

raw_target_count = 0
for path in GENERATED.rglob("*.lean"):
    raw_target_count += len(
        re.findall(r"(?m)^\s*def\s+targetStatement\b", path.read_text())
    )
selected_target = klean_export.target_statement(GENERATED)
expected_target = klean_export.expected_target_definition(obligation_map)

result = {
    "input_manifest": {
        "schema_version_is_3": input_manifest["schema_version"] == 3,
        "problem_matches": (
            input_manifest["problem"] == "151-double-the-difference"
        ),
        "stage1_hashes_match": (
            input_manifest["frozen_input_sha256"]
            == input_manifest["stage1_workspace_sha256"]
            == klean_export.tree_digest(K_WORKSPACE)
        ),
        "discovery_hash_matches": (
            input_manifest["stage3_discovery_manifest_sha256"]
            == discovery_hash
        ),
        "verification_hash_matches": (
            input_manifest["verification_sha256"]
            == sha256_file(K_WORKSPACE / "verification.k")
        ),
        "verification_module_matches": (
            input_manifest["verification_module"]
            == validated["verification_module"]
        ),
        "syntax_module_matches": (
            input_manifest["syntax_module"] == resolution.syntax_module
        ),
        "inventory_hash_matches": (
            input_manifest["inventory_sha256"]
            == validated["inventory_sha256"]
        ),
        "required_k_files_match_after_mount_rebase": (
            recorded_relative_k_files == expected_relative_k_files
        ),
        "required_k_file_count": len(recorded_relative_k_files),
        "summary_functions_match": (
            input_manifest["summary_functions"] == summary_functions
        ),
        "definitions_match_validated_inventory": (
            input_manifest["definitions"] == validated["definitions"]
        ),
        "operational_rules_match_validated_inventory": (
            input_manifest["operational_rules"]
            == validated["operational_rules"]
        ),
        "proved_derived_lemmas_match_validated_inventory": (
            input_manifest["proved_derived_lemmas"]
            == validated["proved_derived_lemmas"]
        ),
        "domain_source_rules_match_validated_inventory": (
            input_manifest["source_rules"] == domain_rules
        ),
    },
    "obligation_bijection": {
        "true_domain_rule_ids": source_ids,
        "input_manifest_rule_ids": input_ids,
        "obligation_map_source_rule_ids": mapped_source_ids,
        "obligation_rule_ids": obligation_ids,
        "ordered_bijection": (
            source_ids == input_ids == mapped_source_ids == obligation_ids
        ),
        "no_duplicates": len(obligation_ids) == len(set(obligation_ids)),
        "obligation_count": len(obligation_map["obligations"]),
        "trust_parameters": obligation_map["trust_parameters"],
        "obligation_map_sha256": sha256_file(
            GENERATED / "obligation-map.json"
        ),
        "manifest_obligation_map_sha256": generator_manifest[
            "obligation_map_sha256"
        ],
    },
    "fixed_target": {
        "computed_target": selected_target,
        "expected_target_definition": expected_target,
        "generator_manifest_target": generator_manifest["target"],
        "preflight_target": preflight["target"],
        "raw_target_declaration_count": raw_target_count,
        "all_absent": (
            selected_target is None
            and expected_target is None
            and generator_manifest["target"] is None
            and preflight["target"] is None
            and raw_target_count == 0
        ),
    },
    "recorded_bindings": {
        "generator_toolchain_matches_lock": (
            generator_manifest["toolchain"] == toolchain_lock
        ),
        "generator_tree_hash_matches": (
            generator_manifest["generated_tree_sha256"]
            == klean_export.tree_digest(GENERATED)
        ),
        "generator_obligation_count_matches": (
            generator_manifest["obligation_count"]
            == len(obligation_map["obligations"])
        ),
        "export_result_status": export_result["status"],
        "preflight_status": preflight["status"],
        "export_result_trust_inventory_hash_matches": (
            export_result["trust_inventory_sha256"]
            == sha256_file(GENERATION / "trust-inventory.json")
        ),
        "trust_allowlist_count": len(trust_inventory["allowlist"]),
    },
    "classification_only_stage5": {
        "candidate_exists": Path("/candidate").exists(),
        "audit_input_lean_workspace_hash": load_json(
            Path("/audit-input.json")
        )["resolution"]["hashes"]["lean_workspace_sha256"],
        "audit_input_lean_invocation_hash": load_json(
            Path("/audit-input.json")
        )["resolution"]["hashes"]["lean_invocation_sha256"],
    },
}
print(json.dumps(result, indent=2, sort_keys=True))
