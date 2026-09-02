#!/usr/bin/env python3
"""Verify launcher and Stage 4 hashes against the mounted immutable inputs."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "/reference")
from tools.klean_export import target_statement, tree_digest
from tools.pipeline_contract import sha256_tree


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_document = json.loads(Path("/audit-input.json").read_text())
audit = audit_document["resolution"]
generation = Path("/reference/klean-generation")
generated = generation / "generated"
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)

actual_core = {
    "k_workspace_sha256": sha256_tree(Path("/reference/k-proof")),
    "stage1_export_sha256": tree_digest(Path("/reference/k-proof")),
    "discovery_manifest_sha256": file_hash(
        Path("/reference/lemma-discovery.json")
    ),
    "k_audit_sha256": sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": sha256_tree(generation),
    "generation_producer_sources_sha256": sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": tree_digest(generated),
    "lean_workspace_sha256": sha256_tree(Path("/candidate")),
}
expected_core = {
    key: audit["hashes"][key]
    for key in actual_core
}

stage1_expected = audit["stage1_source_hashes"]
stage1_actual = {
    path.relative_to("/reference/k-proof").as_posix(): file_hash(path)
    for path in Path("/reference/k-proof").rglob("*")
    if path.is_file() and not path.is_symlink()
}
stage1_mismatches = {
    name: {
        "expected": stage1_expected.get(name),
        "actual": stage1_actual.get(name),
    }
    for name in sorted(set(stage1_expected) | set(stage1_actual))
    if stage1_expected.get(name) != stage1_actual.get(name)
}

computed_target = target_statement(generated)
trust_inventory_hash = file_hash(generation / "trust-inventory.json")
obligation_map_hash = file_hash(generated / "obligation-map.json")
checks = {
    "launcher_core_hashes_match": actual_core == expected_core,
    "stage1_source_file_set_and_hashes_match": not stage1_mismatches,
    "generator_generated_tree_matches": (
        generator_manifest["generated_tree_sha256"]
        == actual_core["generated_tree_sha256"]
    ),
    "generator_obligation_map_hash_matches": (
        generator_manifest["obligation_map_sha256"] == obligation_map_hash
    ),
    "generator_exporter_hash_matches": (
        generator_manifest["exporter_sha256"]
        == file_hash(Path("/reference/generation-tools/klean_export.py"))
        == source_manifest["files"]["klean_export.py"]
    ),
    "generator_klean_hash_matches": (
        generator_manifest["klean_py_sha256"]
        == file_hash(Path("/reference/generation-tools/klean.py"))
        == source_manifest["files"]["klean.py"]
    ),
    "generator_image_matches_source_manifest": (
        generator_manifest["provenance"]["generator_image_id"]
        == source_manifest["generator_image_id"]
    ),
    "generator_stage1_provenance_matches": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == actual_core["stage1_export_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == input_manifest["frozen_input_sha256"]
    ),
    "generator_discovery_provenance_matches": (
        generator_manifest["provenance"]["stage3_discovery_manifest_sha256"]
        == actual_core["discovery_manifest_sha256"]
        == input_manifest["stage3_discovery_manifest_sha256"]
    ),
    "input_verification_hash_matches": (
        input_manifest["verification_sha256"]
        == file_hash(Path("/reference/k-proof/verification.k"))
    ),
    "export_result_stage1_hash_matches": (
        export_result["frozen_input_sha256"]
        == actual_core["stage1_export_sha256"]
    ),
    "export_result_discovery_hash_matches": (
        export_result["stage3_discovery_manifest_sha256"]
        == actual_core["discovery_manifest_sha256"]
    ),
    "export_result_generated_hash_matches": (
        export_result["generated_tree_sha256"]
        == actual_core["generated_tree_sha256"]
    ),
    "export_result_trust_hash_matches": (
        export_result["trust_inventory_sha256"] == trust_inventory_hash
    ),
    "computed_target_matches_generator_manifest": (
        computed_target == generator_manifest["target"]
    ),
    "computed_target_matches_audit_input": (
        computed_target == audit["target"]
    ),
    "computed_target_matches_recorded_preflight": (
        computed_target == audit["stage4_preflight"]["target"]
    ),
    "input_and_obligation_source_rules_match": (
        input_manifest["source_rules"] == obligation_map["source_rules"]
    ),
}

print(
    json.dumps(
        {
            "actual_core_hashes": actual_core,
            "expected_core_hashes": expected_core,
            "stage1_file_count": len(stage1_actual),
            "stage1_hash_mismatches": stage1_mismatches,
            "obligation_map_sha256": obligation_map_hash,
            "trust_inventory_sha256": trust_inventory_hash,
            "computed_target": computed_target,
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)
if not all(checks.values()):
    raise SystemExit(1)
