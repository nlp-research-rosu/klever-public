#!/usr/bin/env python3
"""Recompute launcher, producer, manifest, bijection, and target bindings."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract
from tools.lemma_discovery_contract import validate_trust_boundary


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
expected_hashes = resolution["hashes"]

computed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
    "stage1_export_sha256": klean_export.tree_digest(K_WORKSPACE),
    "discovery_manifest_sha256": sha256_file(DISCOVERY),
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        PRODUCERS
    ),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

stage1_source_hashes = {
    path.relative_to(K_WORKSPACE).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        K_WORKSPACE, "mounted Stage 1 workspace"
    )
}
expected_stage1_source_hashes = resolution["stage1_source_hashes"]
source_mismatches = sorted(
    key
    for key in set(stage1_source_hashes) | set(expected_stage1_source_hashes)
    if stage1_source_hashes.get(key) != expected_stage1_source_hashes.get(key)
)

generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
obligation_map = json.loads(
    (GENERATED / "obligation-map.json").read_text()
)
trust_inventory = json.loads(
    (GENERATION / "trust-inventory.json").read_text()
)
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
recorded_preflight = json.loads((GENERATION / "preflight.json").read_text())
validated_discovery = validate_trust_boundary(K_WORKSPACE, DISCOVERY)

producer_hashes = {
    "klean_export.py": sha256_file(PRODUCERS / "klean_export.py"),
    "klean.py": sha256_file(PRODUCERS / "klean.py"),
}
producer_image = generator_manifest["provenance"]["generator_image_id"]
audit_producer_path = Path(resolution["generation_producer_sources"])

domain_ids = [
    rule["source_rule_id"] for rule in validated_discovery["domain_lemmas"]
]
input_source_ids = [
    rule["source_rule_id"] for rule in input_manifest["source_rules"]
]
mapped_source_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"] for obligation in obligation_map["obligations"]
]

recorded_build = recorded_preflight["diagnostics"][1]
recorded_build_tail_hash = hashlib.sha256(
    recorded_build["output_tail"].encode()
).hexdigest()

checks = {
    "launcher_mode_and_problem_match_environment": (
        os.environ.get("AUDIT_MODE") == resolution["mode"]
        and resolution["mode"] == "CLASSIFICATION_ONLY"
        and resolution["problem_id"] == "52-below-threshold"
        and resolution["condition"] == "kit-semantics"
        and resolution["semantics_mode"] == "SUPPLIED_SEMANTICS"
    ),
    "audit_input_envelope_digest_valid": (
        resolved_digest == audit_document["resolved_input_sha256"]
    ),
    "all_launcher_hashes_match": computed_hashes == expected_hashes,
    "all_stage1_source_hashes_match": not source_mismatches,
    "producer_file_hashes_match_source_manifest": (
        producer_hashes == source_manifest["files"]
    ),
    "producer_file_hashes_match_generator_manifest": (
        producer_hashes["klean_export.py"] == generator_manifest["exporter_sha256"]
        and producer_hashes["klean.py"] == generator_manifest["klean_py_sha256"]
    ),
    "producer_image_matches_source_manifest": (
        producer_image == source_manifest["generator_image_id"]
    ),
    "producer_image_matches_audit_path": (
        audit_producer_path.name == producer_image.removeprefix("sha256:")
    ),
    "toolchain_lock_matches_generator": (
        generator_manifest["toolchain"]
        == json.loads(Path("/reference/klean-toolchain.lock.json").read_text())
    ),
    "verification_hash_matches_input_manifest": (
        sha256_file(K_WORKSPACE / "verification.k")
        == input_manifest["verification_sha256"]
    ),
    "inventory_hash_matches_all_manifests": (
        validated_discovery["inventory_sha256"]
        == input_manifest["inventory_sha256"]
        == generator_manifest["provenance"]["inventory_sha256"]
    ),
    "stage1_tree_hash_matches_all_manifests": (
        computed_hashes["stage1_export_sha256"]
        == input_manifest["frozen_input_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == generator_manifest["provenance"]["stage1_workspace_sha256"]
        == export_result["frozen_input_sha256"]
    ),
    "discovery_hash_matches_all_manifests": (
        computed_hashes["discovery_manifest_sha256"]
        == input_manifest["stage3_discovery_manifest_sha256"]
        == generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == export_result["stage3_discovery_manifest_sha256"]
    ),
    "generated_tree_hash_matches_all_manifests": (
        computed_hashes["generated_tree_sha256"]
        == generator_manifest["generated_tree_sha256"]
        == export_result["generated_tree_sha256"]
    ),
    "obligation_map_hash_matches": (
        sha256_file(GENERATED / "obligation-map.json")
        == generator_manifest["obligation_map_sha256"]
    ),
    "trust_inventory_hash_matches": (
        sha256_file(GENERATION / "trust-inventory.json")
        == export_result["trust_inventory_sha256"]
    ),
    "domain_source_obligation_ordered_bijection": (
        domain_ids == input_source_ids == mapped_source_ids == obligation_ids
        and len(obligation_ids) == len(set(obligation_ids))
    ),
    "all_obligation_counts_zero": (
        len(domain_ids)
        == len(obligation_map["obligations"])
        == generator_manifest["obligation_count"]
        == export_result["obligation_count"]
        == recorded_preflight["obligation_count"]
        == 0
    ),
    "no_trust_parameters_for_empty_domain": (
        obligation_map["trust_parameters"] == []
    ),
    "no_expected_or_generated_target": (
        klean_export.expected_target_definition(obligation_map) is None
        and klean_export.target_statement(GENERATED) is None
        and generator_manifest["target"] is None
        and resolution["target"] is None
    ),
    "no_stage5_result_or_candidate": (
        resolution["stage5_result"] is None
        and resolution["lean_workspace"] is None
        and resolution["lean_invocation"] is None
        and not Path("/candidate").exists()
    ),
    "export_and_preflight_status_are_no_obligations": (
        export_result["status"] == "KLEAN_NO_OBLIGATIONS"
        and recorded_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
        and resolution["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
    ),
    "recorded_preflight_build_tail_hash_is_self_consistent": (
        recorded_build_tail_hash == recorded_build["output_sha256"]
    ),
    "trust_inventory_has_no_sorries": (
        trust_inventory["designated_sorries"] == 0
        and trust_inventory["other_sorries"] == 0
    ),
}

report = {
    "checks": checks,
    "computed_hashes": computed_hashes,
    "expected_hashes": expected_hashes,
    "stage1_source_hash_count": len(stage1_source_hashes),
    "stage1_source_hash_mismatches": source_mismatches,
    "producer_hashes": producer_hashes,
    "producer_image": producer_image,
    "domain_ids": domain_ids,
    "input_source_ids": input_source_ids,
    "mapped_source_ids": mapped_source_ids,
    "obligation_ids": obligation_ids,
    "recorded_preflight_build_output_sha256": recorded_build["output_sha256"],
    "recomputed_recorded_build_tail_sha256": recorded_build_tail_hash,
    "target_statement": klean_export.target_statement(GENERATED),
}
print(json.dumps(report, indent=2, sort_keys=True))

if not all(checks.values()):
    raise SystemExit(1)
