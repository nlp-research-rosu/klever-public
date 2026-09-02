#!/usr/bin/env python3
"""Independent Stage 3/4 integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from collections import Counter
from pathlib import Path
from typing import Any

from tools import (
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)
from tools.k_rule_inventory import inventory_verification


AUDIT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
K_AUDIT = Path("/reference/k-audit")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    assert isinstance(value, dict)
    return value


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_files(root: Path) -> list[Path]:
    result: list[Path] = []
    for path in sorted(root.rglob("*")):
        mode = path.lstat().st_mode
        assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), path
        if stat.S_ISREG(mode):
            result.append(path)
    return result


audit_document = load(AUDIT_INPUT)
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
expected_hashes = resolution["hashes"]

inventory = inventory_verification(WORKSPACE)
discovery = load(DISCOVERY)
validated = lemma_discovery_contract.validate_trust_boundary(
    WORKSPACE, DISCOVERY
)
input_manifest = load(GENERATION / "input-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
obligation_map = load(GENERATED / "obligation-map.json")
export_result = load(GENERATION / "export-result.json")
recorded_preflight = load(GENERATION / "preflight.json")
rerun_preflight = load(Path("/audit-output/evidence/preflight-rerun.json"))
trust_inventory = load(GENERATION / "trust-inventory.json")
source_manifest = load(PRODUCERS / "source-manifest.json")
toolchain_lock = load(Path("/reference/klean-toolchain.lock.json"))

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
verification_lines = (WORKSPACE / "verification.k").read_text().splitlines()
manual_rule_checks: list[dict[str, Any]] = []
for rule in inventory["rules"]:
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    source_slice = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    manual_rule_checks.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "span_matches_source": source_slice == rule["text"],
            "normalized_sha256_matches": (
                normalized_sha256 == rule["normalized_sha256"]
            ),
            "source_rule_id_matches": (
                rule["source_rule_id"] == f"rule-{normalized_sha256}"
            ),
        }
    )

classification_by_id = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}
classification_sequence = [
    classification_by_id[source_rule_id] for source_rule_id in inventory_ids
]
simplification_policy_ok = all(
    "simplification" not in rule["attributes"]
    or classification_by_id[rule["source_rule_id"]]
    in {"DEFINITION", "DOMAIN_LEMMA"}
    for rule in inventory["rules"]
)

discovery_hash = file_sha256(DISCOVERY)
expected_source_rules = klean_export._domain_source_rules(
    validated, discovery_hash
)
obligations = obligation_map["obligations"]
obligation_ids = [entry["source_rule_id"] for entry in obligations]
source_rule_ids = [
    entry["source_rule_id"] for entry in expected_source_rules
]
target = klean_export.target_statement(GENERATED)
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)

producer_file_hashes = {
    name: file_sha256(PRODUCERS / name)
    for name in ("klean_export.py", "klean.py")
}
producer_observed_names = {
    path.relative_to(PRODUCERS).as_posix() for path in regular_files(PRODUCERS)
}
producer_image_key = resolution["generation_producer_sources"].rstrip(
    "/"
).split("/")[-1]

observed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(WORKSPACE),
    "stage1_export_sha256": klean_export.tree_digest(WORKSPACE),
    "discovery_manifest_sha256": pipeline_contract.sha256_file(DISCOVERY),
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
    path.relative_to(WORKSPACE).as_posix(): file_sha256(path)
    for path in regular_files(WORKSPACE)
}

trust_inventory_hash = file_sha256(GENERATION / "trust-inventory.json")
obligation_map_hash = file_sha256(GENERATED / "obligation-map.json")
verification_hash = file_sha256(WORKSPACE / "verification.k")

checks = {
    "audit_mode_env_matches": (
        os.environ.get("AUDIT_MODE") == resolution["mode"]
    ),
    "audit_mode_is_classification_only": (
        resolution["mode"] == "CLASSIFICATION_ONLY"
    ),
    "audit_input_resolved_digest_matches": (
        resolved_digest == audit_document["resolved_input_sha256"]
    ),
    "all_launcher_hashes_match": observed_hashes == expected_hashes,
    "stage1_source_hashes_match": (
        stage1_source_hashes == resolution["stage1_source_hashes"]
    ),
    "inventory_hash_matches_discovery": (
        inventory["inventory_sha256"] == discovery["inventory_sha256"]
    ),
    "inventory_ids_same_order": inventory_ids == discovery_ids,
    "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
    "inventory_spans_hashes_and_ids_recomputed": all(
        item["span_matches_source"]
        and item["normalized_sha256_matches"]
        and item["source_rule_id_matches"]
        for item in manual_rule_checks
    ),
    "inventory_source_order_strict": all(
        left["start_line"] < right["start_line"]
        for left, right in zip(
            inventory["rules"][:-1],
            inventory["rules"][1:],
            strict=True,
        )
    ),
    "simplification_policy_ok": simplification_policy_ok,
    "input_inventory_matches": (
        input_manifest["inventory_sha256"] == inventory["inventory_sha256"]
    ),
    "input_verification_hash_matches": (
        input_manifest["verification_sha256"] == verification_hash
    ),
    "input_source_rules_exact": (
        input_manifest["source_rules"] == expected_source_rules
    ),
    "obligation_map_source_rules_exact": (
        obligation_map["source_rules"] == expected_source_rules
    ),
    "source_rule_obligation_ids_bijective": (
        obligation_ids == source_rule_ids
        and len(obligation_ids) == len(set(obligation_ids))
    ),
    "obligation_counts_all_exact": (
        len(obligations)
        == generator_manifest["obligation_count"]
        == export_result["obligation_count"]
        == recorded_preflight["obligation_count"]
        == rerun_preflight["obligation_count"]
        == 0
    ),
    "trust_parameters_empty": obligation_map["trust_parameters"] == [],
    "fixed_generated_target_absent": (
        target is None
        and expected_target_definition is None
        and generator_manifest["target"] is None
        and recorded_preflight["target"] is None
        and rerun_preflight["target"] is None
        and resolution["target"] is None
    ),
    "no_stage5_candidate": not Path("/candidate").exists(),
    "no_domain_rules": validated["domain_lemmas"] == [],
    "no_proved_derived_rules": validated["proved_derived_lemmas"] == [],
    "export_status_exact": (
        export_result["status"] == "KLEAN_NO_OBLIGATIONS"
        and recorded_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
        and rerun_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
        and resolution["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
    ),
    "rerun_preflight_exactly_matches_recorded": (
        rerun_preflight == recorded_preflight
    ),
    "generator_toolchain_matches_lock": (
        generator_manifest["toolchain"] == toolchain_lock
    ),
    "generator_obligation_map_hash_matches": (
        generator_manifest["obligation_map_sha256"] == obligation_map_hash
    ),
    "generator_generated_tree_hash_matches": (
        generator_manifest["generated_tree_sha256"]
        == observed_hashes["generated_tree_sha256"]
    ),
    "export_trust_inventory_hash_matches": (
        export_result["trust_inventory_sha256"] == trust_inventory_hash
    ),
    "producer_bundle_exact_files": producer_observed_names
    == {"source-manifest.json", "klean_export.py", "klean.py"},
    "producer_file_hashes_match_source_manifest": (
        producer_file_hashes == source_manifest["files"]
    ),
    "producer_file_hashes_match_generator_manifest": (
        producer_file_hashes["klean_export.py"]
        == generator_manifest["exporter_sha256"]
        and producer_file_hashes["klean.py"]
        == generator_manifest["klean_py_sha256"]
    ),
    "producer_image_id_matches_all_bindings": (
        source_manifest["generator_image_id"]
        == generator_manifest["provenance"]["generator_image_id"]
        == f"sha256:{producer_image_key}"
    ),
    "producer_tree_hash_matches_launcher": (
        observed_hashes["generation_producer_sources_sha256"]
        == expected_hashes["generation_producer_sources_sha256"]
    ),
    "generated_tree_hash_matches_launcher": (
        observed_hashes["generated_tree_sha256"]
        == expected_hashes["generated_tree_sha256"]
    ),
    "stage1_and_discovery_provenance_match": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == observed_hashes["stage1_export_sha256"]
        and generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == observed_hashes["discovery_manifest_sha256"]
    ),
    "inventory_provenance_matches": (
        generator_manifest["provenance"]["inventory_sha256"]
        == inventory["inventory_sha256"]
    ),
}

report = {
    "status": "PASS" if all(checks.values()) else "FAIL",
    "checks": checks,
    "classification_counts": dict(Counter(classification_sequence)),
    "inventory": {
        "rule_count": len(inventory_ids),
        "inventory_sha256": inventory["inventory_sha256"],
        "verification_sha256": inventory["verification_sha256"],
        "verification_module": inventory["verification_module"],
        "verification_modules": inventory["verification_modules"],
        "manual_rule_checks": manual_rule_checks,
    },
    "stage4": {
        "source_rule_count": len(expected_source_rules),
        "obligation_count": len(obligations),
        "target": target,
        "trust_parameter_count": len(obligation_map["trust_parameters"]),
    },
    "producer": {
        "image_id": source_manifest["generator_image_id"],
        "file_hashes": producer_file_hashes,
        "tree_sha256": observed_hashes[
            "generation_producer_sources_sha256"
        ],
    },
    "expected_hashes": expected_hashes,
    "observed_hashes": observed_hashes,
    "resolved_input_sha256": resolved_digest,
}

print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(0 if report["status"] == "PASS" else 1)
