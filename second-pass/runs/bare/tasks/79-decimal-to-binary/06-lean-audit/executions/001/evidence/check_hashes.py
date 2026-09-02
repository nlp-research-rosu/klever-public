#!/usr/bin/env python3
"""Read-only hash and provenance reconciliation for this audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract


def load(path: str) -> dict:
    return json.loads(Path(path).read_text())


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = load("/audit-input.json")
resolution = audit["resolution"]
generator = load("/reference/klean-generation/generator-manifest.json")
source = load("/reference/generation-tools/source-manifest.json")
input_manifest = load("/reference/klean-generation/input-manifest.json")
preflight = load("/reference/klean-generation/preflight.json")

producer = Path("/reference/generation-tools")
producer_files = sorted(
    path.relative_to(producer).as_posix()
    for path in pipeline_contract._walk_regular_files(
        producer, "mounted producer bundle"
    )
)
producer_observed = {
    name: file_sha256(producer / name)
    for name in ("klean.py", "klean_export.py")
}
image_id = generator["provenance"]["generator_image_id"]

stage1 = Path("/reference/k-proof")
stage1_files = {
    path.relative_to(stage1).as_posix(): file_sha256(path)
    for path in pipeline_contract._walk_regular_files(
        stage1, "mounted Stage 1 workspace"
    )
}

checks = {
    "audit_mode_environment_matches_input": (
        os.environ.get("AUDIT_MODE") == resolution["mode"]
    ),
    "problem_condition_semantics_match_request": (
        resolution["problem_id"] == "79-decimal-to-binary"
        and resolution["condition"] == "bare"
        and resolution["semantics_mode"] == "GENERATED_SEMANTICS"
    ),
    "producer_bundle_exact_file_set": producer_files
    == ["klean.py", "klean_export.py", "source-manifest.json"],
    "producer_file_hashes_match_source_manifest": (
        producer_observed == source["files"]
    ),
    "producer_file_hashes_match_generator_manifest": (
        producer_observed["klean_export.py"] == generator["exporter_sha256"]
        and producer_observed["klean.py"] == generator["klean_py_sha256"]
    ),
    "producer_image_matches_source_and_generator_manifests": (
        source["generator_image_id"] == image_id
    ),
    "producer_image_matches_audit_input_bundle_identity": (
        Path(resolution["generation_producer_sources"]).name
        == image_id.removeprefix("sha256:")
    ),
    "producer_bundle_pipeline_hash_matches_audit_input": (
        pipeline_contract.sha256_tree(producer)
        == resolution["hashes"]["generation_producer_sources_sha256"]
    ),
    "stage1_exact_file_hash_map_matches_audit_input": (
        stage1_files == resolution["stage1_source_hashes"]
    ),
    "stage1_pipeline_tree_hash_matches_audit_input": (
        pipeline_contract.sha256_tree(stage1)
        == resolution["hashes"]["k_workspace_sha256"]
    ),
    "stage1_export_tree_hash_matches_audit_and_manifests": (
        klean_export.tree_digest(stage1)
        == resolution["hashes"]["stage1_export_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == input_manifest["frozen_input_sha256"]
        == generator["provenance"]["stage1_workspace_sha256"]
    ),
    "stage3_file_hash_matches_audit_and_manifests": (
        file_sha256(Path("/reference/lemma-discovery.json"))
        == resolution["hashes"]["discovery_manifest_sha256"]
        == input_manifest["stage3_discovery_manifest_sha256"]
        == generator["provenance"]["stage3_discovery_manifest_sha256"]
    ),
    "selected_stage2_pipeline_hash_matches_audit_input": (
        pipeline_contract.sha256_tree(Path("/reference/k-audit"))
        == resolution["hashes"]["k_audit_sha256"]
    ),
    "selected_stage4_pipeline_hash_matches_audit_input": (
        pipeline_contract.sha256_tree(Path("/reference/klean-generation"))
        == resolution["hashes"]["klean_generation_sha256"]
    ),
    "generated_export_tree_hash_matches_audit_and_generator": (
        klean_export.tree_digest(
            Path("/reference/klean-generation/generated")
        )
        == resolution["hashes"]["generated_tree_sha256"]
        == generator["generated_tree_sha256"]
        == preflight["generated_tree_sha256"]
    ),
    "inventory_hash_consistent_across_manifests": (
        input_manifest["inventory_sha256"]
        == generator["provenance"]["inventory_sha256"]
    ),
    "stage4_status_target_and_count_consistent": (
        resolution["selections"]["klean_generation"]["status"]
        == preflight["status"]
        == "KLEAN_NO_OBLIGATIONS"
        and generator["obligation_count"] == preflight["obligation_count"] == 0
        and resolution["target"] is None
        and generator["target"] is None
        and preflight["target"] is None
    ),
    "launcher_preflight_evidence_matches_sidecar": (
        resolution["stage4_preflight"] == preflight
    ),
    "classification_only_has_no_stage5_paths_or_result": (
        resolution["lean_workspace"] is None
        and resolution["lean_invocation"] is None
        and resolution["stage5_result"] is None
        and not Path("/candidate").exists()
    ),
}

details = {
    "checks": checks,
    "all_checks_pass": all(checks.values()),
    "producer_files": producer_files,
    "producer_observed_sha256": producer_observed,
    "producer_pipeline_tree_sha256": pipeline_contract.sha256_tree(producer),
    "stage1_pipeline_tree_sha256": pipeline_contract.sha256_tree(stage1),
    "stage1_export_tree_sha256": klean_export.tree_digest(stage1),
    "stage3_manifest_sha256": file_sha256(
        Path("/reference/lemma-discovery.json")
    ),
    "stage2_pipeline_tree_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "stage4_pipeline_tree_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generated_export_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
}
print(json.dumps(details, indent=2, sort_keys=True))
