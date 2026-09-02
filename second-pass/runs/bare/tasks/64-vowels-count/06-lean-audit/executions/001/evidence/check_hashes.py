#!/usr/bin/env python3
"""Recompute launcher, source, tree, and producer-authentication hashes."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "/reference")

from tools import klean_export, pipeline_contract, stage6_resolution_contract


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_document = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
recorded = resolution["hashes"]

observed = {
    "discovery_manifest_sha256": file_sha256(
        Path("/reference/lemma-discovery.json")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "lean_invocation_sha256": None,
    "lean_workspace_sha256": None,
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
}

workspace = Path("/reference/k-proof")
observed_source_hashes = {
    path.relative_to(workspace).as_posix(): file_sha256(path)
    for path in pipeline_contract._walk_regular_files(
        workspace, "mounted Stage 1 workspace"
    )
}

generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
preflight = json.loads(
    Path("/reference/klean-generation/preflight.json").read_text()
)
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)

producer_hashes = {
    "klean_export.py": file_sha256(
        Path("/reference/generation-tools/klean_export.py")
    ),
    "klean.py": file_sha256(Path("/reference/generation-tools/klean.py")),
}
image_id = generator_manifest["provenance"]["generator_image_id"]
image_key = image_id.removeprefix("sha256:")
recorded_bundle_key = Path(
    resolution["generation_producer_sources"]
).name
producer_expected = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}

checks = {
    "audit_envelope_digest_verified": (
        resolved_digest == audit_document["resolved_input_sha256"]
    ),
    "all_resolution_hashes_match": observed == recorded,
    "stage1_source_hash_keyset_matches": (
        set(observed_source_hashes) == set(resolution["stage1_source_hashes"])
    ),
    "all_stage1_source_hashes_match": (
        observed_source_hashes == resolution["stage1_source_hashes"]
    ),
    "producer_bundle_exact_file_set": (
        {
            path.relative_to("/reference/generation-tools").as_posix()
            for path in pipeline_contract._walk_regular_files(
                Path("/reference/generation-tools"),
                "mounted producer source bundle",
            )
        }
        == {"source-manifest.json", "klean_export.py", "klean.py"}
    ),
    "producer_file_hashes_match_generator_manifest": (
        producer_hashes == producer_expected
    ),
    "producer_file_hashes_match_source_manifest": (
        producer_hashes == source_manifest["files"]
    ),
    "source_manifest_exact_shape": (
        set(source_manifest)
        == {"schema_version", "generator_image_id", "files"}
        and source_manifest["schema_version"] == 1
    ),
    "generator_image_id_matches_source_manifest": (
        source_manifest["generator_image_id"] == image_id
    ),
    "generator_image_id_matches_audit_input_bundle_key": (
        recorded_bundle_key == image_key
    ),
    "generator_toolchain_matches_lock": (
        generator_manifest["toolchain"] == toolchain_lock
    ),
    "stage4_preflight_exactly_matches_audit_input": (
        preflight == resolution["stage4_preflight"]
    ),
    "generator_target_matches_audit_input": (
        generator_manifest["target"] == resolution["target"]
    ),
    "selection_k_audit_hash_matches": (
        resolution["selections"]["k_audit"]["artifact_sha256"]
        == observed["k_audit_sha256"]
    ),
    "selection_generation_hash_matches": (
        resolution["selections"]["klean_generation"]["artifact_sha256"]
        == observed["klean_generation_sha256"]
    ),
    "input_manifest_stage1_export_hash_matches": (
        input_manifest["stage1_workspace_sha256"]
        == observed["stage1_export_sha256"]
        and input_manifest["frozen_input_sha256"]
        == observed["stage1_export_sha256"]
    ),
    "generator_provenance_stage1_hash_matches": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == observed["stage1_export_sha256"]
    ),
    "generator_generated_tree_hash_matches": (
        generator_manifest["generated_tree_sha256"]
        == observed["generated_tree_sha256"]
    ),
    "classification_only_has_no_candidate": (
        resolution["mode"] == "CLASSIFICATION_ONLY"
        and not Path("/candidate").exists()
        and resolution["lean_workspace"] is None
        and resolution["lean_invocation"] is None
        and resolution["stage5_result"] is None
    ),
}
checks["all_checks_pass"] = all(checks.values())

print(
    json.dumps(
        {
            "resolved_input_sha256": resolved_digest,
            "recorded_hashes": recorded,
            "observed_hashes": observed,
            "recorded_stage1_source_hashes": resolution[
                "stage1_source_hashes"
            ],
            "observed_stage1_source_hashes": observed_source_hashes,
            "producer_authentication": {
                "observed_file_hashes": producer_hashes,
                "generator_manifest_expected": producer_expected,
                "source_manifest_expected": source_manifest["files"],
                "generator_manifest_image_id": image_id,
                "source_manifest_image_id": source_manifest[
                    "generator_image_id"
                ],
                "audit_input_bundle_key": recorded_bundle_key,
                "audit_input_bundle_tree_sha256": recorded[
                    "generation_producer_sources_sha256"
                ],
            },
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)
