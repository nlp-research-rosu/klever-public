#!/usr/bin/env python3
"""Independent Stage 6 mounted-input hash and producer-provenance checks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


document = json.loads(AUDIT_INPUT.read_bytes())
resolution, signed_digest = stage6_resolution_contract.verify_audit_input(document)
expected = resolution["hashes"]

actual_source_hashes = {
    path.relative_to(K_WORKSPACE).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        K_WORKSPACE, "mounted Stage 1 source workspace"
    )
}

generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_bytes()
)
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_bytes())
generator_image_id = generator_manifest["provenance"]["generator_image_id"]
image_digest = generator_image_id.removeprefix("sha256:")

producer_files_actual = {
    name: sha256_file(PRODUCERS / name)
    for name in ("klean_export.py", "klean.py")
}
producer_files_from_generator = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
producer_names = sorted(
    path.relative_to(PRODUCERS).as_posix()
    for path in pipeline_contract._walk_regular_files(
        PRODUCERS, "mounted producer source bundle"
    )
)

checks = {
    "audit_input_signed_envelope": True,
    "audit_mode_env_matches_resolution": (
        os.environ.get("AUDIT_MODE") == resolution["mode"]
    ),
    "discovery_manifest_sha256": (
        sha256_file(DISCOVERY) == expected["discovery_manifest_sha256"]
    ),
    "k_workspace_full_tree_sha256": (
        pipeline_contract.sha256_tree(K_WORKSPACE)
        == expected["k_workspace_sha256"]
    ),
    "stage1_export_tree_digest": (
        klean_export.tree_digest(K_WORKSPACE)
        == expected["stage1_export_sha256"]
    ),
    "stage1_source_hash_keyset": (
        set(actual_source_hashes) == set(resolution["stage1_source_hashes"])
    ),
    "stage1_source_hash_values": (
        actual_source_hashes == resolution["stage1_source_hashes"]
    ),
    "k_audit_tree_sha256": (
        pipeline_contract.sha256_tree(K_AUDIT) == expected["k_audit_sha256"]
    ),
    "klean_generation_tree_sha256": (
        pipeline_contract.sha256_tree(GENERATION)
        == expected["klean_generation_sha256"]
    ),
    "generated_tree_digest": (
        klean_export.tree_digest(GENERATED)
        == expected["generated_tree_sha256"]
    ),
    "producer_bundle_tree_sha256": (
        pipeline_contract.sha256_tree(PRODUCERS)
        == expected["generation_producer_sources_sha256"]
    ),
    "producer_bundle_exact_files": (
        producer_names
        == ["klean.py", "klean_export.py", "source-manifest.json"]
    ),
    "producer_hashes_match_source_manifest": (
        producer_files_actual == source_manifest["files"]
    ),
    "producer_hashes_match_generator_manifest": (
        producer_files_actual == producer_files_from_generator
    ),
    "source_manifest_image_matches_generator_manifest": (
        source_manifest["generator_image_id"] == generator_image_id
    ),
    "audit_input_producer_path_binds_image_id": (
        Path(resolution["generation_producer_sources"]).name == image_digest
    ),
    "classification_only_has_no_stage5_paths": (
        resolution["mode"] == "CLASSIFICATION_ONLY"
        and resolution["lean_workspace"] is None
        and resolution["lean_invocation"] is None
        and expected["lean_workspace_sha256"] is None
        and expected["lean_invocation_sha256"] is None
    ),
    "candidate_mount_absent": not Path("/candidate").exists(),
}

values = {
    "signed_resolution_sha256": signed_digest,
    "generator_image_id": generator_image_id,
    "producer_names": producer_names,
    "producer_files_actual": producer_files_actual,
    "producer_bundle_tree_actual": pipeline_contract.sha256_tree(PRODUCERS),
    "producer_bundle_tree_expected": expected[
        "generation_producer_sources_sha256"
    ],
    "discovery_sha256_actual": sha256_file(DISCOVERY),
    "k_workspace_full_tree_actual": pipeline_contract.sha256_tree(K_WORKSPACE),
    "stage1_export_tree_actual": klean_export.tree_digest(K_WORKSPACE),
    "k_audit_tree_actual": pipeline_contract.sha256_tree(K_AUDIT),
    "klean_generation_tree_actual": pipeline_contract.sha256_tree(GENERATION),
    "generated_tree_actual": klean_export.tree_digest(GENERATED),
    "stage1_source_file_count": len(actual_source_hashes),
}

print(json.dumps({"checks": checks, "values": values}, indent=2, sort_keys=True))
if not all(checks.values()):
    raise SystemExit(1)
