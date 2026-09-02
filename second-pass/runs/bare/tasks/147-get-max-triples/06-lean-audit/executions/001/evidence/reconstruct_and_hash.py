#!/usr/bin/env python3
"""Independent mechanical reconstruction and immutable-input hash checks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)


AUDIT_INPUT = Path("/audit-input.json")
STAGE1 = Path("/reference/k-proof")
STAGE2 = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
LOCK = Path("/reference/klean-toolchain.lock.json")
MECHANICAL_LOCK = Path("/opt/humaneval/data/klean-audit-tools.lock.json")


def load(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise TypeError(f"{path} is not a JSON object")
    return value


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = load(AUDIT_INPUT)
resolution = audit["resolution"]
recorded_hashes = resolution["hashes"]
source_manifest = load(PRODUCERS / "source-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
input_manifest = load(GENERATION / "input-manifest.json")
export_result = load(GENERATION / "export-result.json")
recorded_preflight = load(GENERATION / "preflight.json")
obligation_map = load(GENERATED / "obligation-map.json")
lock = load(LOCK)
mechanical_lock = load(MECHANICAL_LOCK)

inventory = k_rule_inventory.inventory_verification(STAGE1)
validated = lemma_discovery_contract.validate_trust_boundary(
    STAGE1, DISCOVERY
)
manifest = load(DISCOVERY)

observed = {
    "audit_mode_env": os.environ.get("AUDIT_MODE"),
    "audit_mode_signed": resolution["mode"],
    "resolved_input_sha256": (
        stage6_resolution_contract.canonical_json_sha256(resolution)
    ),
    "discovery_manifest_sha256": file_hash(DISCOVERY),
    "k_workspace_sha256": pipeline_contract.sha256_tree(STAGE1),
    "stage1_export_sha256": klean_export.tree_digest(STAGE1),
    "k_audit_sha256": pipeline_contract.sha256_tree(STAGE2),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "generation_producer_sources_sha256": (
        pipeline_contract.sha256_tree(PRODUCERS)
    ),
    "verification_sha256": file_hash(STAGE1 / "verification.k"),
    "obligation_map_sha256": file_hash(GENERATED / "obligation-map.json"),
    "trust_inventory_sha256": file_hash(
        GENERATION / "trust-inventory.json"
    ),
    "klean_toolchain_lock_sha256": file_hash(LOCK),
    "mechanical_checker_lock_sha256": file_hash(MECHANICAL_LOCK),
    "mechanical_checker_files": {
        name: file_hash(Path("/reference") / name)
        for name in sorted(mechanical_lock["files"])
    },
    "producer_files": {
        name: file_hash(PRODUCERS / name)
        for name in ("klean_export.py", "klean.py")
    },
    "stage1_source_hashes": {
        path.relative_to(STAGE1).as_posix(): file_hash(path)
        for path in sorted(STAGE1.rglob("*"))
        if path.is_file() and not path.is_symlink()
    },
}

audit_generator_key = Path(
    resolution["generation_producer_sources"]
).name
generator_image_id = generator_manifest["provenance"][
    "generator_image_id"
]
source_image_id = source_manifest["generator_image_id"]

manifest_rule_ids = [
    entry["source_rule_id"] for entry in manifest["rules"]
]
inventory_rule_ids = [
    entry["source_rule_id"] for entry in inventory["rules"]
]

checks = {
    "audit_envelope_digest": (
        observed["resolved_input_sha256"]
        == audit["resolved_input_sha256"]
    ),
    "audit_mode_env_matches_signed": (
        observed["audit_mode_env"] == observed["audit_mode_signed"]
    ),
    "audit_mode_is_classification_only": (
        observed["audit_mode_signed"] == "CLASSIFICATION_ONLY"
    ),
    "candidate_absent": not Path("/candidate").exists(),
    "stage5_result_absent": resolution["stage5_result"] is None,
    "stage5_paths_absent": (
        resolution["lean_workspace"] is None
        and resolution["lean_invocation"] is None
        and recorded_hashes["lean_workspace_sha256"] is None
        and recorded_hashes["lean_invocation_sha256"] is None
    ),
    "producer_source_manifest_exact_files": (
        set(source_manifest) == {
            "schema_version",
            "generator_image_id",
            "files",
        }
        and source_manifest["schema_version"] == 1
        and set(source_manifest["files"]) == {
            "klean_export.py",
            "klean.py",
        }
    ),
    "producer_bundle_exact_file_set": (
        {
            path.relative_to(PRODUCERS).as_posix()
            for path in PRODUCERS.rglob("*")
            if path.is_file() and not path.is_symlink()
        }
        == {"source-manifest.json", "klean_export.py", "klean.py"}
    ),
    "producer_file_hashes_match_source_manifest": (
        observed["producer_files"] == source_manifest["files"]
    ),
    "producer_exporter_hash_matches_generator_manifest": (
        observed["producer_files"]["klean_export.py"]
        == generator_manifest["exporter_sha256"]
    ),
    "producer_klean_hash_matches_generator_manifest": (
        observed["producer_files"]["klean.py"]
        == generator_manifest["klean_py_sha256"]
    ),
    "producer_image_id_matches_source_and_generator": (
        generator_image_id == source_image_id
    ),
    "producer_image_id_matches_signed_audit_path": (
        generator_image_id == "sha256:" + audit_generator_key
    ),
    "producer_bundle_tree_hash_matches_audit": (
        observed["generation_producer_sources_sha256"]
        == recorded_hashes["generation_producer_sources_sha256"]
    ),
    "k_workspace_tree_hash_matches_audit": (
        observed["k_workspace_sha256"]
        == recorded_hashes["k_workspace_sha256"]
    ),
    "stage1_export_tree_hash_matches_audit": (
        observed["stage1_export_sha256"]
        == recorded_hashes["stage1_export_sha256"]
    ),
    "stage1_source_hash_map_matches_audit": (
        observed["stage1_source_hashes"]
        == resolution["stage1_source_hashes"]
    ),
    "k_audit_tree_hash_matches_audit": (
        observed["k_audit_sha256"]
        == recorded_hashes["k_audit_sha256"]
    ),
    "discovery_hash_matches_audit": (
        observed["discovery_manifest_sha256"]
        == recorded_hashes["discovery_manifest_sha256"]
    ),
    "generation_tree_hash_matches_audit": (
        observed["klean_generation_sha256"]
        == recorded_hashes["klean_generation_sha256"]
    ),
    "generation_selection_hash_matches_tree": (
        resolution["selections"]["klean_generation"]["artifact_sha256"]
        == observed["klean_generation_sha256"]
    ),
    "k_audit_selection_hash_matches_tree": (
        resolution["selections"]["k_audit"]["artifact_sha256"]
        == observed["k_audit_sha256"]
    ),
    "generated_tree_hash_matches_audit": (
        observed["generated_tree_sha256"]
        == recorded_hashes["generated_tree_sha256"]
    ),
    "generated_tree_hash_matches_generator_manifest": (
        observed["generated_tree_sha256"]
        == generator_manifest["generated_tree_sha256"]
    ),
    "obligation_map_hash_matches_generator_manifest": (
        observed["obligation_map_sha256"]
        == generator_manifest["obligation_map_sha256"]
    ),
    "trust_inventory_hash_matches_export_result": (
        observed["trust_inventory_sha256"]
        == export_result["trust_inventory_sha256"]
    ),
    "toolchain_lock_matches_generator_manifest": (
        lock == generator_manifest["toolchain"]
    ),
    "mechanical_checker_lock_hash_matches_audit": (
        observed["mechanical_checker_lock_sha256"]
        == audit["audit"]["mechanical_checker_lock_sha256"]
    ),
    "mechanical_checker_files_match_lock": (
        observed["mechanical_checker_files"] == mechanical_lock["files"]
    ),
    "stage4_preflight_matches_signed_audit": (
        recorded_preflight == resolution["stage4_preflight"]
    ),
    "input_manifest_stage1_hashes_match": (
        input_manifest["frozen_input_sha256"]
        == observed["stage1_export_sha256"]
        == input_manifest["stage1_workspace_sha256"]
    ),
    "input_manifest_discovery_hash_matches": (
        input_manifest["stage3_discovery_manifest_sha256"]
        == observed["discovery_manifest_sha256"]
    ),
    "generator_provenance_stage1_hash_matches": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == observed["stage1_export_sha256"]
    ),
    "generator_provenance_discovery_hash_matches": (
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == observed["discovery_manifest_sha256"]
    ),
    "export_result_hash_bindings_match": (
        export_result["frozen_input_sha256"]
        == observed["stage1_export_sha256"]
        and export_result["stage3_discovery_manifest_sha256"]
        == observed["discovery_manifest_sha256"]
        and export_result["generated_tree_sha256"]
        == observed["generated_tree_sha256"]
    ),
    "recorded_preflight_hash_bindings_match": (
        recorded_preflight["frozen_input_sha256"]
        == observed["stage1_export_sha256"]
        == recorded_preflight["stage1_workspace_sha256"]
        and recorded_preflight["stage3_discovery_manifest_sha256"]
        == observed["discovery_manifest_sha256"]
        and recorded_preflight["generated_tree_sha256"]
        == observed["generated_tree_sha256"]
    ),
    "verification_hash_matches_input_manifest": (
        observed["verification_sha256"]
        == input_manifest["verification_sha256"]
    ),
    "inventory_hash_matches_discovery": (
        inventory["inventory_sha256"] == manifest["inventory_sha256"]
    ),
    "inventory_hash_matches_input_manifest": (
        inventory["inventory_sha256"]
        == input_manifest["inventory_sha256"]
    ),
    "inventory_hash_matches_generator_provenance": (
        inventory["inventory_sha256"]
        == generator_manifest["provenance"]["inventory_sha256"]
    ),
    "manifest_rule_ids_exact_order": (
        manifest_rule_ids == inventory_rule_ids
    ),
    "manifest_rule_ids_unique": (
        len(manifest_rule_ids) == len(set(manifest_rule_ids))
    ),
    "validated_rule_count_exact": (
        len(validated["rules"]) == len(inventory["rules"])
    ),
    "input_manifest_definitions_exact": (
        input_manifest["definitions"] == validated["definitions"]
    ),
    "input_manifest_domain_rules_exact": (
        input_manifest["source_rules"] == validated["domain_lemmas"]
    ),
    "obligation_source_rules_exact": (
        obligation_map["source_rules"] == input_manifest["source_rules"]
    ),
    "obligation_count_exact": (
        len(obligation_map["obligations"])
        == generator_manifest["obligation_count"]
        == export_result["obligation_count"]
    ),
    "zero_obligation_target_absent": (
        not obligation_map["obligations"]
        and obligation_map["trust_parameters"] == []
        and export_result["status"] == "KLEAN_NO_OBLIGATIONS"
        and recorded_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
        and generator_manifest["target"] is None
        and resolution["target"] is None
        and resolution["stage4_preflight"]["target"] is None
        and klean_export.target_statement(GENERATED) is None
    ),
}

document = {
    "observed": observed,
    "inventory": inventory,
    "validated_stage3": validated,
    "manifest_rule_ids": manifest_rule_ids,
    "inventory_rule_ids": inventory_rule_ids,
    "generator_image_id": generator_image_id,
    "source_manifest_image_id": source_image_id,
    "audit_generator_path_key": audit_generator_key,
    "input_manifest_source_rules": input_manifest["source_rules"],
    "obligation_map": obligation_map,
    "checks": checks,
    "all_checks_pass": all(checks.values()),
}
print(json.dumps(document, indent=2, sort_keys=True))
