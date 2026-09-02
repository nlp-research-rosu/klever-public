#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

from tools import klean_export
from tools import lemma_discovery_contract
from tools import pipeline_contract
from tools.k_rule_inventory import inventory_verification


REFERENCE = Path("/reference")
AUDIT_INPUT = Path("/audit-input.json")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_files(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in list(dirnames):
            path = base / name
            mode = path.lstat().st_mode
            if not stat.S_ISDIR(mode):
                raise RuntimeError(f"non-directory tree entry: {path}")
        for name in filenames:
            path = base / name
            mode = path.lstat().st_mode
            if not stat.S_ISREG(mode):
                raise RuntimeError(f"non-regular tree entry: {path}")
            result[path.relative_to(root).as_posix()] = file_sha256(path)
    return dict(sorted(result.items()))


def comparison(actual: object, expected: object) -> dict[str, object]:
    return {"actual": actual, "expected": expected, "match": actual == expected}


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    resolution = audit["resolution"]
    discovery_path = REFERENCE / "lemma-discovery.json"
    generation = REFERENCE / "klean-generation"
    generated = generation / "generated"
    producer = REFERENCE / "generation-tools"
    generator_manifest = json.loads(
        (generation / "generator-manifest.json").read_text()
    )
    source_manifest = json.loads((producer / "source-manifest.json").read_text())
    input_manifest = json.loads((generation / "input-manifest.json").read_text())
    export_result = json.loads((generation / "export-result.json").read_text())
    obligation_map_path = generated / "obligation-map.json"
    obligation_map = json.loads(obligation_map_path.read_text())
    trust_inventory_path = generation / "trust-inventory.json"
    lock = json.loads((REFERENCE / "klean-toolchain.lock.json").read_text())

    actual_stage1_files = regular_files(REFERENCE / "k-proof")
    expected_stage1_files = resolution["stage1_source_hashes"]
    stage1_file_mismatches = {
        path: {
            "actual": actual_stage1_files.get(path),
            "expected": expected_stage1_files.get(path),
        }
        for path in sorted(set(actual_stage1_files) | set(expected_stage1_files))
        if actual_stage1_files.get(path) != expected_stage1_files.get(path)
    }

    inventory = inventory_verification(REFERENCE / "k-proof")
    discovery = json.loads(discovery_path.read_text())
    validated = lemma_discovery_contract.validate_trust_boundary(
        REFERENCE / "k-proof", discovery_path
    )
    inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
    discovery_ids = [entry["source_rule_id"] for entry in discovery["rules"]]

    producer_image_from_path = (
        "sha256:" + Path(resolution["generation_producer_sources"]).name
    )
    producer_checks = {
        "klean_export.py": {
            "actual": file_sha256(producer / "klean_export.py"),
            "source_manifest": source_manifest["files"]["klean_export.py"],
            "generator_manifest": generator_manifest["exporter_sha256"],
        },
        "klean.py": {
            "actual": file_sha256(producer / "klean.py"),
            "source_manifest": source_manifest["files"]["klean.py"],
            "generator_manifest": generator_manifest["klean_py_sha256"],
        },
        "generator_image_id": {
            "source_manifest": source_manifest["generator_image_id"],
            "generator_manifest": generator_manifest["provenance"][
                "generator_image_id"
            ],
            "audit_input_path_binding": producer_image_from_path,
        },
        "producer_tree_sha256": comparison(
            pipeline_contract.sha256_tree(producer),
            resolution["hashes"]["generation_producer_sources_sha256"],
        ),
    }
    producer_checks["all_match"] = (
        len(
            {
                producer_checks["klean_export.py"]["actual"],
                producer_checks["klean_export.py"]["source_manifest"],
                producer_checks["klean_export.py"]["generator_manifest"],
            }
        )
        == 1
        and len(
            {
                producer_checks["klean.py"]["actual"],
                producer_checks["klean.py"]["source_manifest"],
                producer_checks["klean.py"]["generator_manifest"],
            }
        )
        == 1
        and len(
            {
                producer_checks["generator_image_id"]["source_manifest"],
                producer_checks["generator_image_id"]["generator_manifest"],
                producer_checks["generator_image_id"]["audit_input_path_binding"],
            }
        )
        == 1
        and producer_checks["producer_tree_sha256"]["match"]
    )

    expected_ids = [
        rule["source_rule_id"] for rule in input_manifest["source_rules"]
    ]
    observed_ids = [
        obligation["source_rule_id"]
        for obligation in obligation_map["obligations"]
    ]
    source_obligation_detail_errors: list[str] = []
    for index, obligation in enumerate(obligation_map["obligations"]):
        if index >= len(input_manifest["source_rules"]):
            source_obligation_detail_errors.append(
                f"extra obligation at index {index}"
            )
            continue
        source_rule = input_manifest["source_rules"][index]
        if obligation.get("source_span") != {
            "start_line": source_rule["start_line"],
            "end_line": source_rule["end_line"],
        }:
            source_obligation_detail_errors.append(
                f"source span mismatch at index {index}"
            )
        for key in (
            "normalized_sha256",
            "inventory_sha256",
            "discovery_manifest_sha256",
        ):
            if obligation.get(key) != source_rule.get(key):
                source_obligation_detail_errors.append(
                    f"{key} mismatch at index {index}"
                )
        conjunct = obligation.get("lean_conjunct")
        if (
            not isinstance(conjunct, str)
            or not conjunct
            or obligation.get("lean_conjunct_sha256")
            != klean_export.sha256_text(conjunct)
        ):
            source_obligation_detail_errors.append(
                f"Lean conjunct/hash mismatch at index {index}"
            )

    expected_target_definition = klean_export.expected_target_definition(
        obligation_map
    )
    actual_target = klean_export.target_statement(generated)
    target_consistent = (
        expected_target_definition is None
        and actual_target is None
        and generator_manifest["target"] is None
    ) or (
        expected_target_definition is not None
        and actual_target == generator_manifest["target"]
        and actual_target.get("definition_sha256")
        == klean_export.sha256_text(expected_target_definition)
    )

    hash_checks = {
        "discovery_manifest_sha256": comparison(
            file_sha256(discovery_path),
            resolution["hashes"]["discovery_manifest_sha256"],
        ),
        "k_workspace_sha256": comparison(
            pipeline_contract.sha256_tree(REFERENCE / "k-proof"),
            resolution["hashes"]["k_workspace_sha256"],
        ),
        "stage1_export_sha256": comparison(
            klean_export.tree_digest(REFERENCE / "k-proof"),
            resolution["hashes"]["stage1_export_sha256"],
        ),
        "k_audit_sha256": comparison(
            pipeline_contract.sha256_tree(REFERENCE / "k-audit"),
            resolution["hashes"]["k_audit_sha256"],
        ),
        "klean_generation_sha256": comparison(
            pipeline_contract.sha256_tree(generation),
            resolution["hashes"]["klean_generation_sha256"],
        ),
        "generated_tree_sha256": comparison(
            klean_export.tree_digest(generated),
            resolution["hashes"]["generated_tree_sha256"],
        ),
        "stage1_source_hashes": {
            "actual_count": len(actual_stage1_files),
            "expected_count": len(expected_stage1_files),
            "mismatches": stage1_file_mismatches,
            "match": not stage1_file_mismatches,
        },
    }

    manifest_checks = {
        "input_frozen_hash": comparison(
            input_manifest["frozen_input_sha256"],
            resolution["hashes"]["stage1_export_sha256"],
        ),
        "input_stage1_hash": comparison(
            input_manifest["stage1_workspace_sha256"],
            resolution["hashes"]["stage1_export_sha256"],
        ),
        "input_discovery_hash": comparison(
            input_manifest["stage3_discovery_manifest_sha256"],
            resolution["hashes"]["discovery_manifest_sha256"],
        ),
        "input_inventory_hash": comparison(
            input_manifest["inventory_sha256"],
            inventory["inventory_sha256"],
        ),
        "input_verification_hash": comparison(
            input_manifest["verification_sha256"],
            file_sha256(REFERENCE / "k-proof" / "verification.k"),
        ),
        "generator_generated_hash": comparison(
            generator_manifest["generated_tree_sha256"],
            resolution["hashes"]["generated_tree_sha256"],
        ),
        "generator_stage1_hash": comparison(
            generator_manifest["provenance"]["stage1_workspace_sha256"],
            resolution["hashes"]["stage1_export_sha256"],
        ),
        "generator_discovery_hash": comparison(
            generator_manifest["provenance"][
                "stage3_discovery_manifest_sha256"
            ],
            resolution["hashes"]["discovery_manifest_sha256"],
        ),
        "generator_inventory_hash": comparison(
            generator_manifest["provenance"]["inventory_sha256"],
            inventory["inventory_sha256"],
        ),
        "generator_obligation_map_hash": comparison(
            generator_manifest["obligation_map_sha256"],
            file_sha256(obligation_map_path),
        ),
        "generator_toolchain_lock": comparison(
            generator_manifest["toolchain"], lock
        ),
        "export_result_frozen_hash": comparison(
            export_result["frozen_input_sha256"],
            resolution["hashes"]["stage1_export_sha256"],
        ),
        "export_result_discovery_hash": comparison(
            export_result["stage3_discovery_manifest_sha256"],
            resolution["hashes"]["discovery_manifest_sha256"],
        ),
        "export_result_generated_hash": comparison(
            export_result["generated_tree_sha256"],
            resolution["hashes"]["generated_tree_sha256"],
        ),
        "export_result_trust_inventory_hash": comparison(
            export_result["trust_inventory_sha256"],
            file_sha256(trust_inventory_path),
        ),
    }

    output = {
        "launcher": {
            "environment_AUDIT_MODE": os.environ.get("AUDIT_MODE"),
            "audit_input_mode": resolution["mode"],
            "mode_match": os.environ.get("AUDIT_MODE") == resolution["mode"],
            "condition": resolution["condition"],
            "problem_id": resolution["problem_id"],
            "semantics_mode": resolution["semantics_mode"],
            "candidate_exists": Path("/candidate").exists(),
        },
        "producer_integrity": producer_checks,
        "inventory_reconstruction": inventory,
        "discovery_manifest": discovery,
        "inventory_bijection": {
            "inventory_ids": inventory_ids,
            "discovery_ids": discovery_ids,
            "same_order": inventory_ids == discovery_ids,
            "inventory_unique": len(inventory_ids) == len(set(inventory_ids)),
            "discovery_unique": len(discovery_ids) == len(set(discovery_ids)),
            "inventory_hash_match": (
                inventory["inventory_sha256"] == discovery["inventory_sha256"]
            ),
            "trusted_contract_validation_succeeded": validated[
                "inventory_sha256"
            ]
            == inventory["inventory_sha256"],
        },
        "hash_checks": hash_checks,
        "manifest_checks": manifest_checks,
        "source_obligation_bijection": {
            "input_source_rules": input_manifest["source_rules"],
            "obligation_map_source_rules": obligation_map["source_rules"],
            "obligations": obligation_map["obligations"],
            "trust_parameters": obligation_map["trust_parameters"],
            "expected_ids": expected_ids,
            "observed_ids": observed_ids,
            "same_order": expected_ids == observed_ids,
            "unique_obligation_ids": len(observed_ids) == len(set(observed_ids)),
            "source_rules_match": (
                obligation_map["source_rules"]
                == input_manifest["source_rules"]
            ),
            "detail_errors": source_obligation_detail_errors,
            "obligation_count_manifest": generator_manifest["obligation_count"],
            "obligation_count_actual": len(obligation_map["obligations"]),
        },
        "target_identity": {
            "expected_definition": expected_target_definition,
            "actual_target": actual_target,
            "generator_manifest_target": generator_manifest["target"],
            "consistent": target_consistent,
        },
        "status_identity": {
            "selected_status": resolution["selections"]["klean_generation"][
                "status"
            ],
            "export_status": export_result["status"],
            "obligation_count": len(obligation_map["obligations"]),
            "candidate_absent": not Path("/candidate").exists(),
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
