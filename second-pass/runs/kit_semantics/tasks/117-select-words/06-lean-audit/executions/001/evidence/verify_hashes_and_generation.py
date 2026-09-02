#!/usr/bin/env python3
"""Independent Stage 1/3/4 provenance, hash, and bijection verification."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract
from tools.k_rule_inventory import inventory_verification


STAGE1 = Path("/reference/k-proof")
STAGE2 = Path("/reference/k-audit")
DISCOVERY_PATH = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
LOCK_PATH = Path("/reference/klean-toolchain.lock.json")
AUDIT_PATH = Path("/audit-input.json")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_file_hashes(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        filenames.sort()
        base = Path(directory)
        for name in filenames:
            path = base / name
            mode = path.stat(follow_symlinks=False).st_mode
            if not stat.S_ISREG(mode):
                raise RuntimeError(f"non-regular source entry: {path}")
            hashes[path.relative_to(root).as_posix()] = sha256(path)
    return hashes


audit_document = json.loads(AUDIT_PATH.read_text())
resolution, resolved_hash = stage6_resolution_contract.verify_audit_input(
    audit_document
)
discovery = json.loads(DISCOVERY_PATH.read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)
obligation_map = json.loads(
    (GENERATED / "obligation-map.json").read_text()
)
preflight = json.loads((GENERATION / "preflight.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
trust_inventory = json.loads(
    (GENERATION / "trust-inventory.json").read_text()
)
lock = json.loads(LOCK_PATH.read_text())
inventory = inventory_verification(STAGE1)

stage1_pipeline_hash = pipeline_contract.sha256_tree(STAGE1)
stage1_export_hash = klean_export.tree_digest(STAGE1)
stage2_pipeline_hash = pipeline_contract.sha256_tree(STAGE2)
discovery_hash = sha256(DISCOVERY_PATH)
generation_pipeline_hash = pipeline_contract.sha256_tree(GENERATION)
producer_pipeline_hash = pipeline_contract.sha256_tree(PRODUCERS)
generated_export_hash = klean_export.tree_digest(GENERATED)
obligation_map_hash = sha256(GENERATED / "obligation-map.json")
trust_inventory_hash = sha256(GENERATION / "trust-inventory.json")
verification_hash = sha256(STAGE1 / "verification.k")
actual_stage1_files = regular_file_hashes(STAGE1)
recorded_stage1_files = resolution["stage1_source_hashes"]

classified_by_id = {
    entry["source_rule_id"]: entry for entry in discovery["rules"]
}
expected_buckets = {
    "definitions": [],
    "operational_rules": [],
    "proved_derived_lemmas": [],
    "source_rules": [],
}
bucket_for_class = {
    "DEFINITION": "definitions",
    "OPERATIONAL_RULE": "operational_rules",
    "PROVED_DERIVED_LEMMA": "proved_derived_lemmas",
    "DOMAIN_LEMMA": "source_rules",
}
for rule in inventory["rules"]:
    classification = classified_by_id[rule["source_rule_id"]]
    expected_buckets[bucket_for_class[classification["classification"]]].append(
        {**rule, **classification}
    )

checks = {
    "audit_input_self_hash_valid": (
        resolved_hash == audit_document["resolved_input_sha256"]
    ),
    "audit_mode_is_classification_only": (
        resolution["mode"] == "CLASSIFICATION_ONLY"
    ),
    "audit_semantics_mode_is_supplied": (
        resolution["semantics_mode"] == "SUPPLIED_SEMANTICS"
    ),
    "audit_problem_and_condition_match": (
        resolution["problem_id"] == "117-select-words"
        and resolution["condition"] == "kit-semantics"
    ),
    "stage1_pipeline_tree_matches_audit": (
        stage1_pipeline_hash == resolution["hashes"]["k_workspace_sha256"]
    ),
    "stage1_export_tree_matches_audit": (
        stage1_export_hash == resolution["hashes"]["stage1_export_sha256"]
    ),
    "stage2_pipeline_tree_matches_audit": (
        stage2_pipeline_hash == resolution["hashes"]["k_audit_sha256"]
    ),
    "discovery_file_matches_audit": (
        discovery_hash == resolution["hashes"]["discovery_manifest_sha256"]
    ),
    "generation_pipeline_tree_matches_audit": (
        generation_pipeline_hash
        == resolution["hashes"]["klean_generation_sha256"]
    ),
    "producer_pipeline_tree_matches_audit": (
        producer_pipeline_hash
        == resolution["hashes"]["generation_producer_sources_sha256"]
    ),
    "generated_export_tree_matches_audit": (
        generated_export_hash
        == resolution["hashes"]["generated_tree_sha256"]
    ),
    "stage1_source_file_set_exact": (
        set(actual_stage1_files) == set(recorded_stage1_files)
    ),
    "all_stage1_source_hashes_match": (
        actual_stage1_files == recorded_stage1_files
    ),
    "inventory_hash_matches_discovery": (
        inventory["inventory_sha256"] == discovery["inventory_sha256"]
    ),
    "input_manifest_definitions_exact": (
        input_manifest["definitions"] == expected_buckets["definitions"]
    ),
    "input_manifest_operational_rules_exact": (
        input_manifest["operational_rules"]
        == expected_buckets["operational_rules"]
    ),
    "input_manifest_derived_lemmas_exact": (
        input_manifest["proved_derived_lemmas"]
        == expected_buckets["proved_derived_lemmas"]
    ),
    "input_manifest_domain_source_rules_exact": (
        input_manifest["source_rules"] == expected_buckets["source_rules"]
    ),
    "input_manifest_inventory_hash": (
        input_manifest["inventory_sha256"] == inventory["inventory_sha256"]
    ),
    "input_manifest_verification_hash": (
        input_manifest["verification_sha256"] == verification_hash
    ),
    "input_manifest_stage1_hashes": (
        input_manifest["frozen_input_sha256"] == stage1_export_hash
        and input_manifest["stage1_workspace_sha256"] == stage1_export_hash
    ),
    "input_manifest_discovery_hash": (
        input_manifest["stage3_discovery_manifest_sha256"] == discovery_hash
    ),
    "generator_toolchain_matches_lock": generator_manifest["toolchain"] == lock,
    "generator_generated_tree_hash": (
        generator_manifest["generated_tree_sha256"] == generated_export_hash
    ),
    "generator_obligation_map_hash": (
        generator_manifest["obligation_map_sha256"] == obligation_map_hash
    ),
    "generator_provenance_hashes": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == stage1_export_hash
        and generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == discovery_hash
        and generator_manifest["provenance"]["inventory_sha256"]
        == inventory["inventory_sha256"]
    ),
    "obligation_map_source_bijection": (
        obligation_map["source_rules"] == expected_buckets["source_rules"]
        and obligation_map["obligations"] == []
        and obligation_map["trust_parameters"] == []
    ),
    "all_obligation_counts_zero": (
        generator_manifest["obligation_count"] == 0
        and preflight["obligation_count"] == 0
        and export_result["obligation_count"] == 0
    ),
    "all_statuses_no_obligations": (
        resolution["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
        and preflight["status"] == "KLEAN_NO_OBLIGATIONS"
        and export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    ),
    "all_targets_absent": (
        resolution["target"] is None
        and resolution["stage4_preflight"]["target"] is None
        and generator_manifest["target"] is None
        and preflight["target"] is None
        and klean_export.target_statement(GENERATED) is None
    ),
    "no_stage5_input_or_candidate": (
        resolution["lean_workspace"] is None
        and resolution["lean_invocation"] is None
        and resolution["stage5_result"] is None
        and not Path("/candidate").exists()
    ),
    "preflight_frozen_hashes": (
        preflight["frozen_input_sha256"] == stage1_export_hash
        and preflight["stage1_workspace_sha256"] == stage1_export_hash
        and preflight["stage3_discovery_manifest_sha256"] == discovery_hash
        and preflight["generated_tree_sha256"] == generated_export_hash
    ),
    "audit_embedded_preflight_exact": resolution["stage4_preflight"] == preflight,
    "export_result_hashes": (
        export_result["frozen_input_sha256"] == stage1_export_hash
        and export_result["stage3_discovery_manifest_sha256"] == discovery_hash
        and export_result["generated_tree_sha256"] == generated_export_hash
        and export_result["trust_inventory_sha256"] == trust_inventory_hash
    ),
    "trust_inventory_counts_and_parameters_consistent": (
        trust_inventory["designated_sorries"] == 0
        and trust_inventory["other_sorries"] == 0
        and preflight["trust_declaration_count"]
        == len(trust_inventory["allowlist"])
    ),
}

summary = {
    "checks": checks,
    "observed_hashes": {
        "resolved_input_sha256": resolved_hash,
        "stage1_pipeline_tree_sha256": stage1_pipeline_hash,
        "stage1_export_tree_sha256": stage1_export_hash,
        "stage2_pipeline_tree_sha256": stage2_pipeline_hash,
        "discovery_sha256": discovery_hash,
        "generation_pipeline_tree_sha256": generation_pipeline_hash,
        "producer_pipeline_tree_sha256": producer_pipeline_hash,
        "generated_export_tree_sha256": generated_export_hash,
        "verification_sha256": verification_hash,
        "obligation_map_sha256": obligation_map_hash,
        "trust_inventory_sha256": trust_inventory_hash,
    },
    "stage1_source_hash_count": len(actual_stage1_files),
    "stage1_missing_recorded_files": sorted(
        set(recorded_stage1_files) - set(actual_stage1_files)
    ),
    "stage1_extra_observed_files": sorted(
        set(actual_stage1_files) - set(recorded_stage1_files)
    ),
    "stage1_hash_mismatches": sorted(
        name
        for name in set(actual_stage1_files) & set(recorded_stage1_files)
        if actual_stage1_files[name] != recorded_stage1_files[name]
    ),
    "classification_bucket_counts": {
        key: len(value) for key, value in expected_buckets.items()
    },
    "obligation_map": obligation_map,
    "target_statement": klean_export.target_statement(GENERATED),
}
print(json.dumps(summary, indent=2, sort_keys=True))
if not all(checks.values()):
    raise SystemExit(1)
