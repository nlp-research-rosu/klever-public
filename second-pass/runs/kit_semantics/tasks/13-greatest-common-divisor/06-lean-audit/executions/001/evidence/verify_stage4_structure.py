#!/usr/bin/env python3
"""Independent hash, manifest, bijection, and null-target checks for Stage 4."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import inventory_verification
from tools.pipeline_contract import _walk_regular_files, sha256_file, sha256_tree


AUDIT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise TypeError(f"{path} is not a JSON object")
    return value


def main() -> None:
    audit_input = read_json(AUDIT_INPUT)
    resolution = audit_input["resolution"]
    recorded_hashes = resolution["hashes"]
    discovery = read_json(DISCOVERY)
    input_manifest = read_json(GENERATION / "input-manifest.json")
    generator_manifest = read_json(GENERATION / "generator-manifest.json")
    export_result = read_json(GENERATION / "export-result.json")
    obligation_map = read_json(GENERATED / "obligation-map.json")
    trust_inventory_path = GENERATION / "trust-inventory.json"
    toolchain_lock = read_json(Path("/reference/klean-toolchain.lock.json"))

    inventory = inventory_verification(WORKSPACE)
    classified_by_id = {
        entry["source_rule_id"]: entry for entry in discovery["rules"]
    }
    canonical_classified = [
        {**rule, **classified_by_id[rule["source_rule_id"]]}
        for rule in inventory["rules"]
    ]
    expected_definitions = [
        rule
        for rule in canonical_classified
        if rule["classification"] == "DEFINITION"
    ]
    expected_operational = [
        rule
        for rule in canonical_classified
        if rule["classification"] == "OPERATIONAL_RULE"
    ]
    expected_proved = [
        rule
        for rule in canonical_classified
        if rule["classification"] == "PROVED_DERIVED_LEMMA"
    ]
    stage3_domain = [
        rule
        for rule in canonical_classified
        if rule["classification"] == "DOMAIN_LEMMA"
    ]

    actual_stage1_source_hashes = {
        path.relative_to(WORKSPACE).as_posix(): sha256_file(path)
        for path in _walk_regular_files(WORKSPACE, "mounted Stage 1 workspace")
    }
    recorded_stage1_source_hashes = resolution["stage1_source_hashes"]
    source_hash_missing = sorted(
        set(recorded_stage1_source_hashes) - set(actual_stage1_source_hashes)
    )
    source_hash_extra = sorted(
        set(actual_stage1_source_hashes) - set(recorded_stage1_source_hashes)
    )
    source_hash_mismatches = sorted(
        name
        for name in set(actual_stage1_source_hashes)
        & set(recorded_stage1_source_hashes)
        if actual_stage1_source_hashes[name] != recorded_stage1_source_hashes[name]
    )

    observed_hashes = {
        "k_workspace_sha256": sha256_tree(WORKSPACE),
        "stage1_export_sha256": klean_export.tree_digest(WORKSPACE),
        "discovery_manifest_sha256": hashlib.sha256(
            DISCOVERY.read_bytes()
        ).hexdigest(),
        "k_audit_sha256": sha256_tree(K_AUDIT),
        "klean_generation_sha256": sha256_tree(GENERATION),
        "generation_producer_sources_sha256": sha256_tree(PRODUCERS),
        "generated_tree_sha256": klean_export.tree_digest(GENERATED),
        "lean_workspace_sha256": None,
        "lean_invocation_sha256": None,
    }

    actual_target = klean_export.target_statement(GENERATED)
    generated_files = sorted(
        path.relative_to(GENERATED).as_posix()
        for path in GENERATED.rglob("*")
        if path.is_file()
    )
    expected_empty_obligation_map = {
        "schema_version": 3,
        "source_rules": [],
        "obligations": [],
        "trust_parameters": [],
    }
    obligation_ids = [
        obligation.get("source_rule_id")
        for obligation in obligation_map.get("obligations", [])
        if isinstance(obligation, dict)
    ]
    source_rule_ids = [
        rule.get("source_rule_id")
        for rule in obligation_map.get("source_rules", [])
        if isinstance(rule, dict)
    ]

    checks = {
        "audit_mode_classification_only": (
            resolution.get("mode") == "CLASSIFICATION_ONLY"
        ),
        "environment_candidate_absent": not Path("/candidate").exists(),
        "all_launcher_hashes_match": observed_hashes == recorded_hashes,
        "stage1_source_hash_map_exact": (
            not source_hash_missing
            and not source_hash_extra
            and not source_hash_mismatches
            and actual_stage1_source_hashes == recorded_stage1_source_hashes
        ),
        "input_inventory_hash_matches": (
            input_manifest.get("inventory_sha256")
            == inventory["inventory_sha256"]
            == discovery["inventory_sha256"]
        ),
        "input_definitions_exact": (
            input_manifest.get("definitions") == expected_definitions
        ),
        "input_operational_rules_exact": (
            input_manifest.get("operational_rules") == expected_operational
        ),
        "input_proved_derived_lemmas_exact": (
            input_manifest.get("proved_derived_lemmas") == expected_proved
        ),
        "stage3_domain_set_empty": stage3_domain == [],
        "input_source_rules_empty": input_manifest.get("source_rules") == [],
        "obligation_map_exactly_empty": (
            obligation_map == expected_empty_obligation_map
        ),
        "obligation_identity_order_bijective": (
            source_rule_ids == obligation_ids == []
            and len(obligation_ids) == len(set(obligation_ids))
        ),
        "generator_obligation_count_zero": (
            generator_manifest.get("obligation_count") == 0
        ),
        "generator_obligation_map_hash_matches": (
            generator_manifest.get("obligation_map_sha256")
            == hashlib.sha256(
                (GENERATED / "obligation-map.json").read_bytes()
            ).hexdigest()
        ),
        "generator_target_null": generator_manifest.get("target") is None,
        "actual_generated_target_null": actual_target is None,
        "audit_input_target_null": resolution.get("target") is None,
        "export_no_obligations_exact": (
            export_result.get("status") == "KLEAN_NO_OBLIGATIONS"
            and export_result.get("obligation_count") == 0
        ),
        "export_hash_bindings_match": (
            export_result.get("frozen_input_sha256")
            == observed_hashes["stage1_export_sha256"]
            and export_result.get("stage3_discovery_manifest_sha256")
            == observed_hashes["discovery_manifest_sha256"]
            and export_result.get("generated_tree_sha256")
            == observed_hashes["generated_tree_sha256"]
            and export_result.get("trust_inventory_sha256")
            == hashlib.sha256(trust_inventory_path.read_bytes()).hexdigest()
        ),
        "generator_toolchain_exact": (
            generator_manifest.get("toolchain") == toolchain_lock
        ),
        "no_generated_target_file": not any(
            Path(name).name == "Target.lean" for name in generated_files
        ),
        "no_stage5_result": resolution.get("stage5_result") is None,
    }

    result = {
        "recorded_hashes": recorded_hashes,
        "observed_hashes": observed_hashes,
        "stage1_source_file_count": len(actual_stage1_source_hashes),
        "stage1_source_hash_missing": source_hash_missing,
        "stage1_source_hash_extra": source_hash_extra,
        "stage1_source_hash_mismatches": source_hash_mismatches,
        "inventory_sha256": inventory["inventory_sha256"],
        "classification_counts": {
            "DEFINITION": len(expected_definitions),
            "OPERATIONAL_RULE": len(expected_operational),
            "PROVED_DERIVED_LEMMA": len(expected_proved),
            "DOMAIN_LEMMA": len(stage3_domain),
        },
        "obligation_map": obligation_map,
        "actual_target": actual_target,
        "generator_target": generator_manifest.get("target"),
        "audit_input_target": resolution.get("target"),
        "generated_files": generated_files,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
