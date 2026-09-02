#!/usr/bin/env python3
"""Recompute mounted-input and Stage 4 producer provenance hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_input
)
recorded = resolution["hashes"]
generator_dir = Path("/reference/generation-tools")
generation_dir = Path("/reference/klean-generation")
generated_dir = generation_dir / "generated"
k_workspace = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
candidate = Path("/candidate")
discovery = Path("/reference/lemma-discovery.json")
source_manifest = json.loads(
    (generator_dir / "source-manifest.json").read_text()
)
generator_manifest = json.loads(
    (generation_dir / "generator-manifest.json").read_text()
)
input_manifest = json.loads(
    (generation_dir / "input-manifest.json").read_text()
)
export_result = json.loads(
    (generation_dir / "export-result.json").read_text()
)
producer_files = {
    name: file_sha256(generator_dir / name)
    for name in ("klean_export.py", "klean.py")
}
image_from_audit_path = (
    "sha256:" + Path(resolution["generation_producer_sources"]).name
)

stage1_observed_hashes: dict[str, str] = {}
stage1_missing: list[str] = []
for relative in resolution["stage1_source_hashes"]:
    source = k_workspace / relative
    if not source.is_file():
        stage1_missing.append(relative)
        continue
    stage1_observed_hashes[relative] = file_sha256(source)
stage1_hash_mismatches = {
    relative: {
        "expected": resolution["stage1_source_hashes"][relative],
        "observed": stage1_observed_hashes.get(relative),
    }
    for relative in resolution["stage1_source_hashes"]
    if stage1_observed_hashes.get(relative)
    != resolution["stage1_source_hashes"][relative]
}

observed = {
    "resolved_input_sha256": resolved_digest,
    "producer_files": producer_files,
    "producer_tree_sha256": pipeline_contract.sha256_tree(generator_dir),
    "generated_tree_sha256": klean_export.tree_digest(generated_dir),
    "k_workspace_pipeline_sha256": pipeline_contract.sha256_tree(k_workspace),
    "k_workspace_export_sha256": klean_export.tree_digest(k_workspace),
    "k_audit_pipeline_sha256": pipeline_contract.sha256_tree(k_audit),
    "klean_generation_pipeline_sha256": pipeline_contract.sha256_tree(
        generation_dir
    ),
    "candidate_pipeline_sha256": pipeline_contract.sha256_tree(candidate),
    "discovery_manifest_sha256": file_sha256(discovery),
    "trust_inventory_sha256": file_sha256(
        generation_dir / "trust-inventory.json"
    ),
    "generator_image_from_audit_path": image_from_audit_path,
    "generator_image_from_source_manifest": source_manifest[
        "generator_image_id"
    ],
    "generator_image_from_generator_manifest": generator_manifest[
        "provenance"
    ]["generator_image_id"],
    "stage1_source_hash_count": len(resolution["stage1_source_hashes"]),
    "stage1_source_missing": stage1_missing,
    "stage1_source_hash_mismatches": stage1_hash_mismatches,
}

checks = {
    "producer_files_match_source_manifest": (
        producer_files == source_manifest["files"]
    ),
    "producer_files_match_generator_manifest": (
        producer_files["klean_export.py"]
        == generator_manifest["exporter_sha256"]
        and producer_files["klean.py"]
        == generator_manifest["klean_py_sha256"]
    ),
    "producer_tree_matches_audit_input": (
        observed["producer_tree_sha256"]
        == recorded["generation_producer_sources_sha256"]
    ),
    "generator_image_identity_matches": (
        observed["generator_image_from_audit_path"]
        == observed["generator_image_from_source_manifest"]
        == observed["generator_image_from_generator_manifest"]
    ),
    "generated_tree_matches_all_records": (
        observed["generated_tree_sha256"]
        == recorded["generated_tree_sha256"]
        == generator_manifest["generated_tree_sha256"]
        == export_result["generated_tree_sha256"]
    ),
    "stage1_export_tree_matches_all_records": (
        observed["k_workspace_export_sha256"]
        == recorded["stage1_export_sha256"]
        == generator_manifest["provenance"]["stage1_workspace_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == input_manifest["frozen_input_sha256"]
        == export_result["frozen_input_sha256"]
    ),
    "stage1_pipeline_tree_matches_audit_input": (
        observed["k_workspace_pipeline_sha256"]
        == recorded["k_workspace_sha256"]
    ),
    "k_audit_pipeline_tree_matches_audit_input": (
        observed["k_audit_pipeline_sha256"] == recorded["k_audit_sha256"]
    ),
    "generation_pipeline_tree_matches_audit_input": (
        observed["klean_generation_pipeline_sha256"]
        == recorded["klean_generation_sha256"]
    ),
    "candidate_pipeline_tree_matches_audit_input": (
        observed["candidate_pipeline_sha256"]
        == recorded["lean_workspace_sha256"]
    ),
    "discovery_manifest_matches_all_records": (
        observed["discovery_manifest_sha256"]
        == recorded["discovery_manifest_sha256"]
        == generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == input_manifest["stage3_discovery_manifest_sha256"]
        == export_result["stage3_discovery_manifest_sha256"]
    ),
    "trust_inventory_matches_export_result": (
        observed["trust_inventory_sha256"]
        == export_result["trust_inventory_sha256"]
    ),
    "target_matches_audit_input": (
        generator_manifest["target"] == resolution["target"]
    ),
    "preflight_matches_audit_input": (
        json.loads((generation_dir / "preflight.json").read_text())
        == resolution["stage4_preflight"]
    ),
    "all_stage1_source_hashes_match": (
        not stage1_missing and not stage1_hash_mismatches
    ),
}
checks["all_checks_pass"] = all(checks.values())

result = {
    "observed": observed,
    "recorded_audit_hashes": recorded,
    "checks": checks,
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if checks["all_checks_pass"] else 1)
