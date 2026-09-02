#!/usr/bin/env python3
"""Recompute launcher/manifests hashes and Stage 4 structural bindings."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, lemma_discovery_contract, pipeline_contract
from tools.k_rule_inventory import inventory_verification


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_file_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): file_sha(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
hashes = resolution["hashes"]
stage1 = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer = Path("/reference/generation-tools")
lock_path = Path("/reference/klean-toolchain.lock.json")

discovery = json.loads(discovery_path.read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
preflight = json.loads((generation / "preflight.json").read_text())
trust_inventory_path = generation / "trust-inventory.json"
trust_inventory = json.loads(trust_inventory_path.read_text())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
source_manifest = json.loads((producer / "source-manifest.json").read_text())
toolchain_lock = json.loads(lock_path.read_text())
inventory = inventory_verification(stage1)
validated_discovery = lemma_discovery_contract.validate_trust_boundary(
    stage1, discovery_path
)

computed = {
    "audit_mode_environment": os.environ.get("AUDIT_MODE"),
    "discovery_manifest_sha256": file_sha(discovery_path),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(producer),
    "k_audit_sha256": pipeline_contract.sha256_tree(k_audit),
    "k_workspace_sha256": pipeline_contract.sha256_tree(stage1),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "stage1_export_sha256": klean_export.tree_digest(stage1),
    "verification_sha256": file_sha(stage1 / "verification.k"),
    "obligation_map_sha256": file_sha(obligation_map_path),
    "trust_inventory_sha256": file_sha(trust_inventory_path),
    "klean_export_py_sha256": file_sha(producer / "klean_export.py"),
    "klean_py_sha256": file_sha(producer / "klean.py"),
}

expected_core = {
    key: hashes[key]
    for key in (
        "discovery_manifest_sha256",
        "generated_tree_sha256",
        "generation_producer_sources_sha256",
        "k_audit_sha256",
        "k_workspace_sha256",
        "klean_generation_sha256",
        "stage1_export_sha256",
    )
}

source_actual = regular_file_hashes(stage1)
source_expected = resolution["stage1_source_hashes"]
source_missing = sorted(set(source_expected) - set(source_actual))
source_extra = sorted(set(source_actual) - set(source_expected))
source_mismatches = {
    key: {"expected": source_expected[key], "actual": source_actual[key]}
    for key in sorted(set(source_expected) & set(source_actual))
    if source_expected[key] != source_actual[key]
}

image_from_audit_path = (
    "sha256:" + Path(resolution["generation_producer_sources"]).name
)
producer_files = {
    "klean.py": computed["klean_py_sha256"],
    "klean_export.py": computed["klean_export_py_sha256"],
}

checks = {
    "audit_mode_matches": computed["audit_mode_environment"] == resolution["mode"] == "CLASSIFICATION_ONLY",
    "semantics_mode_matches": resolution["semantics_mode"] == "SUPPLIED_SEMANTICS",
    "problem_matches": resolution["problem_id"] == "86-anti-shuffle",
    "core_launcher_hashes_match": all(computed[key] == value for key, value in expected_core.items()),
    "stage1_source_hashes_match_bijectively": not source_missing and not source_extra and not source_mismatches,
    "lean_hashes_are_null": hashes["lean_workspace_sha256"] is None and hashes["lean_invocation_sha256"] is None,
    "candidate_absent": not Path("/candidate").exists(),
    "inventory_hash_matches_discovery": inventory["inventory_sha256"] == discovery["inventory_sha256"] == validated_discovery["inventory_sha256"],
    "verification_hash_matches_input": computed["verification_sha256"] == input_manifest["verification_sha256"],
    "stage1_export_matches_input": computed["stage1_export_sha256"] == input_manifest["stage1_workspace_sha256"] == input_manifest["frozen_input_sha256"],
    "discovery_hash_matches_input": computed["discovery_manifest_sha256"] == input_manifest["stage3_discovery_manifest_sha256"],
    "input_inventory_matches": input_manifest["inventory_sha256"] == inventory["inventory_sha256"],
    "generator_generated_tree_matches": generator_manifest["generated_tree_sha256"] == computed["generated_tree_sha256"],
    "generator_obligation_map_hash_matches": generator_manifest["obligation_map_sha256"] == computed["obligation_map_sha256"],
    "generator_toolchain_matches_lock": generator_manifest["toolchain"] == toolchain_lock,
    "generator_stage1_provenance_matches": generator_manifest["provenance"]["stage1_workspace_sha256"] == computed["stage1_export_sha256"],
    "generator_stage3_provenance_matches": generator_manifest["provenance"]["stage3_discovery_manifest_sha256"] == computed["discovery_manifest_sha256"],
    "generator_inventory_provenance_matches": generator_manifest["provenance"]["inventory_sha256"] == inventory["inventory_sha256"],
    "producer_files_match_source_manifest": producer_files == source_manifest["files"],
    "producer_files_match_generator_manifest": computed["klean_export_py_sha256"] == generator_manifest["exporter_sha256"] and computed["klean_py_sha256"] == generator_manifest["klean_py_sha256"],
    "producer_image_ids_match": source_manifest["generator_image_id"] == generator_manifest["provenance"]["generator_image_id"] == image_from_audit_path,
    "producer_tree_matches_launcher": computed["generation_producer_sources_sha256"] == hashes["generation_producer_sources_sha256"],
    "export_stage1_matches": export_result["frozen_input_sha256"] == computed["stage1_export_sha256"],
    "export_discovery_matches": export_result["stage3_discovery_manifest_sha256"] == computed["discovery_manifest_sha256"],
    "export_generated_matches": export_result["generated_tree_sha256"] == computed["generated_tree_sha256"],
    "export_trust_inventory_matches": export_result["trust_inventory_sha256"] == computed["trust_inventory_sha256"],
    "structural_domain_source_rules_empty": input_manifest["source_rules"] == obligation_map["source_rules"] == [],
    "structural_obligations_empty": obligation_map["obligations"] == [] and generator_manifest["obligation_count"] == 0 and export_result["obligation_count"] == 0 and preflight["obligation_count"] == 0,
    "structural_trust_parameters_empty": obligation_map["trust_parameters"] == [],
    "fixed_generated_target_absent": generator_manifest["target"] is None and preflight["target"] is None and klean_export.target_statement(generated) is None,
    "status_consistent": export_result["status"] == preflight["status"] == resolution["selections"]["klean_generation"]["status"] == "KLEAN_NO_OBLIGATIONS",
    "generated_project_has_no_target_file": not (generated / "Klean86AntiShuffle" / "Target.lean").exists(),
}

report = {
    "computed": computed,
    "expected_core_launcher_hashes": expected_core,
    "stage1_source_hash_count": {
        "expected": len(source_expected),
        "actual": len(source_actual),
    },
    "stage1_source_hash_missing": source_missing,
    "stage1_source_hash_extra": source_extra,
    "stage1_source_hash_mismatches": source_mismatches,
    "source_manifest": source_manifest,
    "generator_image_id_from_audit_path": image_from_audit_path,
    "checks": checks,
}

print(json.dumps(report, indent=2, sort_keys=True))
if not all(checks.values()):
    raise SystemExit("one or more hash/structural checks failed")
print("RECORDED_HASH_AND_STRUCTURE_CHECKS=PASS")
