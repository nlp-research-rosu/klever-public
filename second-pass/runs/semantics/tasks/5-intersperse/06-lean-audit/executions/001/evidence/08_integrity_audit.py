#!/usr/bin/env python3
"""Independent hash, provenance, obligation, and target-integrity audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


def load(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise TypeError(f"expected JSON object: {path}")
    return value


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_path = Path("/audit-input.json")
audit = load(audit_path)
resolution, resolution_digest = stage6_resolution_contract.verify_audit_input(
    audit
)
recorded_hashes = resolution["hashes"]

workspace = Path("/reference/k-proof")
prior_audit = Path("/reference/k-audit")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer = Path("/reference/generation-tools")

source_manifest = load(producer / "source-manifest.json")
generator_manifest = load(generation / "generator-manifest.json")
input_manifest = load(generation / "input-manifest.json")
obligation_map = load(generated / "obligation-map.json")
export_result = load(generation / "export-result.json")
preflight = load(generation / "preflight.json")
trust_inventory_path = generation / "trust-inventory.json"
toolchain_lock = load(Path("/reference/klean-toolchain.lock.json"))
discovery = load(discovery_path)

stage1_source_hashes = {}
for path in pipeline_contract._walk_regular_files(
    workspace, "Stage 1 source workspace"
):
    stage1_source_hashes[path.relative_to(workspace).as_posix()] = file_sha256(
        path
    )

producer_files = {
    path.relative_to(producer).as_posix()
    for path in pipeline_contract._walk_regular_files(
        producer, "Stage 4 producer bundle"
    )
}
producer_image = source_manifest["generator_image_id"]
producer_image_key = producer_image.removeprefix("sha256:")
recorded_producer_path = Path(resolution["generation_producer_sources"])

stage3_domain_ids = [
    item["source_rule_id"]
    for item in discovery["rules"]
    if item["classification"] == "DOMAIN_LEMMA"
]
mapped_source_ids = [
    item["source_rule_id"] for item in obligation_map["source_rules"]
]
mapped_obligation_ids = [
    item["source_rule_id"] for item in obligation_map["obligations"]
]

computed = {
    "audit_input_sha256": file_sha256(audit_path),
    "audit_output_copy_sha256": file_sha256(
        Path("/audit-output/audit-input.json")
    ),
    "discovery_manifest_sha256": file_sha256(discovery_path),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        producer
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(prior_audit),
    "k_workspace_export_sha256": klean_export.tree_digest(workspace),
    "k_workspace_sha256": pipeline_contract.sha256_tree(workspace),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "obligation_map_sha256": file_sha256(
        generated / "obligation-map.json"
    ),
    "trust_inventory_sha256": file_sha256(trust_inventory_path),
    "verification_sha256": file_sha256(workspace / "verification.k"),
}

observed_target = klean_export.target_statement(generated)
checks = {
    "audit_envelope_digest_valid": (
        resolution_digest == audit["resolved_input_sha256"]
    ),
    "audit_output_copy_matches_root_input": (
        computed["audit_input_sha256"]
        == computed["audit_output_copy_sha256"]
    ),
    "mode_matches_environment": (
        resolution["mode"] == os.environ.get("AUDIT_MODE")
        == "CLASSIFICATION_ONLY"
    ),
    "semantics_mode_is_supplied": (
        resolution["semantics_mode"] == "SUPPLIED_SEMANTICS"
    ),
    "producer_exact_file_set": producer_files
    == {"klean.py", "klean_export.py", "source-manifest.json"},
    "producer_image_source_to_generator": (
        generator_manifest["provenance"]["generator_image_id"]
        == producer_image
    ),
    "producer_image_recorded_path": (
        recorded_producer_path.name == producer_image_key
    ),
    "producer_exporter_hash": (
        file_sha256(producer / "klean_export.py")
        == source_manifest["files"]["klean_export.py"]
        == generator_manifest["exporter_sha256"]
    ),
    "producer_klean_hash": (
        file_sha256(producer / "klean.py")
        == source_manifest["files"]["klean.py"]
        == generator_manifest["klean_py_sha256"]
    ),
    "producer_tree_hash": (
        computed["generation_producer_sources_sha256"]
        == recorded_hashes["generation_producer_sources_sha256"]
    ),
    "workspace_pipeline_tree_hash": (
        computed["k_workspace_sha256"]
        == recorded_hashes["k_workspace_sha256"]
    ),
    "workspace_export_tree_hash": (
        computed["k_workspace_export_sha256"]
        == recorded_hashes["stage1_export_sha256"]
        == input_manifest["frozen_input_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == generator_manifest["provenance"]["stage1_workspace_sha256"]
        == preflight["stage1_workspace_sha256"]
    ),
    "stage1_file_hash_bijection": (
        stage1_source_hashes == resolution["stage1_source_hashes"]
    ),
    "verification_hash": (
        computed["verification_sha256"]
        == input_manifest["verification_sha256"]
        == resolution["stage1_source_hashes"]["verification.k"]
    ),
    "discovery_hash": (
        computed["discovery_manifest_sha256"]
        == recorded_hashes["discovery_manifest_sha256"]
        == input_manifest["stage3_discovery_manifest_sha256"]
        == generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == preflight["stage3_discovery_manifest_sha256"]
    ),
    "inventory_hash": (
        discovery["inventory_sha256"]
        == input_manifest["inventory_sha256"]
        == generator_manifest["provenance"]["inventory_sha256"]
    ),
    "prior_audit_tree_hash": (
        computed["k_audit_sha256"] == recorded_hashes["k_audit_sha256"]
    ),
    "generation_tree_hash": (
        computed["klean_generation_sha256"]
        == recorded_hashes["klean_generation_sha256"]
    ),
    "generated_tree_hash": (
        computed["generated_tree_sha256"]
        == recorded_hashes["generated_tree_sha256"]
        == generator_manifest["generated_tree_sha256"]
        == export_result["generated_tree_sha256"]
        == preflight["generated_tree_sha256"]
    ),
    "toolchain_lock_exact": generator_manifest["toolchain"]
    == toolchain_lock,
    "obligation_map_hash": (
        computed["obligation_map_sha256"]
        == generator_manifest["obligation_map_sha256"]
    ),
    "trust_inventory_hash": (
        computed["trust_inventory_sha256"]
        == export_result["trust_inventory_sha256"]
    ),
    "stage3_to_source_rule_ordered_bijection": (
        stage3_domain_ids == mapped_source_ids
        and len(mapped_source_ids) == len(set(mapped_source_ids))
    ),
    "source_rule_to_obligation_ordered_bijection": (
        mapped_source_ids == mapped_obligation_ids
        and len(mapped_obligation_ids) == len(set(mapped_obligation_ids))
    ),
    "zero_obligation_counts": (
        len(mapped_obligation_ids)
        == generator_manifest["obligation_count"]
        == export_result["obligation_count"]
        == preflight["obligation_count"]
        == 0
    ),
    "no_trust_parameters": obligation_map["trust_parameters"] == [],
    "fixed_target_absent_everywhere": (
        observed_target
        == generator_manifest["target"]
        == preflight["target"]
        == resolution["target"]
        is None
    ),
    "no_stage5_candidate": not Path("/candidate").exists(),
    "preflight_record_bound_into_audit_input": (
        resolution["stage4_preflight"] == preflight
    ),
    "status_consistency": (
        preflight["status"]
        == resolution["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
        and export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    ),
}

print("COMPUTED_HASHES")
print(json.dumps(computed, indent=2, sort_keys=True))
print("SOURCE_AND_OBLIGATION_IDS")
print(
    json.dumps(
        {
            "stage3_domain_ids": stage3_domain_ids,
            "mapped_source_ids": mapped_source_ids,
            "mapped_obligation_ids": mapped_obligation_ids,
            "observed_target": observed_target,
        },
        indent=2,
        sort_keys=True,
    )
)
print("INTEGRITY_CHECKS")
print(json.dumps(checks, indent=2, sort_keys=True))
if not all(checks.values()):
    raise SystemExit("FAIL: one or more integrity checks failed")
print("PASS: all independently recomputed integrity checks passed")
