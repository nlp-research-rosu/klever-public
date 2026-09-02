#!/usr/bin/env python3
"""Re-hash the mounted audit inputs and cross-check recorded provenance."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_audit_contract, klean_export, pipeline_contract


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = klean_audit_contract.verify_stage6_audit_input(
    audit_input
)
hashes = resolution["hashes"]

generator_path = Path("/reference/klean-generation/generator-manifest.json")
input_path = Path("/reference/klean-generation/input-manifest.json")
export_path = Path("/reference/klean-generation/export-result.json")
trust_path = Path("/reference/klean-generation/trust-inventory.json")
obligation_path = Path(
    "/reference/klean-generation/generated/obligation-map.json"
)
source_manifest_path = Path("/reference/generation-tools/source-manifest.json")
discovery_path = Path("/reference/lemma-discovery.json")

generator = json.loads(generator_path.read_text())
input_manifest = json.loads(input_path.read_text())
export_result = json.loads(export_path.read_text())
source_manifest = json.loads(source_manifest_path.read_text())
obligation_map = json.loads(obligation_path.read_text())

producer_files = {
    name: file_sha(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
recorded_image = generator["provenance"]["generator_image_id"]
audit_bundle_name = Path(resolution["generation_producer_sources"]).name

stage1_actual_files = {
    path.relative_to("/reference/k-proof").as_posix(): file_sha(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "mounted Stage 1 workspace"
    )
}

actual = {
    "resolved_input_sha256": resolved_digest,
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": file_sha(discovery_path),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "producer_files": producer_files,
}

checks = {
    "audit_envelope_digest_valid": (
        resolved_digest == audit_input["resolved_input_sha256"]
    ),
    "audit_mode_matches_environment": (
        resolution["mode"] == os.environ.get("AUDIT_MODE")
    ),
    "audit_problem_matches": resolution["problem_id"] == "150-x-or-y",
    "audit_condition_matches": resolution["condition"] == "kit-semantics",
    "audit_semantics_mode_matches": (
        resolution["semantics_mode"] == "SUPPLIED_SEMANTICS"
    ),
    "stage1_pipeline_tree_matches_audit": (
        actual["k_workspace_sha256"] == hashes["k_workspace_sha256"]
    ),
    "stage1_export_tree_matches_audit": (
        actual["stage1_export_sha256"] == hashes["stage1_export_sha256"]
    ),
    "discovery_file_matches_audit": (
        actual["discovery_manifest_sha256"]
        == hashes["discovery_manifest_sha256"]
    ),
    "stage2_pipeline_tree_matches_audit": (
        actual["k_audit_sha256"] == hashes["k_audit_sha256"]
    ),
    "generation_pipeline_tree_matches_audit": (
        actual["klean_generation_sha256"]
        == hashes["klean_generation_sha256"]
    ),
    "producer_bundle_tree_matches_audit": (
        actual["generation_producer_sources_sha256"]
        == hashes["generation_producer_sources_sha256"]
    ),
    "generated_tree_matches_audit": (
        actual["generated_tree_sha256"] == hashes["generated_tree_sha256"]
    ),
    "all_stage1_file_names_exact": (
        set(stage1_actual_files) == set(resolution["stage1_source_hashes"])
    ),
    "all_stage1_file_hashes_exact": (
        stage1_actual_files == resolution["stage1_source_hashes"]
    ),
    "producer_bundle_names_exact": (
        {
            path.relative_to("/reference/generation-tools").as_posix()
            for path in pipeline_contract._walk_regular_files(
                Path("/reference/generation-tools"), "producer bundle"
            )
        }
        == {"klean_export.py", "klean.py", "source-manifest.json"}
    ),
    "producer_hashes_match_source_manifest": (
        producer_files == source_manifest["files"]
    ),
    "exporter_hash_matches_generator_manifest": (
        producer_files["klean_export.py"] == generator["exporter_sha256"]
    ),
    "klean_hash_matches_generator_manifest": (
        producer_files["klean.py"] == generator["klean_py_sha256"]
    ),
    "source_manifest_image_matches_generator_manifest": (
        source_manifest["generator_image_id"] == recorded_image
    ),
    "audit_bundle_path_binds_generator_image": (
        f"sha256:{audit_bundle_name}" == recorded_image
    ),
    "generation_stage1_provenance_matches_audit": (
        generator["provenance"]["stage1_workspace_sha256"]
        == hashes["stage1_export_sha256"]
    ),
    "generation_stage3_provenance_matches_audit": (
        generator["provenance"]["stage3_discovery_manifest_sha256"]
        == hashes["discovery_manifest_sha256"]
    ),
    "input_stage1_provenance_matches_audit": (
        input_manifest["stage1_workspace_sha256"]
        == hashes["stage1_export_sha256"]
    ),
    "input_stage3_provenance_matches_audit": (
        input_manifest["stage3_discovery_manifest_sha256"]
        == hashes["discovery_manifest_sha256"]
    ),
    "input_verification_hash_matches_frozen_source": (
        input_manifest["verification_sha256"]
        == file_sha(Path("/reference/k-proof/verification.k"))
    ),
    "generator_generated_tree_matches_actual": (
        generator["generated_tree_sha256"]
        == actual["generated_tree_sha256"]
    ),
    "generator_obligation_map_hash_matches_actual": (
        generator["obligation_map_sha256"] == file_sha(obligation_path)
    ),
    "export_generated_tree_matches_actual": (
        export_result["generated_tree_sha256"]
        == actual["generated_tree_sha256"]
    ),
    "export_trust_inventory_hash_matches_actual": (
        export_result["trust_inventory_sha256"] == file_sha(trust_path)
    ),
    "export_stage1_hash_matches_actual": (
        export_result["frozen_input_sha256"]
        == actual["stage1_export_sha256"]
    ),
    "export_stage3_hash_matches_actual": (
        export_result["stage3_discovery_manifest_sha256"]
        == actual["discovery_manifest_sha256"]
    ),
    "selected_stage2_artifact_hash_matches": (
        resolution["selections"]["k_audit"]["artifact_sha256"]
        == actual["k_audit_sha256"]
    ),
    "selected_stage4_artifact_hash_matches": (
        resolution["selections"]["klean_generation"]["artifact_sha256"]
        == actual["klean_generation_sha256"]
    ),
    "target_identity_null_everywhere": (
        generator["target"] is None
        and resolution["target"] is None
        and obligation_map["obligations"] == []
    ),
}

result = {
    "actual": actual,
    "recorded_resolution_hashes": hashes,
    "recorded_generator_image_id": recorded_image,
    "environment_audit_mode": os.environ.get("AUDIT_MODE"),
    "source_manifest": source_manifest,
    "stage1_file_count": len(stage1_actual_files),
    "checks": checks,
    "all_checks_pass": all(checks.values()),
}
print(json.dumps(result, indent=2, sort_keys=True))
