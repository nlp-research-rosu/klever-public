#!/usr/bin/env python3
"""Independent hash, identity, obligation, and no-target checks for Stage 4."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.lemma_discovery_contract import validate_trust_boundary


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
k_workspace = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer_sources = Path("/reference/generation-tools")

input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
trust_inventory = json.loads(
    (generation / "trust-inventory.json").read_text()
)
preflight = json.loads((generation / "preflight.json").read_text())
obligation_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_path.read_text())
lock = json.loads(Path("/reference/klean-toolchain.lock.json").read_text())
validated = validate_trust_boundary(k_workspace, discovery_path)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


stage1_source_hashes = {
    path.relative_to(k_workspace).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        k_workspace, "Stage 1 source workspace"
    )
}
launcher_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(k_workspace),
    "k_audit_sha256": pipeline_contract.sha256_tree(k_audit),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        producer_sources
    ),
}
exporter_hashes = {
    "stage1_export_sha256": klean_export.tree_digest(k_workspace),
    "generated_tree_sha256": klean_export.tree_digest(generated),
}
discovery_sha256 = sha256_file(discovery_path)
trust_inventory_sha256 = sha256_file(generation / "trust-inventory.json")
obligation_map_sha256 = sha256_file(obligation_path)
target = klean_export.target_statement(generated)

expected_source_rules = validated["domain_lemmas"]
expected_ids = [rule["source_rule_id"] for rule in expected_source_rules]
observed_ids = [
    obligation.get("source_rule_id")
    for obligation in obligation_map["obligations"]
]

checks = {
    "env_mode_equals_launcher_mode": os.environ.get("AUDIT_MODE")
    == resolution["mode"],
    "mode_is_classification_only": resolution["mode"]
    == "CLASSIFICATION_ONLY",
    "semantics_mode_is_supplied": resolution["semantics_mode"]
    == "SUPPLIED_SEMANTICS",
    "problem_and_condition_match": resolution["problem_id"]
    == "147-get-max-triples"
    and resolution["condition"] == "kit-semantics",
    "launcher_tree_hashes_match": all(
        launcher_hashes[name] == resolution["hashes"][name]
        for name in launcher_hashes
    ),
    "exporter_tree_hashes_match": all(
        exporter_hashes[name] == resolution["hashes"][name]
        for name in exporter_hashes
    ),
    "stage1_source_hashes_match_exactly": stage1_source_hashes
    == resolution["stage1_source_hashes"],
    "discovery_file_hash_matches": discovery_sha256
    == resolution["hashes"]["discovery_manifest_sha256"],
    "selected_k_audit_hash_matches": launcher_hashes["k_audit_sha256"]
    == resolution["selections"]["k_audit"]["artifact_sha256"],
    "selected_generation_hash_matches": launcher_hashes[
        "klean_generation_sha256"
    ]
    == resolution["selections"]["klean_generation"]["artifact_sha256"],
    "selected_generation_status_no_obligations": resolution["selections"][
        "klean_generation"
    ]["status"]
    == "KLEAN_NO_OBLIGATIONS",
    "input_stage1_hashes_match": input_manifest["frozen_input_sha256"]
    == input_manifest["stage1_workspace_sha256"]
    == exporter_hashes["stage1_export_sha256"],
    "input_discovery_hash_matches": input_manifest[
        "stage3_discovery_manifest_sha256"
    ]
    == discovery_sha256,
    "input_verification_hash_matches": input_manifest["verification_sha256"]
    == sha256_file(k_workspace / "verification.k")
    == validated["verification_sha256"],
    "inventory_hashes_match": input_manifest["inventory_sha256"]
    == generator_manifest["provenance"]["inventory_sha256"]
    == validated["inventory_sha256"],
    "input_definitions_match_validated_manifest": input_manifest["definitions"]
    == validated["definitions"],
    "input_non_definition_classes_match_validated_manifest": (
        input_manifest["operational_rules"] == validated["operational_rules"]
        and input_manifest["proved_derived_lemmas"]
        == validated["proved_derived_lemmas"]
        and input_manifest["source_rules"] == validated["domain_lemmas"]
    ),
    "true_domain_set_empty": expected_source_rules == [],
    "obligation_source_rules_exact": obligation_map["source_rules"]
    == expected_source_rules,
    "obligation_ids_bijective_and_ordered": observed_ids == expected_ids
    and len(observed_ids) == len(set(observed_ids)),
    "obligations_empty": obligation_map["obligations"] == [],
    "trust_parameters_empty": obligation_map["trust_parameters"] == [],
    "obligation_count_consistent": generator_manifest["obligation_count"]
    == export_result["obligation_count"]
    == preflight["obligation_count"]
    == len(obligation_map["obligations"])
    == 0,
    "obligation_map_hash_matches": obligation_map_sha256
    == generator_manifest["obligation_map_sha256"],
    "generated_tree_hashes_match": exporter_hashes["generated_tree_sha256"]
    == generator_manifest["generated_tree_sha256"]
    == export_result["generated_tree_sha256"]
    == preflight["generated_tree_sha256"],
    "export_result_bindings_match": (
        export_result["frozen_input_sha256"]
        == exporter_hashes["stage1_export_sha256"]
        and export_result["stage3_discovery_manifest_sha256"]
        == discovery_sha256
        and export_result["trust_inventory_sha256"]
        == trust_inventory_sha256
        and export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    ),
    "generator_provenance_matches": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == exporter_hashes["stage1_export_sha256"]
        and generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == discovery_sha256
    ),
    "toolchain_lock_matches_generator": generator_manifest["toolchain"] == lock,
    "target_absent_everywhere": target is None
    and generator_manifest["target"] is None
    and preflight["target"] is None
    and resolution["target"] is None,
    "no_stage5_candidate_mounted": not Path("/candidate").exists(),
    "no_stage5_launcher_paths_or_hashes": (
        resolution["lean_workspace"] is None
        and resolution["lean_invocation"] is None
        and resolution["hashes"]["lean_workspace_sha256"] is None
        and resolution["hashes"]["lean_invocation_sha256"] is None
        and audit["resolution"]["stage5_result"] is None
    ),
    "selected_preflight_bound_in_audit_input": preflight
    == audit["resolution"]["stage4_preflight"],
    "trust_hole_counts_zero": trust_inventory["designated_sorries"] == 0
    and trust_inventory["other_sorries"] == 0,
}

print(
    json.dumps(
        {
            "computed": {
                "launcher_hashes": launcher_hashes,
                "exporter_hashes": exporter_hashes,
                "discovery_manifest_sha256": discovery_sha256,
                "verification_sha256": sha256_file(
                    k_workspace / "verification.k"
                ),
                "inventory_sha256": validated["inventory_sha256"],
                "obligation_map_sha256": obligation_map_sha256,
                "trust_inventory_sha256": trust_inventory_sha256,
                "stage1_source_file_count": len(stage1_source_hashes),
                "validated_definition_count": len(validated["definitions"]),
                "validated_operational_rule_count": len(
                    validated["operational_rules"]
                ),
                "validated_proved_derived_lemma_count": len(
                    validated["proved_derived_lemmas"]
                ),
                "validated_domain_lemma_count": len(
                    validated["domain_lemmas"]
                ),
                "expected_source_rule_ids": expected_ids,
                "observed_obligation_source_rule_ids": observed_ids,
                "target_statement": target,
            },
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
