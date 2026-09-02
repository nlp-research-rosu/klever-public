#!/usr/bin/env python3
"""Recompute all launcher-recorded hashes and Stage 4 producer bindings."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
recorded = resolution["hashes"]
generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())

observed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
    "stage1_export_sha256": klean_export.tree_digest(K_WORKSPACE),
    "discovery_manifest_sha256": file_sha256(DISCOVERY),
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        PRODUCERS
    ),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

producer_hashes = {
    name: file_sha256(PRODUCERS / name)
    for name in ("klean_export.py", "klean.py")
}
expected_producer_hashes = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
recorded_generator_image_id = generator_manifest["provenance"][
    "generator_image_id"
]
audit_bundle_key = Path(resolution["generation_producer_sources"]).name

current_stage1_source_hashes = {
    path.relative_to(K_WORKSPACE).as_posix(): file_sha256(path)
    for path in sorted(K_WORKSPACE.rglob("*"))
    if path.is_file() and not path.is_symlink()
}

checks = {
    "resolved_input_sha256_exact": (
        resolved_digest == audit_document["resolved_input_sha256"]
    ),
    "all_launcher_hashes_exact": observed_hashes == recorded,
    "stage1_source_hashes_exact": (
        current_stage1_source_hashes == resolution["stage1_source_hashes"]
    ),
    "producer_bundle_exact_files": (
        sorted(
            path.relative_to(PRODUCERS).as_posix()
            for path in PRODUCERS.rglob("*")
            if path.is_file() and not path.is_symlink()
        )
        == ["klean.py", "klean_export.py", "source-manifest.json"]
    ),
    "producer_file_hashes_match_generator_manifest": (
        producer_hashes == expected_producer_hashes
    ),
    "producer_file_hashes_match_source_manifest": (
        producer_hashes == source_manifest["files"]
    ),
    "source_manifest_exact_shape": (
        set(source_manifest)
        == {"schema_version", "generator_image_id", "files"}
        and source_manifest["schema_version"] == 1
    ),
    "generator_image_matches_source_manifest": (
        recorded_generator_image_id == source_manifest["generator_image_id"]
    ),
    "generator_image_matches_audit_input_bundle_key": (
        recorded_generator_image_id == f"sha256:{audit_bundle_key}"
    ),
    "producer_bundle_tree_matches_audit_input": (
        observed_hashes["generation_producer_sources_sha256"]
        == recorded["generation_producer_sources_sha256"]
    ),
    "verification_hash_matches_input_manifest": (
        file_sha256(K_WORKSPACE / "verification.k")
        == input_manifest["verification_sha256"]
    ),
    "generator_generated_tree_hash_exact": (
        observed_hashes["generated_tree_sha256"]
        == generator_manifest["generated_tree_sha256"]
    ),
    "obligation_map_hash_exact": (
        file_sha256(obligation_map_path)
        == generator_manifest["obligation_map_sha256"]
    ),
    "export_result_hash_bindings_exact": (
        export_result["frozen_input_sha256"]
        == observed_hashes["stage1_export_sha256"]
        and export_result["stage3_discovery_manifest_sha256"]
        == observed_hashes["discovery_manifest_sha256"]
        and export_result["generated_tree_sha256"]
        == observed_hashes["generated_tree_sha256"]
        and export_result["trust_inventory_sha256"]
        == file_sha256(GENERATION / "trust-inventory.json")
    ),
    "stage1_provenance_exact": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == observed_hashes["stage1_export_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == input_manifest["frozen_input_sha256"]
    ),
    "stage3_provenance_exact": (
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == observed_hashes["discovery_manifest_sha256"]
        == input_manifest["stage3_discovery_manifest_sha256"]
    ),
    "inventory_provenance_exact": (
        generator_manifest["provenance"]["inventory_sha256"]
        == input_manifest["inventory_sha256"]
    ),
    "empty_obligation_bijection": (
        input_manifest["source_rules"] == []
        and obligation_map["source_rules"] == []
        and obligation_map["obligations"] == []
        and obligation_map["trust_parameters"] == []
        and generator_manifest["obligation_count"] == 0
        and export_result["obligation_count"] == 0
    ),
    "fixed_target_absent_everywhere": (
        generator_manifest["target"] is None
        and resolution["target"] is None
        and resolution["stage4_preflight"]["target"] is None
    ),
    "classification_only_has_no_stage5": (
        resolution["mode"] == "CLASSIFICATION_ONLY"
        and resolution["lean_workspace"] is None
        and resolution["lean_invocation"] is None
        and resolution["stage5_result"] is None
        and not Path("/candidate").exists()
    ),
}

print("OBSERVED_LAUNCHER_HASHES")
print(json.dumps(observed_hashes, indent=2, sort_keys=True))
print("RECORDED_LAUNCHER_HASHES")
print(json.dumps(recorded, indent=2, sort_keys=True))
print("PRODUCER_FILE_HASHES")
print(json.dumps(producer_hashes, indent=2, sort_keys=True))
print("GENERATOR_IMAGE_ID", recorded_generator_image_id)
print("AUDIT_INPUT_PRODUCER_BUNDLE_KEY", audit_bundle_key)
print("STAGE1_SOURCE_HASHES")
print(json.dumps(current_stage1_source_hashes, indent=2, sort_keys=True))
print("CHECKS")
print(json.dumps(checks, indent=2, sort_keys=True))
if not all(checks.values()):
    raise SystemExit("FAIL: at least one hash/provenance check failed")
print("RESULT PASS: all hashes, producer provenance, and empty target bindings match")
