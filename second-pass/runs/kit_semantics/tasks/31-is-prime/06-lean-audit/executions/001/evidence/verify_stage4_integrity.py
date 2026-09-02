#!/usr/bin/env python3
"""Independent hash, classification, obligation, and null-target checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import inventory_verification
from tools.pipeline_contract import sha256_file, sha256_tree


ROOT = Path("/reference")
K_PROOF = ROOT / "k-proof"
GENERATION = ROOT / "klean-generation"
GENERATED = GENERATION / "generated"


def regular_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for directory, directory_names, file_names in os.walk(root):
        directory_names.sort()
        file_names.sort()
        for name in file_names:
            path = Path(directory) / name
            if not stat.S_ISREG(path.lstat().st_mode):
                raise RuntimeError(f"non-regular entry in {root}: {path}")
            paths.append(path)
    return paths


def main() -> None:
    audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
    discovery = json.loads((ROOT / "lemma-discovery.json").read_text())
    independent = json.loads(
        Path("/audit-output/evidence/independent_classification.json").read_text()
    )
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    generator = json.loads((GENERATION / "generator-manifest.json").read_text())
    export_result = json.loads((GENERATION / "export-result.json").read_text())
    preflight = json.loads((GENERATION / "preflight.json").read_text())
    obligations = json.loads((GENERATED / "obligation-map.json").read_text())
    inventory = inventory_verification(K_PROOF)

    discovery_hash = sha256_file(ROOT / "lemma-discovery.json")
    pipeline_stage1_hash = sha256_tree(K_PROOF)
    export_stage1_hash = klean_export.tree_digest(K_PROOF)
    k_audit_hash = sha256_tree(ROOT / "k-audit")
    generation_hash = sha256_tree(GENERATION)
    generated_hash = klean_export.tree_digest(GENERATED)
    trust_hash = sha256_file(GENERATION / "trust-inventory.json")
    obligation_map_hash = sha256_file(GENERATED / "obligation-map.json")

    expected_source_hashes = audit["stage1_source_hashes"]
    observed_source_hashes = {
        path.relative_to(K_PROOF).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in regular_files(K_PROOF)
    }

    independent_pairs = [
        (rule["source_rule_id"], rule["classification"])
        for rule in independent["rules"]
    ]
    protected_pairs = [
        (rule["source_rule_id"], rule["classification"])
        for rule in discovery["rules"]
    ]
    inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    independent_ids = [pair[0] for pair in independent_pairs]
    domain_ids = [
        rule["source_rule_id"]
        for rule in independent["rules"]
        if rule["classification"] == "DOMAIN_LEMMA"
    ]
    source_rule_ids = [rule["source_rule_id"] for rule in obligations["source_rules"]]
    obligation_ids = [rule["source_rule_id"] for rule in obligations["obligations"]]

    target = klean_export.target_statement(GENERATED)
    expected_target_definition = klean_export.expected_target_definition(obligations)
    classifications = {rule["source_rule_id"]: rule["classification"] for rule in independent["rules"]}
    simplification_policy = all(
        "simplification" not in rule["attributes"]
        or classifications[rule["source_rule_id"]] in {"DEFINITION", "DOMAIN_LEMMA"}
        for rule in inventory["rules"]
    )

    checks = {
        "audit_mode_classification_only": os.environ.get("AUDIT_MODE")
        == "CLASSIFICATION_ONLY",
        "candidate_absent": not Path("/candidate").exists(),
        "audit_lean_paths_null": audit["lean_workspace"] is None
        and audit["lean_invocation"] is None,
        "audit_lean_hashes_null": audit["hashes"]["lean_workspace_sha256"] is None
        and audit["hashes"]["lean_invocation_sha256"] is None,
        "pipeline_stage1_hash": pipeline_stage1_hash
        == audit["hashes"]["k_workspace_sha256"],
        "export_stage1_hash": export_stage1_hash
        == audit["hashes"]["stage1_export_sha256"],
        "k_audit_hash": k_audit_hash == audit["hashes"]["k_audit_sha256"],
        "discovery_hash": discovery_hash
        == audit["hashes"]["discovery_manifest_sha256"],
        "generation_hash": generation_hash
        == audit["hashes"]["klean_generation_sha256"],
        "generated_hash": generated_hash
        == audit["hashes"]["generated_tree_sha256"],
        "all_stage1_source_hashes": observed_source_hashes == expected_source_hashes,
        "inventory_hash": inventory["inventory_sha256"]
        == discovery["inventory_sha256"]
        == independent["inventory_sha256"]
        == input_manifest["inventory_sha256"]
        == generator["provenance"]["inventory_sha256"],
        "classification_order_and_values": independent_pairs == protected_pairs,
        "classification_inventory_bijection": independent_ids == inventory_ids
        and len(independent_ids) == len(set(independent_ids)),
        "simplification_policy": simplification_policy,
        "true_domain_set_empty": domain_ids == [],
        "input_source_rules_empty": input_manifest["source_rules"] == [],
        "obligation_source_rules_empty": source_rule_ids == [],
        "obligations_empty": obligation_ids == [],
        "source_obligation_bijection": domain_ids == source_rule_ids == obligation_ids,
        "trust_parameters_empty": obligations["trust_parameters"] == [],
        "obligation_count_zero": generator["obligation_count"]
        == export_result["obligation_count"]
        == preflight["obligation_count"]
        == 0,
        "obligation_map_hash": obligation_map_hash
        == generator["obligation_map_sha256"],
        "generated_tree_manifest": generated_hash
        == generator["generated_tree_sha256"]
        == export_result["generated_tree_sha256"]
        == preflight["generated_tree_sha256"],
        "stage1_export_manifest": export_stage1_hash
        == input_manifest["stage1_workspace_sha256"]
        == generator["provenance"]["stage1_workspace_sha256"]
        == export_result["frozen_input_sha256"]
        == preflight["stage1_workspace_sha256"],
        "discovery_manifest_binding": discovery_hash
        == input_manifest["stage3_discovery_manifest_sha256"]
        == generator["provenance"]["stage3_discovery_manifest_sha256"]
        == export_result["stage3_discovery_manifest_sha256"]
        == preflight["stage3_discovery_manifest_sha256"],
        "verification_hash_binding": sha256_file(K_PROOF / "verification.k")
        == input_manifest["verification_sha256"],
        "trust_inventory_hash": trust_hash == export_result["trust_inventory_sha256"],
        "no_expected_target_definition": expected_target_definition is None,
        "no_generated_target": target is None,
        "all_manifest_targets_null": generator["target"] is None
        and preflight["target"] is None
        and audit.get("target") is None,
        "all_statuses_no_obligations": export_result["status"]
        == preflight["status"]
        == audit["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS",
    }
    result = {
        "observed_hashes": {
            "k_workspace_sha256": pipeline_stage1_hash,
            "stage1_export_sha256": export_stage1_hash,
            "k_audit_sha256": k_audit_hash,
            "discovery_manifest_sha256": discovery_hash,
            "klean_generation_sha256": generation_hash,
            "generated_tree_sha256": generated_hash,
            "trust_inventory_sha256": trust_hash,
            "obligation_map_sha256": obligation_map_hash,
        },
        "stage1_source_file_count": len(observed_source_hashes),
        "independent_domain_rule_ids": domain_ids,
        "mapped_source_rule_ids": source_rule_ids,
        "mapped_obligation_ids": obligation_ids,
        "target": target,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
