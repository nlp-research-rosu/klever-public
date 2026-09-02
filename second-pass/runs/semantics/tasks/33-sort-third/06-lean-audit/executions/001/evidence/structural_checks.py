#!/usr/bin/env python3
"""Independent structural checks using only the trusted /reference/tools code."""

from __future__ import annotations

import hashlib
import json
import stat
from pathlib import Path

from tools import (
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)
from tools.k_rule_inventory import inventory_verification


def load(path: Path) -> dict:
    value = json.loads(path.read_bytes())
    if not isinstance(value, dict):
        raise TypeError(f"{path} is not a JSON object")
    return value


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_file_names(root: Path) -> list[str]:
    names: list[str] = []
    for path in sorted(root.rglob("*")):
        mode = path.stat(follow_symlinks=False).st_mode
        if stat.S_ISREG(mode):
            names.append(path.relative_to(root).as_posix())
        elif not stat.S_ISDIR(mode):
            raise RuntimeError(f"unsafe tree entry: {path}")
    return names


audit_input = load(Path("/audit-input.json"))
resolution = audit_input["resolution"]
discovery = load(Path("/reference/lemma-discovery.json"))
source_manifest = load(Path("/reference/generation-tools/source-manifest.json"))
generator_manifest = load(
    Path("/reference/klean-generation/generator-manifest.json")
)
input_manifest = load(Path("/reference/klean-generation/input-manifest.json"))
export_result = load(Path("/reference/klean-generation/export-result.json"))
obligation_map = load(
    Path("/reference/klean-generation/generated/obligation-map.json")
)
trust_inventory_path = Path("/reference/klean-generation/trust-inventory.json")
toolchain_lock = load(Path("/reference/klean-toolchain.lock.json"))

inventory = inventory_verification(Path("/reference/k-proof"))
validated = lemma_discovery_contract.validate_trust_boundary(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
)

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
per_rule_reconstruction = []
for rule in inventory["rules"]:
    normalized = " ".join(rule["text"].split())
    recomputed_normalized_hash = hashlib.sha256(normalized.encode()).hexdigest()
    per_rule_reconstruction.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "attributes": rule["attributes"],
            "normalized_sha256": rule["normalized_sha256"],
            "recomputed_normalized_sha256": recomputed_normalized_hash,
            "source_rule_id_matches_hash": (
                rule["source_rule_id"] == f"rule-{recomputed_normalized_hash}"
            ),
            "text": rule["text"],
        }
    )

producer_hashes = {
    name: file_hash(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
audit_image_id = (
    "sha256:"
    + Path(resolution["generation_producer_sources"]).name
)
producer_checks = {
    "bundle_regular_files_exact": regular_file_names(
        Path("/reference/generation-tools")
    )
    == ["klean.py", "klean_export.py", "source-manifest.json"],
    "source_manifest_files_match_observed": (
        source_manifest["files"] == producer_hashes
    ),
    "generator_manifest_exporter_matches_observed": (
        generator_manifest["exporter_sha256"]
        == producer_hashes["klean_export.py"]
    ),
    "generator_manifest_klean_matches_observed": (
        generator_manifest["klean_py_sha256"] == producer_hashes["klean.py"]
    ),
    "source_manifest_image_matches_generator": (
        source_manifest["generator_image_id"]
        == generator_manifest["provenance"]["generator_image_id"]
    ),
    "source_manifest_image_matches_audit_input_path": (
        source_manifest["generator_image_id"] == audit_image_id
    ),
}

actual_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": file_hash(
        Path("/reference/lemma-discovery.json")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_invocation_sha256": None,
    "lean_workspace_sha256": None,
}
recorded_hashes = resolution["hashes"]
hash_checks = {
    key: actual_hashes[key] == recorded_hashes[key]
    for key in actual_hashes
}

actual_stage1_source_hashes = {
    path.relative_to("/reference/k-proof").as_posix(): file_hash(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "Stage 1 source workspace"
    )
}

discovery_hash = actual_hashes["discovery_manifest_sha256"]
domain_source_rules = klean_export._domain_source_rules(
    validated, discovery_hash
)
target = klean_export.target_statement(
    Path("/reference/klean-generation/generated")
)
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)

manifest_checks = {
    "audit_input_envelope_valid": (
        stage6_resolution_contract.verify_audit_input(audit_input)[1]
        == audit_input["resolved_input_sha256"]
    ),
    "audit_input_copy_exact": (
        file_hash(Path("/audit-input.json"))
        == file_hash(Path("/audit-output/audit-input.json"))
    ),
    "all_recorded_top_level_hashes_match": all(hash_checks.values()),
    "all_stage1_source_hashes_match": (
        actual_stage1_source_hashes == resolution["stage1_source_hashes"]
    ),
    "verification_hash_matches_inventory": (
        inventory["verification_sha256"]
        == file_hash(Path("/reference/k-proof/verification.k"))
    ),
    "verification_hash_matches_input_manifest": (
        input_manifest["verification_sha256"]
        == inventory["verification_sha256"]
    ),
    "inventory_hash_matches_discovery": (
        inventory["inventory_sha256"] == discovery["inventory_sha256"]
    ),
    "inventory_hash_matches_input_manifest": (
        inventory["inventory_sha256"] == input_manifest["inventory_sha256"]
    ),
    "input_manifest_definitions_exact_and_ordered": (
        input_manifest["definitions"] == validated["definitions"]
    ),
    "input_manifest_operational_rules_exact_and_ordered": (
        input_manifest["operational_rules"] == validated["operational_rules"]
    ),
    "input_manifest_proved_derived_lemmas_exact_and_ordered": (
        input_manifest["proved_derived_lemmas"]
        == validated["proved_derived_lemmas"]
    ),
    "generator_toolchain_matches_lock": (
        generator_manifest["toolchain"] == toolchain_lock
    ),
    "generator_tree_hash_matches": (
        generator_manifest["generated_tree_sha256"]
        == actual_hashes["generated_tree_sha256"]
    ),
    "generator_obligation_map_hash_matches": (
        generator_manifest["obligation_map_sha256"]
        == file_hash(
            Path("/reference/klean-generation/generated/obligation-map.json")
        )
    ),
    "generator_stage1_provenance_matches": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == actual_hashes["stage1_export_sha256"]
    ),
    "generator_discovery_provenance_matches": (
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == discovery_hash
    ),
    "generator_inventory_provenance_matches": (
        generator_manifest["provenance"]["inventory_sha256"]
        == inventory["inventory_sha256"]
    ),
    "input_manifest_stage1_hashes_match": (
        input_manifest["frozen_input_sha256"]
        == actual_hashes["stage1_export_sha256"]
        == input_manifest["stage1_workspace_sha256"]
    ),
    "input_manifest_discovery_hash_matches": (
        input_manifest["stage3_discovery_manifest_sha256"]
        == discovery_hash
    ),
    "input_manifest_source_rules_match_independent_domain_set": (
        input_manifest["source_rules"] == domain_source_rules
    ),
    "obligation_map_source_rules_match_independent_domain_set": (
        obligation_map["source_rules"] == domain_source_rules
    ),
    "obligations_count_matches_generator": (
        len(obligation_map["obligations"])
        == generator_manifest["obligation_count"]
    ),
    "obligation_source_ids_unique_and_ordered": (
        [item["source_rule_id"] for item in obligation_map["obligations"]]
        == [item["source_rule_id"] for item in domain_source_rules]
        and len(
            {
                item["source_rule_id"]
                for item in obligation_map["obligations"]
            }
        )
        == len(obligation_map["obligations"])
    ),
    "zero_obligations_have_no_target_definition": (
        len(domain_source_rules) != 0
        or (expected_target_definition is None and target is None)
    ),
    "target_matches_generator_manifest": (
        target == generator_manifest["target"]
    ),
    "target_matches_audit_input": target == resolution["target"],
    "export_result_stage1_hash_matches": (
        export_result["frozen_input_sha256"]
        == actual_hashes["stage1_export_sha256"]
    ),
    "export_result_discovery_hash_matches": (
        export_result["stage3_discovery_manifest_sha256"]
        == discovery_hash
    ),
    "export_result_generated_hash_matches": (
        export_result["generated_tree_sha256"]
        == actual_hashes["generated_tree_sha256"]
    ),
    "export_result_trust_inventory_hash_matches": (
        export_result["trust_inventory_sha256"]
        == file_hash(trust_inventory_path)
    ),
    "export_result_obligation_count_matches": (
        export_result["obligation_count"] == len(obligation_map["obligations"])
    ),
    "export_result_status_matches_empty_set": (
        export_result["status"]
        == (
            "KLEAN_NO_OBLIGATIONS"
            if not obligation_map["obligations"]
            else "OK"
        )
    ),
    "audit_mode_matches_no_obligations": (
        resolution["mode"] == "CLASSIFICATION_ONLY"
        and not obligation_map["obligations"]
        and resolution["stage5_result"] is None
        and resolution["lean_workspace"] is None
        and resolution["lean_invocation"] is None
    ),
    "candidate_absent": not Path("/candidate").exists(),
}

classification_counts = {
    "definitions": len(validated["definitions"]),
    "operational_rules": len(validated["operational_rules"]),
    "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
    "domain_lemmas": len(validated["domain_lemmas"]),
}

result = {
    "producer_hashes": producer_hashes,
    "producer_checks": producer_checks,
    "actual_hashes": actual_hashes,
    "recorded_hashes": recorded_hashes,
    "hash_checks": hash_checks,
    "inventory_summary": {
        "schema_version": inventory["schema_version"],
        "verification_file": inventory["verification_file"],
        "verification_sha256": inventory["verification_sha256"],
        "verification_module": inventory["verification_module"],
        "verification_modules": inventory["verification_modules"],
        "inventory_sha256": inventory["inventory_sha256"],
        "rule_count": len(inventory["rules"]),
        "manifest_rule_count": len(discovery["rules"]),
        "canonical_ids": canonical_ids,
        "manifest_ids": manifest_ids,
        "no_duplicate_manifest_ids": len(manifest_ids) == len(set(manifest_ids)),
        "identity_order_exact": canonical_ids == manifest_ids,
        "classification_counts": classification_counts,
    },
    "per_rule_reconstruction": per_rule_reconstruction,
    "domain_source_rules": domain_source_rules,
    "obligation_map": obligation_map,
    "observed_target": target,
    "expected_target_definition": expected_target_definition,
    "manifest_checks": manifest_checks,
}

print(json.dumps(result, indent=2, sort_keys=True))

all_checks = (
    all(producer_checks.values())
    and all(hash_checks.values())
    and all(manifest_checks.values())
    and result["inventory_summary"]["no_duplicate_manifest_ids"]
    and result["inventory_summary"]["identity_order_exact"]
    and all(
        item["source_rule_id_matches_hash"]
        and item["normalized_sha256"]
        == item["recomputed_normalized_sha256"]
        for item in per_rule_reconstruction
    )
)
raise SystemExit(0 if all_checks else 1)
